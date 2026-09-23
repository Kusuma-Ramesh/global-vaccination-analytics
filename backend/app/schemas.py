from typing import Optional
from pydantic import BaseModel


class CountryOut(BaseModel):
    country_code: str
    country_name: str
    who_region: Optional[str] = None

    class Config:
        from_attributes = True


class VaccineOut(BaseModel):
    vaccine_code: str
    vaccine_description: Optional[str] = None

    class Config:
        from_attributes = True


class DiseaseOut(BaseModel):
    disease_code: str
    disease_description: Optional[str] = None

    class Config:
        from_attributes = True


class CoverageTrendPoint(BaseModel):
    year: int
    coverage: Optional[float] = None
    doses: Optional[int] = None
    target_number: Optional[int] = None


class CoverageByCountryPoint(BaseModel):
    country_code: str
    country_name: str
    who_region: Optional[str] = None
    coverage: Optional[float] = None


class IncidenceTrendPoint(BaseModel):
    year: int
    incidence_rate: Optional[float] = None


class CasesTrendPoint(BaseModel):
    year: int
    cases: Optional[int] = None


class DoseDropoffPoint(BaseModel):
    year: int
    dose1_coverage: Optional[float] = None
    dose3_coverage: Optional[float] = None
    dropout_rate_pct: Optional[float] = None


class CorrelationPoint(BaseModel):
    country_code: str
    country_name: str
    coverage: Optional[float] = None
    incidence_rate: Optional[float] = None


class IntroductionTimelinePoint(BaseModel):
    year: int
    who_region: Optional[str] = None
    countries_introduced: int
    total_countries: int
    pct_introduced: Optional[float] = None


class KpiSummary(BaseModel):
    latest_year: int
    global_avg_coverage: Optional[float] = None
    total_reported_cases: Optional[int] = None
    countries_tracked: int
    countries_high_coverage: int  # >= 90% for the flagship vaccine
    diseases_tracked: int
