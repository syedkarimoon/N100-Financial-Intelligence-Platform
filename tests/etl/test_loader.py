import pytest

from config.paths import RAW_DATA_DIR
from src.etl.loader import ExcelLoader


loader = ExcelLoader(RAW_DATA_DIR)


def test_loader_returns_dataframe():
    df = loader.load_excel("balancesheet.xlsx")
    assert df is not None


def test_loader_rows():
    df = loader.load_excel("balancesheet.xlsx")
    assert df.shape[0] > 1000


def test_loader_columns():
    df = loader.load_excel("balancesheet.xlsx")
    assert df.shape[1] == 13


def test_company_column_exists():
    df = loader.load_excel("balancesheet.xlsx")
    assert "company_id" in df.columns


def test_total_assets_exists():
    df = loader.load_excel("balancesheet.xlsx")
    assert "total_assets" in df.columns


def test_duplicate_removed():
    df = loader.load_excel("balancesheet.xlsx")
    assert df.duplicated().sum() == 0


def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        loader.load_excel("dummy.xlsx")