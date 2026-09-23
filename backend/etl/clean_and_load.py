"""
Main ETL entry point.

Usage (from the backend/ directory, with your virtualenv active and a
PostgreSQL server running / reachable using the credentials in .env):

    python -m etl.clean_and_load

This will:
  1. Extract the 5 raw WHO Excel files from backend/data/
  2. Clean & transform them into normalized DataFrames
  3. (Re)create the database schema (backend/sql/schema.sql)
  4. Bulk-load everything into PostgreSQL
"""
import time

from etl import extract, transform, load


def main():
    start = time.time()
    print("=" * 60)
    print("VACCINATION DATA ETL PIPELINE")
    print("=" * 60)

    # 1. EXTRACT --------------------------------------------------
    raw_coverage = extract.extract_coverage()
    raw_incidence = extract.extract_incidence()
    raw_cases = extract.extract_cases()
    raw_introduction = extract.extract_introduction()
    raw_schedule = extract.extract_schedule()

    # 2. TRANSFORM --------------------------------------------------
    print("\n[transform] Cleaning & normalizing data ...")
    fact_coverage, countries_a, vaccines_a = transform.transform_coverage(raw_coverage)
    fact_incidence, countries_b, diseases_a = transform.transform_incidence(raw_incidence)
    fact_cases, countries_c, diseases_b = transform.transform_cases(raw_cases)
    fact_introduction, countries_d = transform.transform_introduction(raw_introduction)
    fact_schedule, countries_e = transform.transform_schedule(raw_schedule)

    dim_country = transform.merge_country_dims(countries_a, countries_b, countries_c, countries_d, countries_e)
    dim_disease = transform.merge_code_desc_dims("disease_code", "disease_description", diseases_a, diseases_b)
    dim_vaccine = transform.merge_code_desc_dims("vaccine_code", "vaccine_description", vaccines_a)

    print(f"[transform] dim_country: {len(dim_country):,} rows")
    print(f"[transform] dim_disease: {len(dim_disease):,} rows")
    print(f"[transform] dim_vaccine: {len(dim_vaccine):,} rows")

    # 3 & 4. SCHEMA + LOAD --------------------------------------------------
    print("\n[load] Connecting to PostgreSQL ...")
    conn = load.get_connection()
    try:
        load.create_schema(conn)

        print("\n[load] Loading dimension tables ...")
        load.load_dim_country(conn, dim_country)
        load.load_dim_disease(conn, dim_disease)
        load.load_dim_vaccine(conn, dim_vaccine)

        print("\n[load] Loading fact tables ...")
        load.load_fact_coverage(conn, fact_coverage)
        load.load_fact_incidence(conn, fact_incidence)
        load.load_fact_cases(conn, fact_cases)
        load.load_fact_introduction(conn, fact_introduction)
        load.load_fact_schedule(conn, fact_schedule)
    finally:
        conn.close()

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"ETL COMPLETE in {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
