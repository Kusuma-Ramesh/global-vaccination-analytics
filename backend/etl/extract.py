"""
Extraction layer: reads the raw WHO Excel files ('Data' sheet of each)
into pandas DataFrames. No cleaning happens here - just raw extraction.
"""
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FILES = {
    "coverage": "coverage-data.xlsx",
    "incidence": "incidence-rate-data.xlsx",
    "cases": "reported-cases-data.xlsx",
    "introduction": "vaccine-introduction-data.xlsx",
    "schedule": "vaccine-schedule-data.xlsx",
}


def _read(file_name: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Expected data file not found: {path}\n"
            f"Place the WHO source .xlsx files inside backend/data/"
        )
    print(f"[extract] Reading {file_name} ...")
    df = pd.read_excel(path, sheet_name="Data", engine="openpyxl")
    print(f"[extract]   -> {len(df):,} rows, {len(df.columns)} columns")
    return df


def extract_coverage() -> pd.DataFrame:
    return _read(FILES["coverage"])


def extract_incidence() -> pd.DataFrame:
    return _read(FILES["incidence"])


def extract_cases() -> pd.DataFrame:
    return _read(FILES["cases"])


def extract_introduction() -> pd.DataFrame:
    return _read(FILES["introduction"])


def extract_schedule() -> pd.DataFrame:
    return _read(FILES["schedule"])


def extract_all() -> dict:
    return {
        "coverage": extract_coverage(),
        "incidence": extract_incidence(),
        "cases": extract_cases(),
        "introduction": extract_introduction(),
        "schedule": extract_schedule(),
    }
