from pathlib import Path

import sqlite3

import pandas as pd


# ============================================================
# 1. Project paths
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

CLEANED_FILE = (
    PROJECT_DIR
    / "data"
    / "cleaned"
    / "financial_reporting_cleaned.xlsx"
)

DATABASE_FILE = (
    PROJECT_DIR
    / "data"
    / "cleaned"
    / "financial_reporting.db"
)

TABLE_NAME = "financial_reporting_cleaned"


# ============================================================
# 2. Database creation
# ============================================================

def create_sqlite_database() -> None:
    """Create a SQLite database from the cleaned Excel dataset."""

    if not CLEANED_FILE.exists():
        raise FileNotFoundError(
            f"File not found: {CLEANED_FILE}\n"
            "Run clean_financial_data.py first."
        )

    df = pd.read_excel(
        CLEANED_FILE,
        engine="openpyxl",
    )

    with sqlite3.connect(DATABASE_FILE) as connection:
        df.to_sql(
            TABLE_NAME,
            connection,
            if_exists="replace",
            index=False,
        )

    print("SQLite database created successfully.")
    print(DATABASE_FILE)
    print(f"Table created: {TABLE_NAME}")
    print(f"Rows inserted: {df.shape[0]}")
    print(f"Columns inserted: {df.shape[1]}")


# ============================================================
# 3. Script entry point
# ============================================================

if __name__ == "__main__":
    create_sqlite_database()