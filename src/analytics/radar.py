"""
Sprint 3 - Day 19
Radar Chart Engine

Generates radar/polar charts for Nifty 100 companies.

For companies with peer groups:
    - Company values shown as filled polygon
    - Peer group average shown as dashed outline

For companies without peer groups:
    - Company values shown as filled polygon
    - Nifty 100 average shown as dashed outline

Output:
    reports/radar_charts/<company_id>_radar.png
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RadarChartEngine:

    def __init__(
        self,
        db_path="db/nifty100.db",
        peer_groups_path="data/supporting/peer_groups.xlsx",
        output_dir="reports/radar_charts"
    ):

        self.db_path = Path(db_path)

        self.peer_groups_path = Path(
            peer_groups_path
        )

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            self.db_path
        )

    # =========================================================
    # LOAD PEER GROUPS
    # =========================================================

    def load_peer_groups(self):

        if not self.peer_groups_path.exists():

            raise FileNotFoundError(
                f"Peer group file not found: "
                f"{self.peer_groups_path}"
            )

        df = pd.read_excel(
            self.peer_groups_path
        )

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(
                " ",
                "_"
            )
        )

        return df[
            [
                "company_id",
                "peer_group_name"
            ]
        ].drop_duplicates(
            subset=["company_id"]
        )

    # =========================================================
    # LOAD FINANCIAL DATA
    # =========================================================

    def load_financial_data(self):

        query = """
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            return_on_equity_pct,
            debt_to_equity,
            free_cash_flow_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr
        FROM financial_ratios
        """

        return pd.read_sql_query(
            query,
            self.conn
        )

    # =========================================================
    # CALCULATE ROCE
    # =========================================================

    def calculate_roce(self):

        query = """
        SELECT
            p.company_id,
            p.year,
            p.operating_profit,
            b.equity_capital,
            b.reserves,
            b.borrowings
        FROM profit_and_loss p

        INNER JOIN balance_sheet b
            ON p.company_id = b.company_id
            AND p.year = b.year
        """

        df = pd.read_sql_query(
            query,
            self.conn
        )

        df["capital_employed"] = (
            df["equity_capital"].fillna(0)
            +
            df["reserves"].fillna(0)
            +
            df["borrowings"].fillna(0)
        )

        valid = (
            df["capital_employed"] > 0
        )

        df["roce"] = np.nan

        df.loc[valid, "roce"] = (
            df.loc[
                valid,
                "operating_profit"
            ]
            /
            df.loc[
                valid,
                "capital_employed"
            ]
        ) * 100

        return df[
            [
                "company_id",
                "year",
                "roce"
            ]
        ]

    # =========================================================
    # LOAD COMPOSITE SCORES
    # =========================================================

    def load_composite_scores(self):

        query = """
        SELECT
            company_id,
            year,
            composite_score
        FROM company_scores
        """

        return pd.read_sql_query(
            query,
            self.conn
        )

    # =========================================================
    # PREPARE DATA
    # =========================================================

    def prepare_data(self):

        financial = (
            self.load_financial_data()
        )

        roce = (
            self.calculate_roce()
        )

        scores = (
            self.load_composite_scores()
        )

        peers = (
            self.load_peer_groups()
        )

        # -----------------------------------------------------
        # Merge ROCE
        # -----------------------------------------------------

        data = financial.merge(
            roce,
            on=[
                "company_id",
                "year"
            ],
            how="left"
        )

        # -----------------------------------------------------
        # Merge Composite Score
        # -----------------------------------------------------

        data = data.merge(
            scores,
            on=[
                "company_id",
                "year"
            ],
            how="left"
        )

        # -----------------------------------------------------
        # Merge Peer Groups
        # -----------------------------------------------------

        data = data.merge(
            peers,
            on="company_id",
            how="left"
        )

        # -----------------------------------------------------
        # Convert Year
        # -----------------------------------------------------

        data["_year_date"] = pd.to_datetime(
            data["year"],
            format="%b %Y",
            errors="coerce"
        )

        # -----------------------------------------------------
        # Select Latest Record
        # -----------------------------------------------------

        data = data.sort_values(
            [
                "company_id",
                "_year_date"
            ]
        )

        data = (
            data
            .groupby(
                "company_id",
                as_index=False
            )
            .tail(1)
            .copy()
        )

        return data

    # =========================================================
    # NORMALIZE METRICS
    # =========================================================

    @staticmethod
    def normalize(
        series,
        reverse=False
    ):

        values = pd.to_numeric(
            series,
            errors="coerce"
        )

        minimum = values.min()
        maximum = values.max()

        if pd.isna(minimum) or pd.isna(maximum):

            return pd.Series(
                50.0,
                index=series.index
            )

        if minimum == maximum:

            return pd.Series(
                100.0,
                index=series.index
            )

        score = (
            (values - minimum)
            /
            (maximum - minimum)
        ) * 100

        if reverse:

            score = (
                100 - score
            )

        return score

    # =========================================================
    # PREPARE RADAR SCORES
    # =========================================================

    def prepare_radar_scores(
        self,
        data
    ):

        data = data.copy()

        # -----------------------------------------------------
        # Normalize radar metrics across Nifty 100
        # -----------------------------------------------------

        data["ROE"] = self.normalize(
            data[
                "return_on_equity_pct"
            ]
        )

        data["ROCE"] = self.normalize(
            data[
                "roce"
            ]
        )

        data["NPM"] = self.normalize(
            data[
                "net_profit_margin_pct"
            ]
        )

        # Lower D/E = Better
        data["D/E"] = self.normalize(
            data[
                "debt_to_equity"
            ],
            reverse=True
        )

        data["FCF Score"] = self.normalize(
            data[
                "free_cash_flow_cr"
            ]
        )

        data["PAT CAGR 5yr"] = self.normalize(
            data[
                "pat_cagr_5yr"
            ]
        )

        data["Revenue CAGR 5yr"] = self.normalize(
            data[
                "revenue_cagr_5yr"
            ]
        )

        # Composite score already 0-100
        data["Composite Score"] = (
            data[
                "composite_score"
            ]
        )

        return data

    # =========================================================
    # GENERATE SINGLE RADAR CHART
    # =========================================================

    def generate_chart(
        self,
        company_row,
        reference_data,
        reference_name
    ):

        axes = [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF Score",
            "PAT CAGR 5yr",
            "Revenue CAGR 5yr",
            "Composite Score"
        ]

        company_values = [
            company_row[
                axis
            ]
            for axis in axes
        ]

        reference_values = [
            reference_data[
                axis
            ]
            for axis in axes
        ]

        # -----------------------------------------------------
        # Radar Angles
        # -----------------------------------------------------

        angles = np.linspace(
            0,
            2 * np.pi,
            len(axes),
            endpoint=False
        ).tolist()

        angles += angles[:1]

        company_values = (
            list(company_values)
            +
            company_values[:1]
        )

        reference_values = (
            list(reference_values)
            +
            reference_values[:1]
        )

        # -----------------------------------------------------
        # Create Figure
        # -----------------------------------------------------

        fig, ax = plt.subplots(
            figsize=(10, 10),
            subplot_kw={
                "polar": True
            }
        )

        # -----------------------------------------------------
        # Company Polygon
        # -----------------------------------------------------

        ax.plot(
            angles,
            company_values,
            linewidth=2,
            label=company_row[
                "company_id"
            ]
        )

        ax.fill(
            angles,
            company_values,
            alpha=0.25
        )

        # -----------------------------------------------------
        # Reference Outline
        # -----------------------------------------------------

        ax.plot(
            angles,
            reference_values,
            linestyle="--",
            linewidth=2,
            label=reference_name
        )

        # -----------------------------------------------------
        # Axis Labels
        # -----------------------------------------------------

        ax.set_xticks(
            angles[:-1]
        )

        ax.set_xticklabels(
            axes,
            fontsize=11
        )

        # -----------------------------------------------------
        # Y Axis
        # -----------------------------------------------------

        ax.set_ylim(
            0,
            100
        )

        ax.set_yticks(
            [
                20,
                40,
                60,
                80,
                100
            ]
        )

        ax.set_yticklabels(
            [
                "20",
                "40",
                "60",
                "80",
                "100"
            ],
            fontsize=9
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        peer_group = (
            company_row[
                "peer_group_name"
            ]
            if pd.notna(
                company_row[
                    "peer_group_name"
                ]
            )
            else "No Peer Group"
        )

        ax.set_title(
            (
                f"{company_row['company_id']} "
                f"— Financial Radar\n"
                f"Peer Group: {peer_group}"
            ),
            fontsize=15,
            fontweight="bold",
            pad=25
        )

        # -----------------------------------------------------
        # Legend
        # -----------------------------------------------------

        ax.legend(
            loc="upper right",
            bbox_to_anchor=(
                1.25,
                1.10
            ),
            fontsize=10
        )

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

        company_id = (
            company_row[
                "company_id"
            ]
        )

        output_path = (
            self.output_dir
            /
            f"{company_id}_radar.png"
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

        return output_path

    # =========================================================
    # GENERATE ALL RADAR CHARTS
    # =========================================================

    def generate_all_charts(self):

        data = (
            self.prepare_data()
        )

        data = (
            self.prepare_radar_scores(
                data
            )
        )

        axes = [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF Score",
            "PAT CAGR 5yr",
            "Revenue CAGR 5yr",
            "Composite Score"
        ]

        generated = []

        # -----------------------------------------------------
        # Generate Chart Per Company
        # -----------------------------------------------------

        for _, company in data.iterrows():

            peer_group = (
                company[
                    "peer_group_name"
                ]
            )

            # -------------------------------------------------
            # Peer Group Reference
            # -------------------------------------------------

            if pd.notna(
                peer_group
            ):

                peers = data[
                    data[
                        "peer_group_name"
                    ]
                    ==
                    peer_group
                ]

                reference = (
                    peers[
                        axes
                    ]
                    .mean()
                )

                reference_name = (
                    f"{peer_group} Average"
                )

            # -------------------------------------------------
            # Nifty 100 Reference
            # -------------------------------------------------

            else:

                reference = (
                    data[
                        axes
                    ]
                    .mean()
                )

                reference_name = (
                    "Nifty 100 Average"
                )

            # -------------------------------------------------
            # Generate Chart
            # -------------------------------------------------

            output_path = (
                self.generate_chart(
                    company,
                    reference,
                    reference_name
                )
            )

            generated.append(
                output_path
            )

        return generated

    # =========================================================
    # CLOSE DATABASE
    # =========================================================

    def close(self):

        self.conn.close()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    engine = RadarChartEngine()

    try:

        print(
            "\n"
            + "=" * 70
        )

        print(
            "SPRINT 3 - DAY 19"
        )

        print(
            "RADAR CHART GENERATION"
        )

        print(
            "=" * 70
        )

        charts = (
            engine.generate_all_charts()
        )

        print(
            "\n========== RADAR CHART SUMMARY =========="
        )

        print(
            "Charts Generated:",
            len(charts)
        )

        print(
            "Output Directory:",
            engine.output_dir
        )

        print(
            "\nSample Files:"
        )

        for path in charts[:10]:

            print(
                path
            )

        print(
            "\nRadar chart generation completed successfully."
        )

    finally:

        engine.close()