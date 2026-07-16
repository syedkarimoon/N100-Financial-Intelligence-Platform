import sqlite3
import os
from datetime import datetime

import pandas as pd


DB_PATH = "db/nifty100.db"
OUTPUT_FILE = "output/ratio_edge_cases.log"


FINANCIAL_SUB_SECTORS = [
    "Consumer Finance",
    "Diversified Financials",
    "General Insurance",
    "Life Insurance",
    "Private Banks",
    "Public Sector Banks"
]


def write_log(message):

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(message + "\n")


def main():

    conn = sqlite3.connect(DB_PATH)


    # clear previous log

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


    write_log(
        "Day 13 Ratio Edge Case Log"
    )

    write_log(
        str(datetime.now())
    )

    write_log(
        "-" * 60
    )


    # ----------------------------
    # Load data
    # ----------------------------

    companies = pd.read_sql(
        """
        SELECT *
        FROM companies
        """,
        conn
    )


    sectors = pd.read_sql(
        """
        SELECT *
        FROM sectors
        """,
        conn
    )


    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    # ----------------------------
    # Financial carve out
    # ----------------------------

    financials = sectors[
        sectors["sub_sector"].isin(
            FINANCIAL_SUB_SECTORS
        )
    ]


    financial_company_ids = set(
        financials["company_id"]
    )


    print(
        "Financial companies:",
        len(financial_company_ids)
    )


    write_log(
        f"Financial carve-out companies: {len(financial_company_ids)}"
    )


    # ----------------------------
    # D/E warning suppression
    # ----------------------------

    debt_flags = ratios[
        [
            "company_id",
            "debt_to_equity"
        ]
    ].copy()


    debt_flags["de_warning"] = (
        debt_flags["debt_to_equity"] > 2
    )


    debt_flags.loc[
        debt_flags.company_id.isin(
            financial_company_ids
        ),
        "de_warning"
    ] = False


    suppressed = debt_flags[
        debt_flags.company_id.isin(
            financial_company_ids
        )
    ]


    write_log(
        f"D/E warning suppressed for {len(suppressed)} Financial companies"
    )


    # ----------------------------
    # ROE Cross Check
    # ----------------------------


    roe_check = ratios.merge(
        companies[
            [
                "id",
                "roe_percentage"
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="inner"
    )


    roe_check["difference"] = (
        roe_check["return_on_equity_pct"]
        -
        roe_check["roe_percentage"]
    ).abs()


    roe_anomaly = roe_check[
        roe_check["difference"] > 5
    ]


    for _, row in roe_anomaly.iterrows():

        write_log(
            f"""
Metric: ROE
Company: {row.company_id}
Engine Value: {row.return_on_equity_pct}
Source Value: {row.roe_percentage}
Difference: {round(row.difference,2)}
Category: Data source issue
"""
        )


    print(
        "ROE anomalies:",
        len(roe_anomaly)
    )


    # ----------------------------
    # ROCE Cross Check
    # ----------------------------

    write_log(
        """
ROCE CHECK
Computed ROCE column not present in financial_ratios.
Pending calculation from balance sheet engine.
Category: Version difference
"""
    )


    print(
        "ROCE check logged"
    )


    conn.close()


    print(
        "Day 13 completed"
    )


if __name__ == "__main__":
    main()