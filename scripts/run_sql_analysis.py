from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# 1. Project paths
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = (
    PROJECT_DIR
    / "data"
    / "cleaned"
    / "financial_reporting.db"
)

SQL_FILE = (
    PROJECT_DIR
    / "sql"
    / "01_financial_analysis_queries.sql"
)


# ============================================================
# 2. SQL query execution
# ============================================================

def load_sql_queries(file_path: Path) -> list[str]:
    """Load SQL queries from a SQL file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql_content = file_path.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    return queries


def run_sql_analysis() -> None:
    """Run SQL audit and financial analysis queries."""

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Database file not found: {DATABASE_FILE}\n"
            "Run create_sqlite_database.py first."
        )

    queries = load_sql_queries(SQL_FILE)

    with sqlite3.connect(DATABASE_FILE) as connection:
        for index, query in enumerate(queries, start=1):
            print("\n" + "=" * 80)
            print(f"Query {index}")
            print("=" * 80)

            result = pd.read_sql_query(query, connection)

            if result.empty:
                print("No rows returned.")
            else:
                print(result.to_string(index=False))


# ============================================================
# 3. Script entry point
# ============================================================

if __name__ == "__main__":
    run_sql_analysis()