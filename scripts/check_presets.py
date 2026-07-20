"""
Sprint 3 - Day 16

Preset Validation Script

Runs all implemented preset screeners and
prints company counts and top companies.
"""

from src.screener.presets import PresetScreeners


def display_results(title, df):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Companies Found : {len(df)}")

    if len(df) == 0:
        print("No companies matched.")
        return

    columns = [
        "company_id",
        "year",
        "broad_sector",
        "composite_quality_score"
    ]

    available = [c for c in columns if c in df.columns]

    print(df[available].head(10))


def main():

    screener = PresetScreeners()

    display_results(
        "QUALITY COMPOUNDER",
        screener.quality_compounder()
    )

    display_results(
        "GROWTH ACCELERATOR",
        screener.growth_accelerator()
    )

    display_results(
        "DIVIDEND CHAMPION",
        screener.dividend_champion()
    )

    display_results(
        "DEBT FREE BLUE CHIP",
        screener.debt_free_bluechip()
    )


if __name__ == "__main__":
    main()