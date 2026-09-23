from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/correlation", response_model=List[schemas.CorrelationPoint])
def coverage_vs_incidence(
    vaccine_code: str = Query("MCV1", description="Vaccine/antigen code"),
    disease_code: str = Query("MEASLES", description="Disease code"),
    year: int = Query(2023),
    coverage_category: str = Query("WUENIC"),
    db: Session = Depends(get_db),
):
    """Pairs each country's vaccination coverage with its disease incidence
    rate for the same year - used to answer 'how does coverage correlate
    with disease reduction' style questions, and to spot countries with
    high coverage but unexpectedly high incidence."""
    cov_sq = (
        db.query(
            models.FactCoverage.country_code,
            models.FactCoverage.coverage,
        )
        .filter(
            models.FactCoverage.vaccine_code == vaccine_code,
            models.FactCoverage.year == year,
            models.FactCoverage.coverage_category == coverage_category,
        )
        .subquery()
    )
    inc_sq = (
        db.query(
            models.FactIncidenceRate.country_code,
            models.FactIncidenceRate.incidence_rate,
        )
        .filter(
            models.FactIncidenceRate.disease_code == disease_code,
            models.FactIncidenceRate.year == year,
        )
        .subquery()
    )

    q = (
        db.query(
            models.DimCountry.country_code,
            models.DimCountry.country_name,
            cov_sq.c.coverage,
            inc_sq.c.incidence_rate,
        )
        .join(cov_sq, cov_sq.c.country_code == models.DimCountry.country_code)
        .join(inc_sq, inc_sq.c.country_code == models.DimCountry.country_code)
    )

    return [
        schemas.CorrelationPoint(
            country_code=r.country_code,
            country_name=r.country_name,
            coverage=float(r.coverage) if r.coverage is not None else None,
            incidence_rate=float(r.incidence_rate) if r.incidence_rate is not None else None,
        )
        for r in q.all()
    ]


@router.get("/summary", response_model=schemas.KpiSummary)
def kpi_summary(
    flagship_vaccine: str = Query("DTPCV3"),
    coverage_category: str = Query("WUENIC"),
    db: Session = Depends(get_db),
):
    latest_year = db.query(func.max(models.FactCoverage.year)).scalar() or 0

    avg_coverage = (
        db.query(func.avg(models.FactCoverage.coverage))
        .filter(
            models.FactCoverage.vaccine_code == flagship_vaccine,
            models.FactCoverage.year == latest_year,
            models.FactCoverage.coverage_category == coverage_category,
        )
        .scalar()
    )

    total_cases = (
        db.query(func.sum(models.FactReportedCases.cases))
        .filter(models.FactReportedCases.year == latest_year)
        .scalar()
    )

    countries_tracked = db.query(func.count(models.DimCountry.country_code)).scalar() or 0

    countries_high_coverage = (
        db.query(func.count(models.FactCoverage.country_code))
        .filter(
            models.FactCoverage.vaccine_code == flagship_vaccine,
            models.FactCoverage.year == latest_year,
            models.FactCoverage.coverage_category == coverage_category,
            models.FactCoverage.coverage >= 90,
        )
        .scalar()
        or 0
    )

    diseases_tracked = db.query(func.count(models.DimDisease.disease_code)).scalar() or 0

    return schemas.KpiSummary(
        latest_year=latest_year,
        global_avg_coverage=round(float(avg_coverage), 2) if avg_coverage is not None else None,
        total_reported_cases=int(total_cases) if total_cases is not None else None,
        countries_tracked=countries_tracked,
        countries_high_coverage=countries_high_coverage,
        diseases_tracked=diseases_tracked,
    )
