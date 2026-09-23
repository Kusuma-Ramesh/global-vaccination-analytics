from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/coverage", tags=["coverage"])


@router.get("/trend", response_model=List[schemas.CoverageTrendPoint])
def coverage_trend(
    country_code: str = Query(..., description="ISO-3 country code, e.g. IND"),
    vaccine_code: str = Query("DTPCV3", description="Vaccine/antigen code, e.g. DTPCV3, MCV1, BCG"),
    coverage_category: str = Query("WUENIC", description="ADMIN | OFFICIAL | WUENIC"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(
        models.FactCoverage.year,
        func.avg(models.FactCoverage.coverage).label("coverage"),
        func.sum(models.FactCoverage.doses).label("doses"),
        func.sum(models.FactCoverage.target_number).label("target_number"),
    ).filter(
        models.FactCoverage.country_code == country_code,
        models.FactCoverage.vaccine_code == vaccine_code,
        models.FactCoverage.coverage_category == coverage_category,
    )
    if year_from:
        q = q.filter(models.FactCoverage.year >= year_from)
    if year_to:
        q = q.filter(models.FactCoverage.year <= year_to)
    q = q.group_by(models.FactCoverage.year).order_by(models.FactCoverage.year)

    return [
        schemas.CoverageTrendPoint(year=r.year, coverage=r.coverage, doses=r.doses, target_number=r.target_number)
        for r in q.all()
    ]


@router.get("/by-country", response_model=List[schemas.CoverageByCountryPoint])
def coverage_by_country(
    vaccine_code: str = Query("DTPCV3"),
    year: int = Query(2023),
    coverage_category: str = Query("WUENIC"),
    who_region: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = (
        db.query(
            models.FactCoverage.country_code,
            models.DimCountry.country_name,
            models.DimCountry.who_region,
            models.FactCoverage.coverage,
        )
        .join(models.DimCountry, models.DimCountry.country_code == models.FactCoverage.country_code)
        .filter(
            models.FactCoverage.vaccine_code == vaccine_code,
            models.FactCoverage.year == year,
            models.FactCoverage.coverage_category == coverage_category,
        )
    )
    if who_region:
        q = q.filter(models.DimCountry.who_region == who_region)
    q = q.order_by(models.FactCoverage.coverage.desc().nullslast())

    return [
        schemas.CoverageByCountryPoint(
            country_code=r.country_code, country_name=r.country_name,
            who_region=r.who_region, coverage=float(r.coverage) if r.coverage is not None else None,
        )
        for r in q.all()
    ]


@router.get("/dose-dropoff", response_model=List[schemas.DoseDropoffPoint])
def dose_dropoff(
    country_code: str = Query(..., description="ISO-3 country code"),
    dose1_code: str = Query("DTPCV1"),
    dose3_code: str = Query("DTPCV3"),
    coverage_category: str = Query("WUENIC"),
    db: Session = Depends(get_db),
):
    """WHO's classic drop-off indicator: comparing coverage of the 1st dose
    vs. the 3rd/final dose of the same vaccine schedule (e.g. DTP1 -> DTP3)."""

    def series(vaccine_code: str):
        rows = (
            db.query(models.FactCoverage.year, func.avg(models.FactCoverage.coverage))
            .filter(
                models.FactCoverage.country_code == country_code,
                models.FactCoverage.vaccine_code == vaccine_code,
                models.FactCoverage.coverage_category == coverage_category,
            )
            .group_by(models.FactCoverage.year)
            .all()
        )
        return {year: float(cov) if cov is not None else None for year, cov in rows}

    dose1 = series(dose1_code)
    dose3 = series(dose3_code)
    years = sorted(set(dose1) | set(dose3))

    results = []
    for y in years:
        d1 = dose1.get(y)
        d3 = dose3.get(y)
        dropout = None
        if d1 and d1 > 0 and d3 is not None:
            dropout = round((d1 - d3) / d1 * 100, 2)
        results.append(schemas.DoseDropoffPoint(year=y, dose1_coverage=d1, dose3_coverage=d3, dropout_rate_pct=dropout))
    return results
