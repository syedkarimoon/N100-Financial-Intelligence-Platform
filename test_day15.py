from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

# Load data
df = engine.load_financial_ratios()

# Apply filters
filtered_df = engine.apply_filters(df)

print("Original rows :", len(df))
print("Filtered rows :", len(filtered_df))

print("\nColumns:")
print(filtered_df.columns.tolist())

print("\nTop 5 Results:")
print(
    filtered_df[
        [
            "company_id",
            "broad_sector",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "composite_quality_score",
        ]
    ].head()
)