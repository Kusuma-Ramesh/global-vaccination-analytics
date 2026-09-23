from sqlalchemy import (
    Column, String, SmallInteger, BigInteger, Numeric, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class DimCountry(Base):
    __tablename__ = "dim_country"

    country_code = Column(String(10), primary_key=True)
    country_name = Column(String(150), nullable=False)
    who_region = Column(String(10))


class DimDisease(Base):
    __tablename__ = "dim_disease"

    disease_code = Column(String(30), primary_key=True)
    disease_description = Column(String(200))


class DimVaccine(Base):
    __tablename__ = "dim_vaccine"

    vaccine_code = Column(String(30), primary_key=True)
    vaccine_description = Column(String(200))


class FactCoverage(Base):
    __tablename__ = "fact_coverage"

    id = Column(BigInteger, primary_key=True)
    country_code = Column(String(10), ForeignKey("dim_country.country_code"))
    year = Column(SmallInteger, nullable=False)
    vaccine_code = Column(String(30), ForeignKey("dim_vaccine.vaccine_code"))
    coverage_category = Column(String(20))
    coverage_category_description = Column(String(100))
    target_number = Column(BigInteger)
    doses = Column(BigInteger)
    coverage = Column(Numeric(6, 2))

    country = relationship("DimCountry")
    vaccine = relationship("DimVaccine")


class FactIncidenceRate(Base):
    __tablename__ = "fact_incidence_rate"

    id = Column(BigInteger, primary_key=True)
    country_code = Column(String(10), ForeignKey("dim_country.country_code"))
    year = Column(SmallInteger, nullable=False)
    disease_code = Column(String(30), ForeignKey("dim_disease.disease_code"))
    denominator = Column(String(60))
    incidence_rate = Column(Numeric(14, 4))

    country = relationship("DimCountry")
    disease = relationship("DimDisease")


class FactReportedCases(Base):
    __tablename__ = "fact_reported_cases"

    id = Column(BigInteger, primary_key=True)
    country_code = Column(String(10), ForeignKey("dim_country.country_code"))
    year = Column(SmallInteger, nullable=False)
    disease_code = Column(String(30), ForeignKey("dim_disease.disease_code"))
    cases = Column(BigInteger)

    country = relationship("DimCountry")
    disease = relationship("DimDisease")


class FactVaccineIntroduction(Base):
    __tablename__ = "fact_vaccine_introduction"

    id = Column(BigInteger, primary_key=True)
    country_code = Column(String(10), ForeignKey("dim_country.country_code"))
    who_region = Column(String(10))
    year = Column(SmallInteger, nullable=False)
    vaccine_description = Column(String(200))
    introduced = Column(Boolean)

    country = relationship("DimCountry")


class FactVaccineSchedule(Base):
    __tablename__ = "fact_vaccine_schedule"

    id = Column(BigInteger, primary_key=True)
    country_code = Column(String(10), ForeignKey("dim_country.country_code"))
    who_region = Column(String(10))
    year = Column(SmallInteger, nullable=False)
    vaccine_code = Column(String(30))
    vaccine_description = Column(String(200))
    schedule_rounds = Column(SmallInteger)
    target_pop = Column(String(100))
    target_pop_description = Column(String(200))
    geoarea = Column(String(100))
    age_administered = Column(String(60))
    source_comment = Column(String, nullable=True)

    country = relationship("DimCountry")
