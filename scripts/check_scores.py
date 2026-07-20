"""
Sprint 3 - Day 17
Company Score Validation

Runs the CompanyScorer and validates:

1. Companies scored
2. Score range
3. Grade distribution
4. Ranking
5. Sector ranking
6. Summary statistics
"""

from pathlib import Path

from src.analytics.scorer import CompanyScorer


def main():

    root = Path(__file__).resolve().parents[1]

    db_path = root / "db" / "nifty100.db"

    scorer = CompanyScorer(db_path)

    df = scorer.run()

    print("\n" + "=" * 60)
    print("COMPANY SCORE VALIDATION")
    print("=" * 60)

    # --------------------------------------------------
    # Basic Statistics
    # --------------------------------------------------

    print(f"\nCompanies Scored : {len(df)}")

    print("\nComposite Score Statistics")
    print("-" * 35)

    print(f"Minimum : {df['composite_score'].min():.2f}")
    print(f"Maximum : {df['composite_score'].max():.2f}")
    print(f"Average : {df['composite_score'].mean():.2f}")

    # --------------------------------------------------
    # Grade Distribution
    # --------------------------------------------------

    print("\nGrade Distribution")
    print("-" * 35)

    print(df["quality_grade"].value_counts().sort_index())

    # --------------------------------------------------
    # Top 10
    # --------------------------------------------------

    print("\nTop 10 Companies")
    print("-" * 35)

    print(
        df[
            [
                "overall_rank",
                "company_id",
                "composite_score",
                "quality_grade",
            ]
        ].head(10)
    )

    # --------------------------------------------------
    # Bottom 10
    # --------------------------------------------------

    print("\nBottom 10 Companies")
    print("-" * 35)

    print(
        df[
            [
                "overall_rank",
                "company_id",
                "composite_score",
                "quality_grade",
            ]
        ].tail(10)
    )

    # --------------------------------------------------
    # Sector Leaders
    # --------------------------------------------------

    if "broad_sector" in df.columns:

        print("\nTop Company in Each Sector")
        print("-" * 35)

        leaders = (
            df.sort_values("sector_rank")
              .groupby("broad_sector")
              .head(1)
        )

        print(
            leaders[
                [
                    "broad_sector",
                    "company_id",
                    "composite_score",
                    "sector_rank",
                ]
            ]
        )

    # --------------------------------------------------
    # Validation Checks
    # --------------------------------------------------

    print("\nValidation Checks")
    print("-" * 35)

    if df["composite_score"].between(0, 100).all():
        print("PASS : Composite scores are between 0 and 100")
    else:
        print("FAIL : Invalid composite score found")

    if df["overall_rank"].isna().sum() == 0:
        print("PASS : Overall ranking generated")
    else:
        print("FAIL : Missing overall rank")

    if "sector_rank" in df.columns:

        if df["sector_rank"].isna().sum() == 0:
            print("PASS : Sector ranking generated")
        else:
            print("FAIL : Missing sector rank")

    if df["company_id"].duplicated().sum() == 0:
        print("PASS : No duplicate companies")
    else:
        print("FAIL : Duplicate companies found")

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    root = Path(__file__).resolve().parents[1]

    db_path = root / "db" / "nifty100.db"

    scorer = CompanyScorer(db_path)

    df = scorer.run()

    print("\n" + "=" * 60)
    print("COMPANY SCORE VALIDATION")
    print("=" * 60)

    print(f"\nCompanies Scored : {len(df)}")

    print("\nComposite Score Statistics")
    print("-" * 35)
    print(f"Minimum : {df['composite_score'].min():.2f}")
    print(f"Maximum : {df['composite_score'].max():.2f}")
    print(f"Average : {df['composite_score'].mean():.2f}")

    print("\nGrade Distribution")
    print("-" * 35)
    print(df["quality_grade"].value_counts().sort_index())

    print("\nTop 10 Companies")
    print("-" * 35)
    print(
        df[
            [
                "overall_rank",
                "company_id",
                "composite_score",
                "quality_grade",
            ]
        ].head(10)
    )

    print("\nBottom 10 Companies")
    print("-" * 35)
    print(
        df[
            [
                "overall_rank",
                "company_id",
                "composite_score",
                "quality_grade",
            ]
        ].tail(10)
    )

    print("\nValidation Checks")
    print("-" * 35)

    print(
        "PASS : Composite scores are between 0 and 100"
        if df["composite_score"].between(0, 100).all()
        else "FAIL : Invalid composite score found"
    )

    print(
        "PASS : Overall ranking generated"
        if df["overall_rank"].isna().sum() == 0
        else "FAIL : Missing overall rank"
    )

    if "sector_rank" in df.columns:
        print(
            "PASS : Sector ranking generated"
            if df["sector_rank"].isna().sum() == 0
            else "FAIL : Missing sector rank"
        )

    print(
        "PASS : No duplicate companies"
        if df["company_id"].duplicated().sum() == 0
        else "FAIL : Duplicate companies found"
    )

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETED")
    print("=" * 60)