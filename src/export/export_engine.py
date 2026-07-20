"""
Sprint 3 - Day 17
Export Engine

Creates:
    output/screener_output.xlsx
"""

from pathlib import Path
import sqlite3

import pandas as pd

from src.screener.presets import PresetScreeners


class ExportEngine:

    def __init__(self, db_path):

        self.db_path = Path(db_path)

        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        self.output_file = self.output_dir / "screener_output.xlsx"

        self.presets = PresetScreeners(str(self.db_path))

    # --------------------------------------------------
    # Database Connection
    # --------------------------------------------------

    def connect(self):
        return sqlite3.connect(self.db_path)

    # --------------------------------------------------
    # Load Company Scores
    # --------------------------------------------------

    def load_scores(self):

        conn = self.connect()

        df = pd.read_sql(
            "SELECT * FROM company_scores",
            conn
        )

        conn.close()

        return df

    # --------------------------------------------------
    # Load Financial Ratios
    # --------------------------------------------------

    def load_ratios(self):

        conn = self.connect()

        df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            conn
        )

        conn.close()

        return df

    # --------------------------------------------------
    # Merge Data
    # --------------------------------------------------

    def prepare_export_data(self):

        scores = self.load_scores()
        ratios = self.load_ratios()

        ratios["report_date"] = pd.to_datetime(
            ratios["year"],
            format="%b %Y",
            errors="coerce"
        )

        ratios = (
            ratios.sort_values(
                ["company_id", "report_date"]
            )
            .groupby("company_id", as_index=False)
            .tail(1)
        )

        ratios = ratios.drop(columns=["report_date"])

        df = scores.merge(
            ratios,
            on=["company_id", "year"],
            how="left"
        )

        return df

    # --------------------------------------------------
    # Export Workbook
    # --------------------------------------------------

    def export_excel(self):

        df = self.prepare_export_data()

        export_columns = [

            "overall_rank",
            "company_id",
            "broad_sector",
            "quality_grade",
            "composite_score",

            "profitability_score",
            "cash_quality_score",
            "growth_score",
            "leverage_score",

            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",

            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",

            "earnings_per_share",
            "book_value_per_share",
        ]

        export_columns = [
            c for c in export_columns
            if c in df.columns
        ]

        df = df[export_columns]

        df = df.sort_values(
            "overall_rank"
        )

        with pd.ExcelWriter(
            self.output_file,
            engine="openpyxl"
        ) as writer:

            # Sheet 1
            df.to_excel(
                writer,
                sheet_name="All Companies",
                index=False
            )

            # Sheet 2
            self.presets.quality_compounder().to_excel(
                writer,
                sheet_name="Quality Compounder",
                index=False
            )

            # Sheet 3
            self.presets.growth_accelerator().to_excel(
                writer,
                sheet_name="Growth Accelerator",
                index=False
            )

            # Sheet 4
            self.presets.dividend_champion().to_excel(
                writer,
                sheet_name="Dividend Champion",
                index=False
            )

            # Sheet 5
            self.presets.debt_free_bluechip().to_excel(
                writer,
                sheet_name="Debt Free Blue Chip",
                index=False
            )

        print("\nWorkbook created successfully")
        print(self.output_file)

    # --------------------------------------------------
    # Run
    # --------------------------------------------------

    def run(self):

        self.export_excel()


if __name__ == "__main__":

    ROOT = Path(__file__).resolve().parents[2]

    DB_PATH = ROOT / "db" / "nifty100.db"

    engine = ExportEngine(DB_PATH)

    engine.run()