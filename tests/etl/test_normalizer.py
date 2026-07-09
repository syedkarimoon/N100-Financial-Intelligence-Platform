from src.etl.normalizer import DataNormalizer

# ----------------------------------------------------
# normalize_year() Tests (20 Cases)
# ----------------------------------------------------

def test_year_mar_23():
    assert DataNormalizer.normalize_year("Mar-23") == "2023-03"


def test_year_mar_24():
    assert DataNormalizer.normalize_year("Mar-24") == "2024-03"


def test_year_mar_2024():
    assert DataNormalizer.normalize_year("Mar-2024") == "2024-03"


def test_year_dec_23():
    assert DataNormalizer.normalize_year("Dec-23") == "2023-12"


def test_year_dec_2024():
    assert DataNormalizer.normalize_year("Dec-2024") == "2024-12"


def test_year_fy24():
    assert DataNormalizer.normalize_year("FY24") == "2024-03"


def test_year_fy2024():
    assert DataNormalizer.normalize_year("FY2024") == "2024-03"


def test_year_fy_space():
    assert DataNormalizer.normalize_year("FY 2024") == "2024-03"


def test_year_plain():
    assert DataNormalizer.normalize_year("2024") == "2024-03"


def test_year_already_normalized():
    assert DataNormalizer.normalize_year("2024-03") == "2024-03"


def test_year_none():
    assert DataNormalizer.normalize_year(None) is None


def test_year_empty():
    assert DataNormalizer.normalize_year("") is None


def test_year_spaces():
    assert DataNormalizer.normalize_year("   ") is None


def test_year_invalid_text():
    assert DataNormalizer.normalize_year("ABC") is None


def test_year_invalid_month():
    assert DataNormalizer.normalize_year("Jan-24") is None


def test_year_invalid_format():
    assert DataNormalizer.normalize_year("24-FY") is None


def test_year_nan():
    import pandas as pd
    assert DataNormalizer.normalize_year(pd.NA) is None


def test_year_lowercase_mar():
    assert DataNormalizer.normalize_year("mar-23") == "2023-03"


def test_year_lowercase_dec():
    assert DataNormalizer.normalize_year("dec-24") == "2024-12"


def test_year_lowercase_fy():
    assert DataNormalizer.normalize_year("fy24") == "2024-03"
# ----------------------------------------------------
# normalize_ticker() Tests (15 Cases)
# ----------------------------------------------------

def test_ticker_uppercase():
    assert DataNormalizer.normalize_ticker("TCS") == "TCS"


def test_ticker_lowercase():
    assert DataNormalizer.normalize_ticker("tcs") == "TCS"


def test_ticker_spaces():
    assert DataNormalizer.normalize_ticker(" TCS ") == "TCS"


def test_ticker_internal_spaces():
    assert DataNormalizer.normalize_ticker("HDFC BANK") == "HDFCBANK"


def test_ticker_hyphen():
    assert DataNormalizer.normalize_ticker("HDFC-BANK") == "HDFCBANK"


def test_ticker_ns_suffix():
    assert DataNormalizer.normalize_ticker("INFY.NS") == "INFY"


def test_ticker_bo_suffix():
    assert DataNormalizer.normalize_ticker("TCS.BO") == "TCS"


def test_ticker_lower_ns():
    assert DataNormalizer.normalize_ticker("infy.ns") == "INFY"


def test_ticker_lower_bo():
    assert DataNormalizer.normalize_ticker("tcs.bo") == "TCS"


def test_ticker_mixed_case():
    assert DataNormalizer.normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_ticker_blank():
    assert DataNormalizer.normalize_ticker("") is None


def test_ticker_spaces_only():
    assert DataNormalizer.normalize_ticker("    ") is None


def test_ticker_none():
    assert DataNormalizer.normalize_ticker(None) is None


def test_ticker_pandas_na():
    import pandas as pd
    assert DataNormalizer.normalize_ticker(pd.NA) is None


def test_ticker_already_clean():
    assert DataNormalizer.normalize_ticker("SBIN") == "SBIN"