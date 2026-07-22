"""
Sprint 3 - Day 17
Company Scoring Engine

Loads latest financial ratios,
calculates composite scores,
generates rankings,
and stores results.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.analytics.composite_score import CompositeScoreEngine


class CompanyScorer:

    def __init__(self, db_path):

        self.db_path = Path(db_path)

        self.engine = CompositeScoreEngine()

    # --------------------------------------------------
    # Database Connection
    # --------------------------------------------------

    def connect(self):

        return sqlite3.connect(self.db_path)

    # --------------------------------------------------
    # Load Latest Record of Every Company
    # --------------------------------------------------

    def load_data(self):

        conn = self.connect()

        query = """
        SELECT *
        FROM financial_ratios
        """

        df = pd.read_sql(query, conn)

        conn.close()

        if df.empty:
            raise ValueError("financial_ratios table is empty.")

        print(f"\nTotal Financial Ratio Records : {len(df)}")

        # Convert report period into date
        df["report_date"] = pd.to_datetime(
            df["year"],
            format="%b %Y",
            errors="coerce"
        )

        # Latest record of each company
        df = (
            df.sort_values(["company_id", "report_date"])
              .groupby("company_id", as_index=False)
              .tail(1)
              .reset_index(drop=True)
        )

        print(f"Latest Company Records : {len(df)}")

        # Remove helper column
        df.drop(columns=["report_date"], inplace=True)

        return df

    # --------------------------------------------------
    # Grade
    # --------------------------------------------------

    @staticmethod
    def assign_grade(score):

        if score >= 85:
            return "A+"

        elif score >= 75:
            return "A"

        elif score >= 65:
            return "B+"

        elif score >= 55:
            return "B"

        elif score >= 45:
            return "C"

        return "D"

    # --------------------------------------------------
    # Overall Rank
    # --------------------------------------------------

    @staticmethod
    def overall_rank(df):

        df["overall_rank"] = (
            df["composite_score"]
            .rank(
                ascending=False,
                method="dense"
            )
        )

        return df

    # --------------------------------------------------
    # Sector Rank
    # --------------------------------------------------

    @staticmethod
    def sector_rank(df):

        if "broad_sector" not in df.columns:
            return df

        df["sector_rank"] = (
            df.groupby("broad_sector")["composite_score"]
            .rank(
                ascending=False,
                method="dense"
            )
        )

        return df
        # --------------------------------------------------
    # Percentile
    # --------------------------------------------------

    @staticmethod
    def calculate_percentile(df):

        df["percentile"] = (
            df["composite_score"]
            .rank(pct=True)
            * 100
        )

        return df

    # --------------------------------------------------
    # Save Results
    # --------------------------------------------------

    def save_results(self, df):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_scores(

            company_id TEXT,
            year TEXT,

            profitability_score REAL,
            cash_quality_score REAL,
            growth_score REAL,
            leverage_score REAL,

            composite_score REAL,

            quality_grade TEXT,

            overall_rank INTEGER,
            sector_rank INTEGER,

            percentile REAL,

            PRIMARY KEY(company_id, year)
        )
        """)

        # Remove previous results for the same reporting periods
        periods = df["year"].unique().tolist()

        for period in periods:
            cursor.execute(
                "DELETE FROM company_scores WHERE year=?",
                (period,)
            )

        save_df = df.copy()

        # Convert ranks safely
        save_df["overall_rank"] = (
            save_df["overall_rank"]
            .fillna(0)
            .astype(int)
        )

        if "sector_rank" in save_df.columns:
            save_df["sector_rank"] = (
                save_df["sector_rank"]
                .fillna(0)
                .astype(int)
            )
        else:
            save_df["sector_rank"] = 0

        save_df.to_sql(
            "company_scores",
            conn,
            if_exists="append",
            index=False
        )

        conn.commit()
        conn.close()

    # --------------------------------------------------
    # Display Summary
    # --------------------------------------------------

    @staticmethod
    def summary(df):

        print("\n" + "=" * 60)
        print("COMPANY SCORING SUMMARY")
        print("=" * 60)

        print(f"Companies : {len(df)}")

        print(
            f"Average Score : {df['composite_score'].mean():.2f}"
        )

        print(
            f"Highest Score : {df['composite_score'].max():.2f}"
        )

        print(
            f"Lowest Score : {df['composite_score'].min():.2f}"
        )

        print("\nGrade Distribution")

        print(
            df["quality_grade"]
            .value_counts()
            .sort_index()
        )

        print("=" * 60)
    # --------------------------------------------------
    # Main Pipeline
    # --------------------------------------------------

    def run(self):

        # Load latest record for every company
        df = self.load_data()
        
        print("\n========== DEBUG COLUMNS ==========")
        print(df.columns.tolist())
        print("===================================")
        
        df = self.engine.calculate_composite_score(df)
        missing = df[df["composite_score"].isna()]

        if not missing.empty:
           print("\nCompanies with missing composite scores:")
           print(
                missing[
                  ["company_id", "year"]
               ]
        )
        # Remove companies where score could not be calculated
        df = df.dropna(subset=["composite_score"]).copy()

        # Generate grades
        df["quality_grade"] = (
            df["composite_score"]
            .apply(self.assign_grade)
        )

        # Rankings
        df = self.overall_rank(df)
        df = self.sector_rank(df)
        df = self.calculate_percentile(df)

        # Convert ranks to integers
        df["overall_rank"] = df["overall_rank"].astype(int)

        if "sector_rank" in df.columns:
            df["sector_rank"] = (
                df["sector_rank"]
                .fillna(0)
                .astype(int)
            )

        # Sort by score
        df = (
            df.sort_values(
                "overall_rank"
            )
            .reset_index(drop=True)
        )

        # Keep useful columns only
        columns = [
            "company_id",
            "year",
            "profitability_score",
            "cash_quality_score",
            "growth_score",
            "leverage_score",
            "composite_score",
            "quality_grade",
            "overall_rank",
            "sector_rank",
            "percentile",
        ]

        columns = [
            c for c in columns
            if c in df.columns
        ]

        df = df[columns]

        # Save
        self.save_results(df)

        # Print summary
        self.summary(df)

        return df


# --------------------------------------------------
# Standalone Execution
# --------------------------------------------------

if __name__ == "__main__":

    ROOT = Path(__file__).resolve().parents[2]

    DB_PATH = ROOT / "db" / "nifty100.db"

    scorer = CompanyScorer(DB_PATH)

    result = scorer.run()

    print("\nTop 20 Companies")
    print("-" * 60)

    print(
        result[
            [
                "overall_rank",
                "company_id",
                "composite_score",
                "quality_grade",
            ]
        ].head(20)
    )