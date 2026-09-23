"""
Load layer: pushes cleaned DataFrames into PostgreSQL.

Uses psycopg2's COPY command (via a CSV buffer) for fast bulk loading of
potentially hundreds of thousands of rows - much faster than row-by-row
INSERTs or pandas.to_sql for this data volume.
"""
import io
import os
import sys

import pandas as pd
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import get_settings  # noqa: E402

SCHEMA_SQL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql", "schema.sql"
)


def get_connection():
    settings = get_settings()
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )


def create_schema(conn):
    print("[load] (Re)creating database schema ...")
    with open(SCHEMA_SQL_PATH, "r") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("[load] Schema ready.")


def _copy_dataframe(conn, df: pd.DataFrame, table: str, columns: list):
    if df.empty:
        print(f"[load] {table}: nothing to load (0 rows)")
        return
    buf = io.StringIO()
    df[columns].to_csv(buf, index=False, header=False, na_rep="\\N")
    buf.seek(0)
    with conn.cursor() as cur:
        cur.copy_expert(
            f"COPY {table} ({', '.join(columns)}) FROM STDIN WITH (FORMAT csv, NULL '\\N')",
            buf,
        )
    conn.commit()
    print(f"[load] {table}: loaded {len(df):,} rows")


def load_dim_country(conn, df: pd.DataFrame):
    _copy_dataframe(conn, df, "dim_country", ["country_code", "country_name", "who_region"])


def load_dim_disease(conn, df: pd.DataFrame):
    _copy_dataframe(conn, df, "dim_disease", ["disease_code", "disease_description"])


def load_dim_vaccine(conn, df: pd.DataFrame):
    _copy_dataframe(conn, df, "dim_vaccine", ["vaccine_code", "vaccine_description"])


def load_fact_coverage(conn, df: pd.DataFrame):
    cols = ["country_code", "year", "vaccine_code", "coverage_category",
            "coverage_category_description", "target_number", "doses", "coverage"]
    _copy_dataframe(conn, df, "fact_coverage", cols)


def load_fact_incidence(conn, df: pd.DataFrame):
    cols = ["country_code", "year", "disease_code", "denominator", "incidence_rate"]
    _copy_dataframe(conn, df, "fact_incidence_rate", cols)


def load_fact_cases(conn, df: pd.DataFrame):
    cols = ["country_code", "year", "disease_code", "cases"]
    _copy_dataframe(conn, df, "fact_reported_cases", cols)


def load_fact_introduction(conn, df: pd.DataFrame):
    cols = ["country_code", "who_region", "year", "vaccine_description", "introduced"]
    _copy_dataframe(conn, df, "fact_vaccine_introduction", cols)


def load_fact_schedule(conn, df: pd.DataFrame):
    cols = ["country_code", "who_region", "year", "vaccine_code", "vaccine_description",
            "schedule_rounds", "target_pop", "target_pop_description", "geoarea",
            "age_administered", "source_comment"]
    _copy_dataframe(conn, df, "fact_vaccine_schedule", cols)
