"""
ETL Pipeline Module

Handles:
- Loading Excel datasets
- Running data quality validations
- Maintaining load audit information
"""

from pathlib import Path
import pandas as pd

from db.loader import SQLiteLoader
from src.etl.validator import SchemaValidator


class ETLPipeline:
    """
    Main ETL Pipeline Controller
    """

    def __init__(self, data_path="data/raw"):

        self.data_path = Path(data_path)
        self.validator = SchemaValidator()
        self.load_audit = []

    # --------------------------------------------------
    # Load All Excel Files
    # --------------------------------------------------

    def load_excel_files(self):
        """
        Load all Excel datasets from raw folder.
        """

        datasets = {}

        files = {
            "analysis": "analysis.xlsx",
            "balance_sheet": "balancesheet.xlsx",
            "cash_flow": "cashflow.xlsx",
            "companies": "companies.xlsx",
            "documents": "documents.xlsx",
            "profit_and_loss": "profitandloss.xlsx",
            "pros_and_cons": "prosandcons.xlsx"
        }

        for table, file_name in files.items():

            file_path = self.data_path / file_name

            if file_path.exists():

                print(f"Loading {file_name}...")

                df = pd.read_excel(file_path)

                datasets[table] = df

                # Load Audit Record
                self.load_audit.append(
                    {
                        "dataset": table,
                        "filename": file_name,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "status": "SUCCESS"
                    }
                )

                print(
                    f"✓ Loaded {table}: "
                    f"{df.shape[0]} rows × {df.shape[1]} columns"
                )

            else:

                self.load_audit.append(
                    {
                        "dataset": table,
                        "filename": file_name,
                        "rows": 0,
                        "columns": 0,
                        "status": "FAILED"
                    }
                )

                print(f"✗ Missing file: {file_name}")

        return datasets

    # --------------------------------------------------
    # Data Quality Validation
    # --------------------------------------------------

    def run_validations(self, dataframes):
        """
        Execute required DQ validations.
        """

        companies = dataframes.get("companies")

        validation_tables = [
            "balance_sheet",
            "cash_flow",
            "profit_and_loss"
        ]

        for table in validation_tables:

            df = dataframes.get(table)

            if df is None:
                continue

            print(f"Running validations for {table}...")

            if {"company_id", "year"}.issubset(df.columns):

                self.validator.validate_annual_pk(
                    df,
                    table
                )

                self.validator.validate_foreign_key(
                    df,
                    companies,
                    table
                )

                self.validator.validate_year_format(
                    df,
                    table
                )

                self.validator.validate_ticker_format(
                    df,
                    table
                )

            else:

                print(
                    f"Skipping {table}: "
                    "company_id/year columns missing"
                )

        return True

    # --------------------------------------------------
    # Complete Pipeline
    # --------------------------------------------------

    def run_pipeline(self):
        """
        Execute complete ETL pipeline.
        """

        print("Starting ETL Pipeline...")

        # Load all datasets
        dataframes = self.load_excel_files()

        # Run validations
        self.run_validations(dataframes)

        # ---------------------------------------------
        # Load into SQLite Database
        # ---------------------------------------------
        print("Loading data into SQLite database...")

        sqlite_loader = SQLiteLoader()

        for table_name, dataframe in dataframes.items():
            sqlite_loader.load_dataframe(
                dataframe,
                table_name
            )

        print("SQLite database created successfully.")
        print("ETL Pipeline completed successfully")

        return dataframes

    # --------------------------------------------------
    # Test Interface
    # --------------------------------------------------

    def load_all(self):
        """
        Load all datasets.

        Used by ETL tests.
        """

        return self.load_excel_files()

    # --------------------------------------------------
    # Load Audit Access
    # --------------------------------------------------

    def get_load_audit(self):
        """
        Return load audit list.
        """

        return self.load_audit
    