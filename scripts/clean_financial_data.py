from pathlib import Path

import pandas as pd


# ============================================================
# 1. Project paths
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "financial_reporting_raw.xlsx"
)

CLEANED_FILE = (
    PROJECT_DIR
    / "data"
    / "cleaned"
    / "financial_reporting_cleaned.xlsx"
)

SHEET_NAME = "Raw_Data"


# ============================================================
# 2. Data loading
# ============================================================

def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Load the raw financial data from the Excel file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}\n"
            "Check that financial_reporting_raw.xlsx is inside data/raw."
        )

    dataframe = pd.read_excel(
        file_path,
        sheet_name=SHEET_NAME,
        engine="openpyxl",
    )

    return dataframe


# ============================================================
# 3. Data cleaning functions
# ============================================================

def clean_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and remove duplicate rows."""

    duplicate_count = df.duplicated().sum()

    print("\nNumber of duplicate rows before cleaning:")
    print(duplicate_count)

    duplicate_rows = df[df.duplicated(keep=False)]

    if not duplicate_rows.empty:
        print("\nDuplicate rows:")
        print(duplicate_rows.to_string(index=False))

    df = df.drop_duplicates()

    duplicate_count_after = df.duplicated().sum()

    print("\nNumber of duplicate rows after cleaning:")
    print(duplicate_count_after)

    print("\nNumber of rows after removing duplicates:")
    print(df.shape[0])

    return df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and remove rows with missing values in critical columns."""

    missing_values_before = df.isna().sum()

    print("\nMissing values before cleaning:")
    print(missing_values_before)

    rows_with_missing_values = df[df.isna().any(axis=1)]

    if not rows_with_missing_values.empty:
        print("\nRows with missing values:")
        print(rows_with_missing_values.to_string(index=False))

    critical_columns = ["Activité", "CA_Réalisé"]

    df = df.dropna(subset=critical_columns)

    missing_values_after = df.isna().sum()

    print("\nMissing values after cleaning:")
    print(missing_values_after)

    print("\nNumber of rows after removing incomplete records:")
    print(df.shape[0])

    return df


def clean_agencies(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and correct invalid agency names."""

    valid_agencies = [
        "Paris",
        "Nanterre",
        "Boulogne",
        "Saint-Denis",
        "Créteil",
    ]

    invalid_agencies_before = df.loc[
        ~df["Agence"].isin(valid_agencies),
        "Agence",
    ].value_counts()

    print("\nInvalid agency names before cleaning:")
    print(invalid_agencies_before)

    agency_corrections = {
        "Nanterrre": "Nanterre",
        "Creteil": "Créteil",
        "Boulognee": "Boulogne",
    }

    df["Agence"] = df["Agence"].replace(agency_corrections)

    invalid_agencies_after = df.loc[
        ~df["Agence"].isin(valid_agencies),
        "Agence",
    ].value_counts()

    print("\nInvalid agency names after cleaning:")
    print(invalid_agencies_after)

    return df


def clean_negative_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and remove rows with negative actual expenses."""

    negative_expenses = df[df["Charges_Réelles"] < 0]

    print("\nRows with negative actual expenses before cleaning:")

    if not negative_expenses.empty:
        print(negative_expenses.to_string(index=False))
    else:
        print("None")

    print("\nNumber of negative actual expenses before cleaning:")
    print(negative_expenses.shape[0])

    df = df[df["Charges_Réelles"] >= 0]

    negative_expenses_after = df[df["Charges_Réelles"] < 0]

    print("\nNumber of negative actual expenses after cleaning:")
    print(negative_expenses_after.shape[0])

    print("\nNumber of rows after removing negative expenses:")
    print(df.shape[0])

    return df


def clean_abnormal_client_counts(df: pd.DataFrame, max_clients: int) -> pd.DataFrame:
    """Detect and remove rows with abnormal client counts."""

    abnormal_client_counts = df[df["Nombre_Clients"] > max_clients]

    print("\nRows with abnormal client counts before cleaning:")

    if not abnormal_client_counts.empty:
        print(abnormal_client_counts.to_string(index=False))
    else:
        print("None")

    print("\nNumber of abnormal client counts before cleaning:")
    print(abnormal_client_counts.shape[0])

    df = df[df["Nombre_Clients"] <= max_clients]

    abnormal_client_counts_after = df[df["Nombre_Clients"] > max_clients]

    print("\nNumber of abnormal client counts after cleaning:")
    print(abnormal_client_counts_after.shape[0])

    print("\nNumber of rows after removing abnormal client counts:")
    print(df.shape[0])

    return df


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the Date column to a standard datetime format."""

    text_dates = df[df["Date"].apply(lambda value: isinstance(value, str))]

    print("\nRows with dates stored as text before cleaning:")

    if not text_dates.empty:
        print(text_dates.to_string(index=False))
    else:
        print("None")

    print("\nNumber of dates stored as text before cleaning:")
    print(text_dates.shape[0])

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
        dayfirst=True,
    )

    invalid_dates_after_conversion = df[df["Date"].isna()]

    print("\nNumber of invalid dates after conversion:")
    print(invalid_dates_after_conversion.shape[0])

    df = df.dropna(subset=["Date"])

    print("\nNumber of rows after removing invalid dates:")
    print(df.shape[0])

    print("\nDate column type after cleaning:")
    print(df["Date"].dtype)

    return df


# ============================================================
# 4. Financial indicator functions
# ============================================================

def create_financial_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Create financial performance indicators."""

    df["Marge_Réelle"] = df["CA_Réalisé"] - df["Charges_Réelles"]
    df["Marge_Budget"] = df["Budget_CA"] - df["Budget_Charges"]
    df["Écart_CA"] = df["CA_Réalisé"] - df["Budget_CA"]
    df["Écart_Charges"] = df["Charges_Réelles"] - df["Budget_Charges"]
    df["Taux_Marge"] = df["Marge_Réelle"] / df["CA_Réalisé"]

    print("\nFinancial indicators created:")
    print([
        "Marge_Réelle",
        "Marge_Budget",
        "Écart_CA",
        "Écart_Charges",
        "Taux_Marge",
    ])

    print("\nFirst 10 rows with financial indicators:")
    print(
        df[
            [
                "Date",
                "Agence",
                "Activité",
                "CA_Réalisé",
                "Charges_Réelles",
                "Marge_Réelle",
                "Écart_CA",
                "Taux_Marge",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    return df


# ============================================================
# 5. Output and reporting functions
# ============================================================

def display_dataset_structure(df: pd.DataFrame) -> None:
    """Display the final dataset structure."""

    print(f"\nNumber of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df.head(10).to_string(index=False))

    print("\nData types:")
    print(df.dtypes)


def display_cleaning_summary(df: pd.DataFrame, max_clients: int) -> None:
    """Display a final summary of remaining data quality issues."""

    print("\nCleaning summary:")
    print(f"Final number of rows: {df.shape[0]}")
    print(f"Final number of columns: {df.shape[1]}")
    print(f"Duplicate rows remaining: {df.duplicated().sum()}")
    print(f"Missing values remaining: {df.isna().sum().sum()}")
    print(f"Negative actual expenses remaining: {(df['Charges_Réelles'] < 0).sum()}")
    print(f"Abnormal client counts remaining: {(df['Nombre_Clients'] > max_clients).sum()}")


def export_cleaned_data(df: pd.DataFrame, output_path: Path) -> None:
    """Export the cleaned dataset to an Excel file."""

    df.to_excel(
        output_path,
        index=False,
        engine="openpyxl",
    )

    print("\nCleaned file exported successfully:")
    print(output_path)


# ============================================================
# 6. Main workflow
# ============================================================

def main() -> None:
    """Run the full financial data cleaning pipeline."""

    max_clients = 200

    print("Loading raw financial data...\n")

    df = load_raw_data(RAW_FILE)

    print("File loaded successfully.")

    df = clean_duplicates(df)
    df = clean_missing_values(df)
    df = clean_agencies(df)
    df = clean_negative_expenses(df)
    df = clean_abnormal_client_counts(df, max_clients)
    df = clean_dates(df)
    df = create_financial_indicators(df)

    display_dataset_structure(df)
    display_cleaning_summary(df, max_clients)

    export_cleaned_data(df, CLEANED_FILE)


# ============================================================
# 7. Script entry point
# ============================================================

if __name__ == "__main__":
    main()