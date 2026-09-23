from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/vaccine", tags=["vaccine"])


@router.get("/introduction/timeline", response_model=List[schemas.IntroductionTimelinePoint])
def introduction_timeline(
    vaccine_description: str = Query(..., description="Exact vaccine description, e.g. 'Rotavirus vaccine'"),
    who_region: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """For a given vaccine, shows how many countries (per WHO region, or
    globally) had introduced it by each year - useful for spotting
    disparities in rollout timelines across regions."""
    total_countries_sq = (
        db.query(models.DimCountry.who_region, func.count(models.DimCountry.country_code).label("total"))
        .group_by(models.DimCountry.who_region)
        .subquery()
    )

    q = (
        db.query(
            models.FactVaccineIntroduction.year,
            models.FactVaccineIntroduction.who_region,
            func.sum(case((models.FactVaccineIntroduction.introduced.is_(True), 1), else_=0)).label("introduced_count"),
        )
        .filter(models.FactVaccineIntroduction.vaccine_description == vaccine_description)
    )
    if who_region:
        q = q.filter(models.FactVaccineIntroduction.who_region == who_region)
    q = q.group_by(models.FactVaccineIntroduction.year, models.FactVaccineIntroduction.who_region)
    q = q.order_by(models.FactVaccineIntroduction.year)

    region_totals = {r.who_region: r.total for r in db.query(total_countries_sq)}

    results = []
    for r in q.all():
        total = region_totals.get(r.who_region, 0)
        pct = round(r.introduced_count / total * 100, 1) if total else None
        results.append(
            schemas.IntroductionTimelinePoint(
                year=r.year, who_region=r.who_region,
                countries_introduced=r.introduced_count, total_countries=total, pct_introduced=pct,
            )
        )
    return results


@router.get("/introduction/list", response_model=List[str])
def list_introducible_vaccines(db: Session = Depends(get_db)):
    rows = (
        db.query(models.FactVaccineIntroduction.vaccine_description)
        .distinct()
        .order_by(models.FactVaccineIntroduction.vaccine_description)
        .all()
    )
    return [r[0] for r in rows]


@router.get("/schedule", response_model=List[dict])
def vaccine_schedule(
    country_code: str = Query(..., description="ISO-3 country code"),
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.FactVaccineSchedule).filter(models.FactVaccineSchedule.country_code == country_code)
    if year:
        q = q.filter(models.FactVaccineSchedule.year == year)
    q = q.order_by(models.FactVaccineSchedule.vaccine_description, models.FactVaccineSchedule.schedule_rounds)

    return [
        {
            "vaccine_code": r.vaccine_code,
            "vaccine_description": r.vaccine_description,
            "schedule_rounds": r.schedule_rounds,
            "target_pop_description": r.target_pop_description,
            "age_administered": r.age_administered,
            "year": r.year,
        }
        for r in q.all()
    ]
