import pytest

from src.analytics.ratios import FinancialRatioEngine
def test_net_profit_margin_normal():
    """
    Test Net Profit Margin for a normal case.
    """
    result = FinancialRatioEngine.net_profit_margin(
        net_profit=500,
        sales=2000
    )

    assert result == 25.0
def test_net_profit_margin_zero_sales():
    """
    Test Net Profit Margin when sales is zero.
    """
    result = FinancialRatioEngine.net_profit_margin(
        net_profit=500,
        sales=0
    )

    assert result is None
def test_return_on_equity_normal():
    """
    Test Return on Equity for a normal case.
    """
    result = FinancialRatioEngine.return_on_equity(
        net_profit=250,
        equity_capital=100,
        reserves=900
    )

    assert result == 25.0
def test_return_on_equity_negative_equity():
    """
    Test Return on Equity when total equity is negative.
    """
    result = FinancialRatioEngine.return_on_equity(
        net_profit=250,
        equity_capital=100,
        reserves=-200
    )

    assert result is None
def test_return_on_capital_employed_normal():
    """
    Test Return on Capital Employed for a normal case.
    """
    result = FinancialRatioEngine.return_on_capital_employed(
        ebit=300,
        equity_capital=100,
        reserves=900,
        borrowings=500
    )

    assert result == 20.0
def test_return_on_assets_zero_assets():
    """
    Test Return on Assets when total assets are zero.
    """
    result = FinancialRatioEngine.return_on_assets(
        net_profit=500,
        total_assets=0
    )

    assert result is None
def test_validate_opm_match():
    """
    Test OPM validation when calculated and source values match.
    """
    result = FinancialRatioEngine.validate_opm(
        operating_profit=200,
        sales=1000,
        source_opm=20
    )

    assert result["mismatch"] is False
    assert result["difference"] == 0.0
def test_validate_opm_mismatch():
    """
    Test OPM validation when calculated and source values differ.
    """
    result = FinancialRatioEngine.validate_opm(
        operating_profit=200,
        sales=1000,
        source_opm=17
    )

    assert result["mismatch"] is True
    assert result["difference"] == 3.0