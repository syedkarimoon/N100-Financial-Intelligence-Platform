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
from src.etl.loader import ExcelLoader
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
        Load all Excel datasets from raw and supporting folders.
        """

        datasets = {}

        raw_path = Path("data/raw")
        supporting_path = Path("data/supporting")

        files = {

            # Core datasets
            "analysis": (raw_path, "analysis.xlsx"),
            "balance_sheet": (raw_path, "balancesheet.xlsx"),
            "cash_flow": (raw_path, "cashflow.xlsx"),
            "companies": (raw_path, "companies.xlsx"),
            "documents": (raw_path, "documents.xlsx"),
            "profit_and_loss": (raw_path, "profitandloss.xlsx"),
            "pros_and_cons": (raw_path, "prosandcons.xlsx"),

            # Supporting datasets
            "financial_ratios": (supporting_path, "financial_ratios.xlsx"),
            "market_cap": (supporting_path, "market_cap.xlsx"),
            "peer_groups": (supporting_path, "peer_groups.xlsx"),
            "sectors": (supporting_path, "sectors.xlsx"),
            "stock_prices": (supporting_path, "stock_prices.xlsx")

        }

        for table, (folder, file_name) in files.items():

            print(f"Loading {file_name}...")

            try:

                loader = ExcelLoader(folder)
                df = loader.load_excel(file_name)

                datasets[table] = df

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

            except FileNotFoundError:

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

                self.validator.validate_annual_pk(df, table)

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

                print(f"✓ Validation completed for {table}")

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

        # Load datasets
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

        # ---------------------------------------------
        # Create outputs folder
        # ---------------------------------------------

        Path("outputs").mkdir(
            exist_ok=True
        )

        # ---------------------------------------------
        # Export Load Audit
        # ---------------------------------------------

        audit_df = pd.DataFrame(self.load_audit)

        audit_df.to_csv(
            "outputs/load_audit.csv",
            index=False
        )

        print(
            "✓ Load audit saved to outputs/load_audit.csv"
        )

        # ---------------------------------------------
        # Export Validation Failures
        # ---------------------------------------------

        self.validator.export_failures(
            "outputs/validation_failures.csv"
        )

        print(
            "✓ Validation failures saved to outputs/validation_failures.csv"
        )

        print("ETL Pipeline completed successfully")

        return dataframes