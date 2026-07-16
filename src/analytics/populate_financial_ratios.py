import sqlite3
import pandas as pd

from src.analytics.cagr import CAGREngine
from src.analytics.growth_score import GrowthScoreEngine


def calculate_company_cagr(company_df):
    """
    Calculate 5-year Revenue, PAT and EPS CAGR
    with Composite Quality Score
    """

    company_df = company_df.copy()

    company_id = company_df["company_id"].iloc[0]

    company_df = (
        company_df
        .sort_values("year")
        .reset_index(drop=True)
    )

    company_df["revenue_cagr_5yr"] = None
    company_df["pat_cagr_5yr"] = None
    company_df["eps_cagr_5yr"] = None
    company_df["composite_quality_score"] = None


    for i in range(5, len(company_df)):

        revenue_cagr, revenue_flag = CAGREngine.revenue_cagr(
            company_df.loc[i - 5, "sales"],
            company_df.loc[i, "sales"],
            5
        )


        pat_cagr, pat_flag = CAGREngine.pat_cagr(
            company_df.loc[i - 5, "net_profit"],
            company_df.loc[i, "net_profit"],
            5
        )


        eps_cagr, eps_flag = CAGREngine.eps_cagr(
            company_df.loc[i - 5, "eps"],
            company_df.loc[i, "eps"],
            5
        )


        company_df.loc[i, "revenue_cagr_5yr"] = revenue_cagr
        company_df.loc[i, "pat_cagr_5yr"] = pat_cagr
        company_df.loc[i, "eps_cagr_5yr"] = eps_cagr


        revenue_score = GrowthScoreEngine.revenue_growth_score(
            revenue_cagr,
            revenue_flag
        )

        pat_score = GrowthScoreEngine.pat_growth_score(
            pat_cagr,
            pat_flag
        )

        eps_score = GrowthScoreEngine.eps_growth_score(
            eps_cagr,
            eps_flag
        )


        company_df.loc[i, "composite_quality_score"] = (
            GrowthScoreEngine.overall_growth_score(
                revenue_score,
                pat_score,
                eps_score
            )
        )


    company_df["company_id"] = company_id

    return company_df



def main():

    conn = sqlite3.connect(
        "db/nifty100.db"
    )


    # Load Profit & Loss

    pnl = pd.read_sql(
        """
        SELECT *
        FROM profit_and_loss
        """,
        conn
    )


    print(f"Profit & Loss rows: {len(pnl)}")


    # Cleaning

    pnl = pnl[pnl["year"] != "TTM"]


    pnl = pnl.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )


    print(
        f"Profit & Loss after cleaning: {len(pnl)}"
    )


    # -------------------------------------
    # Calculate CAGR company wise
    # -------------------------------------

    results = []


    for company_id, company_data in pnl.groupby("company_id"):

        company_result = calculate_company_cagr(
            company_data
        )

        results.append(
            company_result
        )


    result = pd.concat(
        results,
        ignore_index=True
    )


    print(
        result.columns.tolist()
    )

    print(
        result.head(10)
    )


    # -------------------------------------
    # Update financial_ratios table
    # -------------------------------------

    update_df = result[
        [
            "company_id",
            "year",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "composite_quality_score"
        ]
    ]


    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    final = ratios.merge(
        update_df,
        on=[
            "company_id",
            "year"
        ],
        how="left",
        suffixes=(
            "",
            "_new"
        )
    )


    for col in [
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"
    ]:

        final[col] = (
            final[f"{col}_new"]
            .combine_first(
                final[col]
            )
        )

        final.drop(
            columns=[f"{col}_new"],
            inplace=True
        )


    # Save back to database

    final.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )


    print(
        "Financial ratios updated successfully"
    )


    # -------------------------------------
    # Verification
    # -------------------------------------

    check = pd.read_sql(
        """
        SELECT
            COUNT(*) AS total_rows,
            COUNT(revenue_cagr_5yr) AS revenue_cagr,
            COUNT(pat_cagr_5yr) AS pat_cagr,
            COUNT(eps_cagr_5yr) AS eps_cagr,
            COUNT(composite_quality_score) AS quality_score
        FROM financial_ratios
        """,
        conn
    )


    print(check)


    conn.close()



if __name__ == "__main__":
    main()