from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["disease"])


@router.get("/incidence/trend", response_model=List[schemas.IncidenceTrendPoint])
def incidence_trend(
    country_code: str = Query(..., description="ISO-3 country code"),
    disease_code: str = Query("MEASLES"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(
        models.FactIncidenceRate.year,
        func.avg(models.FactIncidenceRate.incidence_rate).label("incidence_rate"),
    ).filter(
        models.FactIncidenceRate.country_code == country_code,
        models.FactIncidenceRate.disease_code == disease_code,
    )
    if year_from:
        q = q.filter(models.FactIncidenceRate.year >= year_from)
    if year_to:
        q = q.filter(models.FactIncidenceRate.year <= year_to)
    q = q.group_by(models.FactIncidenceRate.year).order_by(models.FactIncidenceRate.year)

    return [
        schemas.IncidenceTrendPoint(year=r.year, incidence_rate=float(r.incidence_rate) if r.incidence_rate is not None else None)
        for r in q.all()
    ]


@router.get("/cases/trend", response_model=List[schemas.CasesTrendPoint])
def cases_trend(
    country_code: str = Query(..., description="ISO-3 country code"),
    disease_code: str = Query("MEASLES"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(
        models.FactReportedCases.year,
        func.sum(models.FactReportedCases.cases).label("cases"),
    ).filter(
        models.FactReportedCases.country_code == country_code,
        models.FactReportedCases.disease_code == disease_code,
    )
    if year_from:
        q = q.filter(models.FactReportedCases.year >= year_from)
    if year_to:
        q = q.filter(models.FactReportedCases.year <= year_to)
    q = q.group_by(models.FactReportedCases.year).order_by(models.FactReportedCases.year)

    return [
        schemas.CasesTrendPoint(year=r.year, cases=int(r.cases) if r.cases is not None else None)
        for r in q.all()
    ]


@router.get("/cases/by-country", response_model=List[dict])
def cases_by_country(
    disease_code: str = Query("MEASLES"),
    year: int = Query(2023),
    db: Session = Depends(get_db),
):
    q = (
        db.query(
            models.FactReportedCases.country_code,
            models.DimCountry.country_name,
            models.DimCountry.who_region,
            models.FactReportedCases.cases,
        )
        .join(models.DimCountry, models.DimCountry.country_code == models.FactReportedCases.country_code)
        .filter(models.FactReportedCases.disease_code == disease_code, models.FactReportedCases.year == year)
        .order_by(models.FactReportedCases.cases.desc().nullslast())
    )
    return [
        {"country_code": r.country_code, "country_name": r.country_name, "who_region": r.who_region, "cases": r.cases}
        for r in q.all()
    ]
