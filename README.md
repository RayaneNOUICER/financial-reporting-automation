# Financial Reporting Automation

## Project Objective

This project automates the cleaning, preparation and analysis of a raw financial reporting dataset using Python, Excel and SQL.

The goal is to transform an imperfect Excel file into a clean and reliable dataset that can be used for financial reporting, SQL analysis, or Power BI dashboards.

## Tools Used

- Python
- pandas
- openpyxl
- SQLite
- SQL
- Excel

## Data Quality Controls

The Python script performs several data quality checks:

- Detects and removes duplicate rows
- Detects missing values in critical reporting columns
- Removes incomplete records when required
- Detects and corrects invalid agency names using a reference list
- Detects and removes negative actual expenses
- Detects and removes abnormal client counts
- Converts and standardizes date formats

## Financial Indicators Created

The script also creates financial performance indicators:

- Actual margin
- Budget margin
- Revenue variance
- Expense variance
- Margin rate

## Project Structure

```text
financial-reporting-automation/
├── data/
│   ├── raw/
│   │   └── financial_reporting_raw.xlsx
│   └── cleaned/
│       ├── financial_reporting_cleaned.xlsx
│       └── financial_reporting.db
├── scripts/
│   ├── clean_financial_data.py
│   ├── create_sqlite_database.py
│   └── run_sql_analysis.py
├── sql/
│   └── 01_financial_analysis_queries.sql
├── powerbi/
├── images/
│   ├── cleaning_summary.png
│   ├── sql_quality_audit.png
│   └── sql_financial_analysis.png
├── README.md
└── requirements.txt
```

## How to Run the Project

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the cleaning script:

```bash
python scripts/clean_financial_data.py
```

The cleaned file is exported to:

```text
data/cleaned/financial_reporting_cleaned.xlsx
```

## Cleaning Summary

The cleaning script produces a final quality control summary after processing the raw dataset.

![Cleaning summary](images/cleaning_summary.png)

## SQL Analysis

After the cleaned Excel file is generated, the project creates a local SQLite database to run SQL audit and financial analysis queries.

The SQLite database is created from:

```text
data/cleaned/financial_reporting_cleaned.xlsx
```

The database file is generated here:

```text
data/cleaned/financial_reporting.db
```

The SQL queries are stored in:

```text
sql/01_financial_analysis_queries.sql
```

The SQL part of the project includes:

- Data quality audit queries
- Duplicate checks
- Missing value checks
- Invalid agency name checks
- Negative expense checks
- Abnormal client count checks
- Revenue analysis by agency
- Margin analysis by agency and activity
- Budget variance analysis
- Monthly revenue trend analysis

To create the SQLite database, run:

```bash
python scripts/create_sqlite_database.py
```

To execute the SQL audit and analysis queries, run:

```bash
python scripts/run_sql_analysis.py
```

## SQL Quality Audit Example

The SQL audit queries verify that no critical data quality issues remain after the Python cleaning process.

![SQL quality audit](images/sql_quality_audit.png)

## SQL Financial Analysis Example

The SQL analysis queries produce financial insights such as revenue by agency, margin by activity and budget variance.

![SQL financial analysis](images/sql_financial_analysis.png)

## Output

The final cleaned dataset contains:

- No duplicate rows
- No missing values in critical fields
- No invalid agency names
- No negative actual expenses
- No abnormal client counts
- Standardized date values
- Financial performance indicators ready for reporting

## Business Value

This project demonstrates how Python and SQL can be used to automate financial data preparation, reduce manual Excel cleaning, improve reporting reliability, and prepare clean datasets for analysis or dashboarding.

The project follows a practical data workflow:

```text
Raw Excel file
→ Python data cleaning
→ Cleaned Excel file
→ SQLite database
→ SQL quality audit
→ SQL financial analysis
```

## Skills Demonstrated

This project demonstrates the ability to:

- Structure a Python data project
- Load and process Excel files with pandas
- Apply data quality checks
- Use business rules to clean financial data
- Create financial indicators
- Export clean datasets for reporting
- Create a SQLite database from cleaned data
- Write SQL audit queries
- Write SQL financial analysis queries
- Prepare data for further analysis in Power BI