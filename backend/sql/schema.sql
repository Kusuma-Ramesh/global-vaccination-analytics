-- ============================================================
-- Vaccination Analytics Database Schema (PostgreSQL)
-- Normalized star-schema style: dimension tables + fact tables
-- ============================================================

DROP TABLE IF EXISTS fact_vaccine_schedule CASCADE;
DROP TABLE IF EXISTS fact_vaccine_introduction CASCADE;
DROP TABLE IF EXISTS fact_reported_cases CASCADE;
DROP TABLE IF EXISTS fact_incidence_rate CASCADE;
DROP TABLE IF EXISTS fact_coverage CASCADE;
DROP TABLE IF EXISTS dim_vaccine CASCADE;
DROP TABLE IF EXISTS dim_disease CASCADE;
DROP TABLE IF EXISTS dim_country CASCADE;

-- ---------------------------------------------------------
-- Dimension: Country
-- ---------------------------------------------------------
CREATE TABLE dim_country (
    country_code    VARCHAR(10) PRIMARY KEY,   -- ISO Alpha-3 code
    country_name    VARCHAR(150) NOT NULL,
    who_region      VARCHAR(10)                -- e.g. AFRO, AMRO, EMRO, EURO, SEARO, WPRO
);

-- ---------------------------------------------------------
-- Dimension: Disease
-- ---------------------------------------------------------
CREATE TABLE dim_disease (
    disease_code        VARCHAR(30) PRIMARY KEY,
    disease_description  VARCHAR(200)
);

-- ---------------------------------------------------------
-- Dimension: Vaccine / Antigen
-- ---------------------------------------------------------
CREATE TABLE dim_vaccine (
    vaccine_code         VARCHAR(30) PRIMARY KEY,
    vaccine_description  VARCHAR(200)
);

-- ---------------------------------------------------------
-- Fact: Coverage
-- One row per country / year / antigen / coverage_category
-- ---------------------------------------------------------
CREATE TABLE fact_coverage (
    id                          BIGSERIAL PRIMARY KEY,
    country_code                VARCHAR(10) REFERENCES dim_country(country_code),
    year                        SMALLINT NOT NULL,
    vaccine_code                VARCHAR(30) REFERENCES dim_vaccine(vaccine_code),
    coverage_category           VARCHAR(20),
    coverage_category_description VARCHAR(100),
    target_number               BIGINT,
    doses                       BIGINT,
    coverage                    NUMERIC(6,2)   -- percentage 0-100 (can exceed 100 slightly in source data)
);

CREATE INDEX idx_coverage_country_year ON fact_coverage(country_code, year);
CREATE INDEX idx_coverage_vaccine ON fact_coverage(vaccine_code);

-- ---------------------------------------------------------
-- Fact: Incidence Rate
-- ---------------------------------------------------------
CREATE TABLE fact_incidence_rate (
    id              BIGSERIAL PRIMARY KEY,
    country_code    VARCHAR(10) REFERENCES dim_country(country_code),
    year            SMALLINT NOT NULL,
    disease_code    VARCHAR(30) REFERENCES dim_disease(disease_code),
    denominator     VARCHAR(60),
    incidence_rate  NUMERIC(14,4)
);

CREATE INDEX idx_incidence_country_year ON fact_incidence_rate(country_code, year);
CREATE INDEX idx_incidence_disease ON fact_incidence_rate(disease_code);

-- ---------------------------------------------------------
-- Fact: Reported Cases
-- ---------------------------------------------------------
CREATE TABLE fact_reported_cases (
    id              BIGSERIAL PRIMARY KEY,
    country_code    VARCHAR(10) REFERENCES dim_country(country_code),
    year            SMALLINT NOT NULL,
    disease_code    VARCHAR(30) REFERENCES dim_disease(disease_code),
    cases           BIGINT
);

CREATE INDEX idx_cases_country_year ON fact_reported_cases(country_code, year);
CREATE INDEX idx_cases_disease ON fact_reported_cases(disease_code);

-- ---------------------------------------------------------
-- Fact: Vaccine Introduction
-- ---------------------------------------------------------
CREATE TABLE fact_vaccine_introduction (
    id              BIGSERIAL PRIMARY KEY,
    country_code    VARCHAR(10) REFERENCES dim_country(country_code),
    who_region      VARCHAR(10),
    year            SMALLINT NOT NULL,
    vaccine_description VARCHAR(200),
    introduced      BOOLEAN
);

CREATE INDEX idx_intro_country_year ON fact_vaccine_introduction(country_code, year);

-- ---------------------------------------------------------
-- Fact: Vaccine Schedule
-- ---------------------------------------------------------
CREATE TABLE fact_vaccine_schedule (
    id                      BIGSERIAL PRIMARY KEY,
    country_code            VARCHAR(10) REFERENCES dim_country(country_code),
    who_region              VARCHAR(10),
    year                    SMALLINT NOT NULL,
    vaccine_code            VARCHAR(30),
    vaccine_description     VARCHAR(200),
    schedule_rounds         SMALLINT,
    target_pop              VARCHAR(100),
    target_pop_description  VARCHAR(200),
    geoarea                 VARCHAR(100),
    age_administered        VARCHAR(60),
    source_comment          TEXT
);

CREATE INDEX idx_schedule_country_year ON fact_vaccine_schedule(country_code, year);
