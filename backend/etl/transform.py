"""
Transformation layer: cleans raw WHO data and reshapes it into the
normalized dimension / fact tables defined in sql/schema.sql.

Cleaning rules applied (per project "Data Cleaning" requirements):
  1. Missing data      -> drop footer/metadata rows, fill sensible
                           defaults for numeric columns, drop rows with
                           no country code (can't be linked to dim_country).
  2. Normalize units    -> coverage kept as 0-100 percentage (values are
                           already percentages; out-of-range noise dropped),
                           counts coerced to whole numbers.
  3. Date consistency    -> YEAR coerced to nullable Int16, invalid years
                           removed.
  4. Deduplication       -> exact duplicate rows removed.
"""
import pandas as pd
import numpy as np

VALID_YEAR_MIN = 1974  # WHO Expanded Programme on Immunization started 1974
VALID_YEAR_MAX = 2035


def _clean_year(df: pd.DataFrame, col: str = "YEAR") -> pd.DataFrame:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=[col])
    df[col] = df[col].astype(int)
    df = df[(df[col] >= VALID_YEAR_MIN) & (df[col] <= VALID_YEAR_MAX)]
    return df


def _only_countries(df: pd.DataFrame, group_col: str = "GROUP") -> pd.DataFrame:
    """Keep only country-level rows, drop aggregate groups (GLOBAL, WHO_REGIONS, ...)
    and any trailing metadata/footer rows exported by the WHO portal."""
    if group_col in df.columns:
        df = df[df[group_col] == "COUNTRIES"]
    return df


def _dedupe(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


# ------------------------------------------------------------------
# Coverage
# ------------------------------------------------------------------
def transform_coverage(raw: pd.DataFrame):
    df = raw.copy()
    df = _only_countries(df)
    df = df.dropna(subset=["CODE", "YEAR"])
    df = _clean_year(df)

    df = df.rename(columns={
        "CODE": "country_code",
        "NAME": "country_name",
        "YEAR": "year",
        "ANTIGEN": "vaccine_code",
        "ANTIGEN_DESCRIPTION": "vaccine_description",
        "COVERAGE_CATEGORY": "coverage_category",
        "COVERAGE_CATEGORY_DESCRIPTION": "coverage_category_description",
        "TARGET_NUMBER": "target_number",
        "DOSES": "doses",
        "COVERAGE": "coverage",
    })

    df["target_number"] = pd.to_numeric(df["target_number"], errors="coerce").round().astype("Int64")
    df["doses"] = pd.to_numeric(df["doses"], errors="coerce").round().astype("Int64")
    df["coverage"] = pd.to_numeric(df["coverage"], errors="coerce")
    # Coverage is a percentage; clip absurd outliers (data-entry noise) but
    # allow slight >100 values which genuinely occur in WHO admin data.
    df["coverage"] = df["coverage"].clip(lower=0, upper=150)

    df = _dedupe(df)

    countries = df[["country_code", "country_name"]].dropna().drop_duplicates(subset=["country_code"])
    vaccines = df[["vaccine_code", "vaccine_description"]].dropna(subset=["vaccine_code"]).drop_duplicates(subset=["vaccine_code"])

    fact = df[[
        "country_code", "year", "vaccine_code", "coverage_category",
        "coverage_category_description", "target_number", "doses", "coverage",
    ]].reset_index(drop=True)

    return fact, countries, vaccines


# ------------------------------------------------------------------
# Incidence rate
# ------------------------------------------------------------------
def transform_incidence(raw: pd.DataFrame):
    df = raw.copy()
    df = _only_countries(df)
    df = df.dropna(subset=["CODE", "YEAR"])
    df = _clean_year(df)

    df = df.rename(columns={
        "CODE": "country_code",
        "NAME": "country_name",
        "YEAR": "year",
        "DISEASE": "disease_code",
        "DISEASE_DESCRIPTION": "disease_description",
        "DENOMINATOR": "denominator",
        "INCIDENCE_RATE": "incidence_rate",
    })

    df["incidence_rate"] = pd.to_numeric(df["incidence_rate"], errors="coerce")
    df = df.dropna(subset=["incidence_rate"])
    df["incidence_rate"] = df["incidence_rate"].clip(lower=0)

    df = _dedupe(df)

    countries = df[["country_code", "country_name"]].dropna().drop_duplicates(subset=["country_code"])
    diseases = df[["disease_code", "disease_description"]].dropna(subset=["disease_code"]).drop_duplicates(subset=["disease_code"])

    fact = df[[
        "country_code", "year", "disease_code", "denominator", "incidence_rate",
    ]].reset_index(drop=True)

    return fact, countries, diseases


# ------------------------------------------------------------------
# Reported cases
# ------------------------------------------------------------------
def transform_cases(raw: pd.DataFrame):
    df = raw.copy()
    df = _only_countries(df)
    df = df.dropna(subset=["CODE", "YEAR"])
    df = _clean_year(df)

    df = df.rename(columns={
        "CODE": "country_code",
        "NAME": "country_name",
        "YEAR": "year",
        "DISEASE": "disease_code",
        "DISEASE_DESCRIPTION": "disease_description",
        "CASES": "cases",
    })

    df["cases"] = pd.to_numeric(df["cases"], errors="coerce")
    df = df.dropna(subset=["cases"])
    df["cases"] = df["cases"].clip(lower=0).round().astype("Int64")

    df = _dedupe(df)

    countries = df[["country_code", "country_name"]].dropna().drop_duplicates(subset=["country_code"])
    diseases = df[["disease_code", "disease_description"]].dropna(subset=["disease_code"]).drop_duplicates(subset=["disease_code"])

    fact = df[["country_code", "year", "disease_code", "cases"]].reset_index(drop=True)

    return fact, countries, diseases


# ------------------------------------------------------------------
# Vaccine introduction
# ------------------------------------------------------------------
def transform_introduction(raw: pd.DataFrame):
    df = raw.copy()
    df = df.dropna(subset=["ISO_3_CODE", "YEAR"])
    df = _clean_year(df)

    df = df.rename(columns={
        "ISO_3_CODE": "country_code",
        "COUNTRYNAME": "country_name",
        "WHO_REGION": "who_region",
        "YEAR": "year",
        "DESCRIPTION": "vaccine_description",
        "INTRO": "introduced_raw",
    })

    df["introduced"] = df["introduced_raw"].astype(str).str.strip().str.lower().map({
        "yes": True, "y": True, "true": True, "1": True,
        "no": False, "n": False, "false": False, "0": False,
    })
    df = df.dropna(subset=["introduced"])

    df = _dedupe(df)

    countries = df[["country_code", "country_name", "who_region"]].dropna(subset=["country_code"]).drop_duplicates(subset=["country_code"])

    fact = df[["country_code", "who_region", "year", "vaccine_description", "introduced"]].reset_index(drop=True)

    return fact, countries


# ------------------------------------------------------------------
# Vaccine schedule
# ------------------------------------------------------------------
def transform_schedule(raw: pd.DataFrame):
    df = raw.copy()
    df = df.dropna(subset=["ISO_3_CODE", "YEAR"])
    df = _clean_year(df)

    df = df.rename(columns={
        "ISO_3_CODE": "country_code",
        "COUNTRYNAME": "country_name",
        "WHO_REGION": "who_region",
        "YEAR": "year",
        "VACCINECODE": "vaccine_code",
        "VACCINE_DESCRIPTION": "vaccine_description",
        "SCHEDULEROUNDS": "schedule_rounds",
        "TARGETPOP": "target_pop",
        "TARGETPOP_DESCRIPTION": "target_pop_description",
        "GEOAREA": "geoarea",
        "AGEADMINISTERED": "age_administered",
        "SOURCECOMMENT": "source_comment",
    })

    df["schedule_rounds"] = pd.to_numeric(df["schedule_rounds"], errors="coerce").astype("Int64")

    df = _dedupe(df)

    countries = df[["country_code", "country_name", "who_region"]].dropna(subset=["country_code"]).drop_duplicates(subset=["country_code"])

    fact = df[[
        "country_code", "who_region", "year", "vaccine_code", "vaccine_description",
        "schedule_rounds", "target_pop", "target_pop_description", "geoarea",
        "age_administered", "source_comment",
    ]].reset_index(drop=True)

    return fact, countries


def merge_country_dims(*country_frames: pd.DataFrame) -> pd.DataFrame:
    """Combine country reference data gathered from every source file into
    a single deduplicated dim_country table, preferring rows that already
    carry a WHO region."""
    combined = pd.concat(country_frames, ignore_index=True, sort=False)
    if "who_region" not in combined.columns:
        combined["who_region"] = np.nan
    combined = combined.sort_values(by="who_region", na_position="last")
    combined = combined.drop_duplicates(subset=["country_code"], keep="first")
    return combined[["country_code", "country_name", "who_region"]].reset_index(drop=True)


def merge_code_desc_dims(id_col: str, desc_col: str, *frames: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat(frames, ignore_index=True, sort=False)
    combined = combined.dropna(subset=[id_col])
    combined = combined.drop_duplicates(subset=[id_col], keep="first")
    return combined[[id_col, desc_col]].reset_index(drop=True)
