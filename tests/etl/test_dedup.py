import pandas as pd

from src.etl.normalizer import DataNormalizer


def test_remove_exact_duplicates():
    df = pd.DataFrame({
        "company_id": ["TCS", "TCS"],
        "year": ["2024-03", "2024-03"]
    })

    result = DataNormalizer.remove_duplicates(df)

    assert len(result) == 1


def test_remove_duplicate_subset():
    df = pd.DataFrame({
        "company_id": ["INFY", "INFY", "INFY"],
        "year": ["2023-03", "2023-03", "2024-03"],
        "sales": [100, 100, 120]
    })

    result = DataNormalizer.remove_duplicates(
        df,
        subset=["company_id", "year"]
    )

    assert len(result) == 2


def test_no_duplicates():
    df = pd.DataFrame({
        "company_id": ["TCS", "INFY"],
        "year": ["2024-03", "2024-03"]
    })

    result = DataNormalizer.remove_duplicates(df)

    assert len(result) == 2


def test_empty_dataframe():
    df = pd.DataFrame(columns=["company_id", "year"])

    result = DataNormalizer.remove_duplicates(df)

    assert result.empty


def test_single_row():
    df = pd.DataFrame({
        "company_id": ["SBIN"],
        "year": ["2024-03"]
    })

    result = DataNormalizer.remove_duplicates(df)

    assert len(result) == 1
    