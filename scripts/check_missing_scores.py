"""
Sprint 3 - Day 18
Missing Composite Score Debugger

Checks why some companies are not receiving
a composite score.
"""

from pathlib import Path

import pandas as pd

from src.analytics.scorer import CompanyScorer


def main():

    ROOT = Path(__file__).resolve().parents[1]

    DB_PATH = ROOT / "db" / "nifty100.db"

    scorer = CompanyScorer(DB_PATH)

    df = scorer.load_data()

    df = scorer.engine.calculate_composite_score(df)

    missing = df[df["composite_score"].isna()].copy()

    print("\n" + "=" * 80)
    print("COMPANIES WITH MISSING COMPOSITE SCORE")
    print("=" * 80)

    print(f"\nTotal : {len(missing)}")

    if missing.empty:
        print("\nNo missing composite scores found.")
        return

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    columns = [

        "company_id",
        "year",

        "net_profit_margin_pct",
        "return_on_equity_pct",

        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",

        "free_cash_flow_cr",
        "cash_from_operations_cr",

        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",

        "profitability_score",
        "cash_quality_score",
        "growth_score",
        "leverage_score",

        "composite_score",
    ]

    columns = [c for c in columns if c in missing.columns]

    print(missing[columns])

    print("\n" + "=" * 80)
    print("MISSING VALUE COUNT")
    print("=" * 80)

    print(missing[columns].isna().sum())

    print("\n" + "=" * 80)
    print("DEBUG COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()