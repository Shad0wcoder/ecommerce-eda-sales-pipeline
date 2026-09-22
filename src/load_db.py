from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text



# Configuration


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "raw"
SQL_DIR = BASE_DIR / "sql"

load_dotenv(BASE_DIR / ".env")



# Database Configuration


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured. "
        "Create a .env file using .env.example."
    )

engine = create_engine(
    DATABASE_URL,
    future=True,
)



# Database Connection Test


def test_connection():
    """Verify that the database is reachable."""

    try:
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

        print("Database connection successful.")

    except Exception as exc:
        raise RuntimeError(
            "Could not connect to the database. "
            "Check DATABASE_URL and PostgreSQL."
        ) from exc



# Create Database Schema


def create_schema():
    """Execute the SQL schema file."""

    schema_file = SQL_DIR / "01_schema.sql"

    if not schema_file.exists():
        raise FileNotFoundError(
            f"Schema file not found: {schema_file}"
        )

    sql = schema_file.read_text(
        encoding="utf-8"
    )

    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    with engine.begin() as connection:

        for statement in statements:
            connection.execute(
                text(statement)
            )

    print("Database schema created successfully.")



# Load CSV into Database


def load_table(
    filename,
    table_name,
    parse_dates=None,
):
    """Load a CSV file into a database table."""

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(
        file_path,
        parse_dates=parse_dates,
    )

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi",
    )

    print(
        f"Loaded {len(df):,} rows "
        f"into '{table_name}'."
    )



# Main Pipeline


def main():

    print("=" * 60)
    print("E-COMMERCE DATABASE LOADING PIPELINE")
    print("=" * 60)

    test_connection()

    print("\nCreating database schema...")
    create_schema()

    print("\nLoading customers...")
    load_table(
        "customers.csv",
        "customers",
        parse_dates=["signup_date"],
    )


    print("\nLoading products...")
    load_table(
        "products.csv",
        "products",
    )

    print("\nLoading orders...")
    load_table(
        "orders.csv",
        "orders",
        parse_dates=[
            "order_date",
            "shipping_date",
            "delivery_date",
        ],
    )

    print("\nLoading order items...")
    load_table(
        "order_items.csv",
        "order_items",
    )

    print("\nLoading payments...")
    load_table(
        "payments.csv",
        "payments",
        parse_dates=["payment_date"],
    )

    print("\n" + "=" * 60)
    print("DATABASE LOADING COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()