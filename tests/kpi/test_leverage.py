from src.analytics.ratios import FinancialRatioEngine
def test_debt_to_equity_normal():
    """
    Test Debt-to-Equity ratio for a normal case.
    """
    result = FinancialRatioEngine.debt_to_equity(
        borrowings=500,
        equity_capital=100,
        reserves=900
    )

    assert result == 0.5

def test_debt_to_equity_debt_free():
    """
    Test Debt-to-Equity when borrowings are zero.
    """
    result = FinancialRatioEngine.debt_to_equity(
        borrowings=0,
        equity_capital=100,
        reserves=900
    )

    assert result == 0   

def test_high_leverage_flag():
    """
    Test High Leverage Flag for a non-financial company.
    """
    result = FinancialRatioEngine.high_leverage_flag(
        debt_to_equity=6.2,
        broad_sector="Industrials"
    )

    assert result is True

def test_high_leverage_flag_financials():
    """
    Test that Financials sector is exempt from High Leverage Flag.
    """
    result = FinancialRatioEngine.high_leverage_flag(
        debt_to_equity=6.2,
        broad_sector="Financials"
    )

    assert result is False

def test_interest_coverage_ratio_interest_zero():
    """
    Test ICR when interest expense is zero.
    """
    result = FinancialRatioEngine.interest_coverage_ratio(
        operating_profit=400,
        other_income=100,
        interest=0
    )

    assert result is None

def test_icr_label_debt_free():
    """
    Test Debt Free label when ICR is None.
    """
    result = FinancialRatioEngine.icr_label(None)

    assert result == "Debt Free"

def test_net_debt():
    """
    Test Net Debt calculation.
    """
    result = FinancialRatioEngine.net_debt(
        borrowings=1000,
        investments=300
    )

    assert result == 700

def test_asset_turnover_zero_assets():
    """
    Test Asset Turnover when total assets are zero.
    """
    result = FinancialRatioEngine.asset_turnover(
        sales=2000,
        total_assets=0
    )

    assert result is None