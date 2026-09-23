from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import distinct
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["lookups"])


@router.get("/countries", response_model=List[schemas.CountryOut])
def list_countries(db: Session = Depends(get_db)):
    return (
        db.query(models.DimCountry)
        .order_by(models.DimCountry.country_name)
        .all()
    )


@router.get("/regions", response_model=List[str])
def list_regions(db: Session = Depends(get_db)):
    rows = (
        db.query(distinct(models.DimCountry.who_region))
        .filter(models.DimCountry.who_region.isnot(None))
        .order_by(models.DimCountry.who_region)
        .all()
    )
    return [r[0] for r in rows]


@router.get("/vaccines", response_model=List[schemas.VaccineOut])
def list_vaccines(db: Session = Depends(get_db)):
    return (
        db.query(models.DimVaccine)
        .order_by(models.DimVaccine.vaccine_description)
        .all()
    )


@router.get("/diseases", response_model=List[schemas.DiseaseOut])
def list_diseases(db: Session = Depends(get_db)):
    return (
        db.query(models.DimDisease)
        .order_by(models.DimDisease.disease_description)
        .all()
    )
