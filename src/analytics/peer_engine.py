"""
Sprint 3 - Day 18
Peer Comparison Engine

Loads peer group assignments and financial metrics,
calculates ROCE, and prepares data for peer percentile rankings.
"""

import sqlite3
from pathlib import Path

import pandas as pd


class PeerComparisonEngine:
    """
    Peer Comparison Engine

    Responsibilities:
    1. Load peer group assignments.
    2. Load financial ratio metrics.
    3. Calculate ROCE using existing project formula.
    4. Merge financial metrics with peer groups.
    5. Calculate peer percentile rankings.
    6. Store results in peer_percentiles table.
    """

    def __init__(
        self,
        db_path="db/nifty100.db",
        peer_groups_path="data/supporting/peer_groups.xlsx"
    ):
        self.db_path = Path(db_path)
        self.peer_groups_path = Path(peer_groups_path)

        self.conn = sqlite3.connect(self.db_path)

    # =========================================================
    # LOAD PEER GROUPS
    # =========================================================

    def load_peer_groups(self):
        """
        Load peer group assignments from Excel.
        """

        if not self.peer_groups_path.exists():
            raise FileNotFoundError(
                f"Peer group file not found: "
                f"{self.peer_groups_path}"
            )

        df = pd.read_excel(self.peer_groups_path)

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        required_columns = {
            "company_id",
            "peer_group_name",
            "is_benchmark"
        }

        missing_columns = (
            required_columns - set(df.columns)
        )

        if missing_columns:
            raise ValueError(
                "Missing peer group columns: "
                f"{missing_columns}"
            )

        return df

    # =========================================================
    # LOAD FINANCIAL RATIOS
    # =========================================================

    def load_financial_ratios(self):
        """
        Load financial metrics required for peer comparison.
        """

        query = """
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            return_on_equity_pct,
            debt_to_equity,
            interest_coverage,
            asset_turnover,
            free_cash_flow_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr
        FROM financial_ratios
        """

        df = pd.read_sql_query(
            query,
            self.conn
        )

        return df

    # =========================================================
    # CALCULATE ROCE
    # =========================================================

    def calculate_roce(self):
        """
        Calculate Return on Capital Employed (ROCE).

        Formula:

        ROCE =
            Operating Profit
            -------------------------------- × 100
            Equity Capital + Reserves + Borrowings

        Uses the same formula defined in src/analytics/ratios.py.
        """

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

        # Calculate capital employed
        df["capital_employed"] = (
            df["equity_capital"].fillna(0)
            + df["reserves"].fillna(0)
            + df["borrowings"].fillna(0)
        )

        # Calculate ROCE safely
        df["return_on_capital_employed_pct"] = None

        valid = df["capital_employed"] > 0

        df.loc[valid, "return_on_capital_employed_pct"] = (
            df.loc[valid, "operating_profit"]
            / df.loc[valid, "capital_employed"]
        ) * 100

        return df[
            [
                "company_id",
                "year",
                "return_on_capital_employed_pct"
            ]
        ]

    # =========================================================
    # PREPARE PEER DATA
    # =========================================================

    def prepare_peer_data(self):
        """
        Combine financial metrics, ROCE and peer groups.
        """

        # Load financial ratios
        financial_data = self.load_financial_ratios()

        # Calculate ROCE
        roce_data = self.calculate_roce()

        # Merge ROCE
        data = financial_data.merge(
            roce_data,
            on=["company_id", "year"],
            how="left"
        )

        # Load peer groups
        peer_groups = self.load_peer_groups()

        # Merge peer groups
        data = data.merge(
            peer_groups[
                [
                    "company_id",
                    "peer_group_name",
                    "is_benchmark"
                ]
            ],
            on="company_id",
            how="left"
        )

        # Find companies without peer groups
        missing_peer_groups = data[
            data["peer_group_name"].isna()
        ]

        if not missing_peer_groups.empty:

            companies = (
                missing_peer_groups["company_id"]
                .drop_duplicates()
                .tolist()
            )

            print(
                "\nNo peer group assigned — "
                f"{len(companies)} company(s)"
            )

            print(
                "Companies:",
                companies
            )

        return data
    # =========================================================
    # CALCULATE PEER PERCENTILE RANKINGS
    # =========================================================

    def calculate_percentiles(self, data):
        """
        Calculate percentile rankings for 10 financial metrics
        within each peer group.

        Higher value = Higher percentile for all metrics
        except D/E.

        For D/E:
            Lower D/E = Higher percentile

            percentile_rank = 1 - normal_percentile
        """

        # -----------------------------------------------------
        # Select latest record for each company
        # -----------------------------------------------------

        data = data.copy()

        # Convert year to sortable date
        data["_year_date"] = pd.to_datetime(
            data["year"],
            errors="coerce"
        )

        # Sort by company and date
        data = data.sort_values(
            [
                "company_id",
                "_year_date"
            ]
        )

        # Keep latest financial record per company
        latest_data = (
            data
            .groupby("company_id", as_index=False)
            .tail(1)
            .copy()
        )

        # -----------------------------------------------------
        # Metrics
        # -----------------------------------------------------

        metrics = {
            "ROE": "return_on_equity_pct",
            "ROCE": "return_on_capital_employed_pct",
            "Net Profit Margin": "net_profit_margin_pct",
            "D/E": "debt_to_equity",
            "FCF": "free_cash_flow_cr",
            "PAT CAGR 5yr": "pat_cagr_5yr",
            "Revenue CAGR 5yr": "revenue_cagr_5yr",
            "EPS CAGR 5yr": "eps_cagr_5yr",
            "Interest Coverage": "interest_coverage",
            "Asset Turnover": "asset_turnover"
        }

        percentile_results = []

        # -----------------------------------------------------
        # Process each metric
        # -----------------------------------------------------

        for metric_name, column_name in metrics.items():

            # Skip if metric does not exist
            if column_name not in latest_data.columns:
                print(
                    f"Warning: Missing metric "
                    f"{column_name}"
                )
                continue

            # Keep only rows with peer groups
            metric_data = latest_data[
                latest_data["peer_group_name"].notna()
            ].copy()

            # Keep only rows with valid metric values
            metric_data = metric_data[
                metric_data[column_name].notna()
            ].copy()

            # -------------------------------------------------
            # Calculate percentile within peer group
            # -------------------------------------------------

            metric_data["percentile_rank"] = (
                metric_data
                .groupby("peer_group_name")[column_name]
                .rank(
                    method="average",
                    pct=True,
                    ascending=True
                )
            )

            # -------------------------------------------------
            # Invert D/E
            # -------------------------------------------------

            if metric_name == "D/E":

                metric_data["percentile_rank"] = (
                    1
                    - metric_data["percentile_rank"]
                )

            # -------------------------------------------------
            # Create result records
            # -------------------------------------------------

            result = pd.DataFrame(
                {
                    "company_id":
                        metric_data["company_id"],

                    "peer_group_name":
                        metric_data["peer_group_name"],

                    "metric":
                        metric_name,

                    "value":
                        metric_data[column_name],

                    "percentile_rank":
                        metric_data["percentile_rank"],

                    "year":
                        metric_data["year"]
                }
            )

            percentile_results.append(result)

        # -----------------------------------------------------
        # Combine all metrics
        # -----------------------------------------------------

        if not percentile_results:

            return pd.DataFrame(
                columns=[
                    "company_id",
                    "peer_group_name",
                    "metric",
                    "value",
                    "percentile_rank",
                    "year"
                ]
            )

        percentile_df = pd.concat(
            percentile_results,
            ignore_index=True
        )

        # Remove helper column
        percentile_df = percentile_df[
            [
                "company_id",
                "peer_group_name",
                "metric",
                "value",
                "percentile_rank",
                "year"
            ]
        ]

        return percentile_df

    # =========================================================
    # CREATE PEER PERCENTILES TABLE
    # =========================================================

    def create_peer_percentiles_table(self):
        """
        Create SQLite table for peer percentile rankings.
        """

        query = """
        CREATE TABLE IF NOT EXISTS peer_percentiles (
            company_id TEXT NOT NULL,
            peer_group_name TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL,
            percentile_rank REAL,
            year TEXT,
            PRIMARY KEY (
                company_id,
                peer_group_name,
                metric,
                year
            )
        )
        """

        self.conn.execute(query)
        self.conn.commit()
    # =========================================================
    # SAVE PEER PERCENTILES
    # =========================================================

    def save_percentiles(self, percentile_df):
        """
        Save peer percentile rankings into SQLite.

        Existing records are replaced to ensure the table
        always contains the latest calculation.
        """

        if percentile_df.empty:
            print(
                "\nNo percentile data to save."
            )
            return

        # Create table if it does not exist
        self.create_peer_percentiles_table()

        # Clear previous results
        self.conn.execute(
            "DELETE FROM peer_percentiles"
        )

        # Insert latest results
        percentile_df.to_sql(
            "peer_percentiles",
            self.conn,
            if_exists="append",
            index=False
        )

        self.conn.commit()

        print(
            "\nPeer percentile results saved successfully."
        )

        print(
            "Rows inserted:",
            len(percentile_df)
        )

    # =========================================================
    # CLOSE CONNECTION
    # =========================================================

    def close(self):
        """
        Close SQLite connection.
        """

        if self.conn:
            self.conn.close()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    engine = PeerComparisonEngine()

    try:

        print("\n" + "=" * 70)
        print("SPRINT 3 - DAY 18")
        print("PEER COMPARISON ENGINE")
        print("=" * 70)

        # -----------------------------------------------------
        # Load Peer Groups
        # -----------------------------------------------------

        peer_groups = engine.load_peer_groups()

        print("\n========== PEER GROUP DATA ==========")

        print(
            peer_groups.head(20).to_string(
                index=False
            )
        )

        print(
            "\nTotal Peer Group Records:",
            len(peer_groups)
        )

        print(
            "Unique Peer Groups:",
            peer_groups["peer_group_name"].nunique()
        )

        # -----------------------------------------------------
        # Calculate ROCE
        # -----------------------------------------------------

        roce = engine.calculate_roce()

        print("\n========== ROCE DATA ==========")

        print(
            roce.head().to_string(
                index=False
            )
        )

        print(
            "\nROCE Records:",
            len(roce)
        )

        print(
            "ROCE Available:",
            roce[
                "return_on_capital_employed_pct"
            ].notna().sum()
        )

        # -----------------------------------------------------
        # Prepare Peer Data
        # -----------------------------------------------------

        data = engine.prepare_peer_data()

        print("\n========== PREPARED PEER DATA ==========")

        print(
            data.head().to_string(
                index=False
            )
        )

        print(
            "\nPrepared Records:",
            len(data)
        )

        print(
            "Companies:",
            data["company_id"].nunique()
        )

        print(
            "Peer Groups:",
            data["peer_group_name"].nunique()
        )

        # -----------------------------------------------------
        # Display Required Metrics
        # -----------------------------------------------------

        required_metrics = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "pat_cagr_5yr",
            "revenue_cagr_5yr",
            "eps_cagr_5yr",
            "interest_coverage",
            "asset_turnover"
        ]

        print(
            "\n========== REQUIRED METRICS =========="
        )

        for metric in required_metrics:

            if metric in data.columns:

                print(
                    f"{metric:<40}"
                    f"Available: "
                    f"{data[metric].notna().sum()}"
                )

            else:

                print(
                    f"{metric:<40}"
                    "MISSING"
                )
                # -----------------------------------------------------
        # Calculate Peer Percentiles
        # -----------------------------------------------------

        percentile_df = engine.calculate_percentiles(
            data
        )
                # -----------------------------------------------------
        # Check Missing Peer Group Companies
        # -----------------------------------------------------

        assigned_companies = set(
            data[
                data["peer_group_name"].notna()
            ]["company_id"].unique()
        )

        ranked_companies = set(
            percentile_df["company_id"].unique()
        )

        not_ranked = (
            assigned_companies
            - ranked_companies
        )

        print(
            "\n========== PEER COMPANIES NOT RANKED =========="
        )

        print(
            "Assigned Peer Companies:",
            len(assigned_companies)
        )

        print(
            "Ranked Companies:",
            len(ranked_companies)
        )

        print(
            "Not Ranked:",
            len(not_ranked)
        )

        if not_ranked:
            print(
                "Companies:",
                sorted(not_ranked)
            )

        print(
            "\n========== PEER PERCENTILE RESULTS =========="
        )

        print(
            percentile_df.head(20).to_string(
                index=False
            )
        )

        print(
            "\nTotal Percentile Records:",
            len(percentile_df)
        )

        print(
            "Companies Ranked:",
            percentile_df["company_id"].nunique()
        )

        print(
            "Metrics Ranked:",
            percentile_df["metric"].nunique()
        )

        print(
            "Peer Groups Ranked:",
            percentile_df["peer_group_name"].nunique()
        )

        print(
            "\nMetric Distribution:"
        )

        print(
            percentile_df["metric"]
            .value_counts()
        )

        # -----------------------------------------------------
        # Validate Percentile Range
        # -----------------------------------------------------

        invalid_percentiles = percentile_df[
            (percentile_df["percentile_rank"] < 0)
            |
            (percentile_df["percentile_rank"] > 1)
        ]

        print(
            "\nInvalid Percentile Values:",
            len(invalid_percentiles)
        )
        
        # -----------------------------------------------------
        # Create Database Table
        # -----------------------------------------------------

        engine.create_peer_percentiles_table()

        print(
            "\npeer_percentiles table ready."
        )
        # -----------------------------------------------------
        # Save Results to SQLite
        # -----------------------------------------------------

        engine.save_percentiles(
            percentile_df
        )

    finally:

        engine.close()