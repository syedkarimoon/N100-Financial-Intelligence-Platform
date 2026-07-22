"""
Sprint 3 - Day 18
Peer Percentile Ranking Validation

Validates the peer_percentiles table in SQLite.
"""

import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    try:

        print("\n" + "=" * 70)
        print("SPRINT 3 - DAY 18")
        print("PEER PERCENTILE RANKING VALIDATION")
        print("=" * 70)

        # -----------------------------------------------------
        # Table Schema
        # -----------------------------------------------------

        print(
            "\n========== TABLE SCHEMA =========="
        )

        schema = conn.execute(
            "PRAGMA table_info(peer_percentiles)"
        ).fetchall()

        for row in schema:
            print(row)

        # -----------------------------------------------------
        # Total Records
        # -----------------------------------------------------

        total_records = conn.execute(
            """
            SELECT COUNT(*)
            FROM peer_percentiles
            """
        ).fetchone()[0]

        print(
            "\nTotal Percentile Records:",
            total_records
        )

        # -----------------------------------------------------
        # Unique Companies
        # -----------------------------------------------------

        unique_companies = conn.execute(
            """
            SELECT COUNT(DISTINCT company_id)
            FROM peer_percentiles
            """
        ).fetchone()[0]

        print(
            "Unique Companies:",
            unique_companies
        )

        # -----------------------------------------------------
        # Unique Peer Groups
        # -----------------------------------------------------

        unique_peer_groups = conn.execute(
            """
            SELECT COUNT(DISTINCT peer_group_name)
            FROM peer_percentiles
            """
        ).fetchone()[0]

        print(
            "Unique Peer Groups:",
            unique_peer_groups
        )

        # -----------------------------------------------------
        # Unique Metrics
        # -----------------------------------------------------

        unique_metrics = conn.execute(
            """
            SELECT COUNT(DISTINCT metric)
            FROM peer_percentiles
            """
        ).fetchone()[0]

        print(
            "Unique Metrics:",
            unique_metrics
        )

        # -----------------------------------------------------
        # Metric Distribution
        # -----------------------------------------------------

        print(
            "\n========== METRIC DISTRIBUTION =========="
        )

        metric_df = pd.read_sql_query(
            """
            SELECT
                metric,
                COUNT(*) AS records
            FROM peer_percentiles
            GROUP BY metric
            ORDER BY metric
            """,
            conn
        )

        print(
            metric_df.to_string(
                index=False
            )
        )

        # -----------------------------------------------------
        # Percentile Range
        # -----------------------------------------------------

        print(
            "\n========== PERCENTILE RANGE =========="
        )

        min_rank, max_rank = conn.execute(
            """
            SELECT
                MIN(percentile_rank),
                MAX(percentile_rank)
            FROM peer_percentiles
            """
        ).fetchone()

        print(
            "Minimum Percentile:",
            min_rank
        )

        print(
            "Maximum Percentile:",
            max_rank
        )

        # -----------------------------------------------------
        # Invalid Percentile Values
        # -----------------------------------------------------

        invalid_percentiles = conn.execute(
            """
            SELECT COUNT(*)
            FROM peer_percentiles
            WHERE percentile_rank < 0
               OR percentile_rank > 1
            """
        ).fetchone()[0]

        print(
            "Invalid Percentiles:",
            invalid_percentiles
        )

        # -----------------------------------------------------
        # D/E Validation
        # -----------------------------------------------------

        print(
            "\n========== D/E PERCENTILE SAMPLE =========="
        )

        de_df = pd.read_sql_query(
            """
            SELECT
                company_id,
                peer_group_name,
                value,
                percentile_rank,
                year
            FROM peer_percentiles
            WHERE metric = 'D/E'
            ORDER BY percentile_rank DESC
            LIMIT 10
            """,
            conn
        )

        print(
            de_df.to_string(
                index=False
            )
        )

        # -----------------------------------------------------
        # Peer Group Distribution
        # -----------------------------------------------------

        print(
            "\n========== PEER GROUP DISTRIBUTION =========="
        )

        peer_df = pd.read_sql_query(
            """
            SELECT
                peer_group_name,
                COUNT(DISTINCT company_id) AS companies,
                COUNT(*) AS percentile_records
            FROM peer_percentiles
            GROUP BY peer_group_name
            ORDER BY peer_group_name
            """,
            conn
        )

        print(
            peer_df.to_string(
                index=False
            )
        )

        # -----------------------------------------------------
        # Final Validation
        # -----------------------------------------------------

        print(
            "\n========== FINAL VALIDATION =========="
        )

        checks = {
            "Table exists":
                len(schema) == 6,

            "10 metrics present":
                unique_metrics == 10,

            "11 peer groups present":
                unique_peer_groups == 11,

            "Percentiles within 0-1":
                invalid_percentiles == 0,

            "Records exist":
                total_records > 0
        }

        all_passed = True

        for check_name, result in checks.items():

            status = "PASS" if result else "FAIL"

            print(
                f"{status:<6} - {check_name}"
            )

            if not result:
                all_passed = False

        print(
            "\n" + "=" * 70
        )

        if all_passed:

            print(
                "DAY 18 PEER PERCENTILE VALIDATION PASSED"
            )

        else:

            print(
                "DAY 18 PEER PERCENTILE VALIDATION FAILED"
            )

        print(
            "=" * 70
        )

    finally:

        conn.close()


if __name__ == "__main__":
    main()