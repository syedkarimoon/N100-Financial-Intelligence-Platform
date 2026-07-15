from src.analytics.cashflow import CashFlowEngine
def test_free_cash_flow():
    assert CashFlowEngine.free_cash_flow(1000, -300) == 700
def test_free_cash_flow_negative():
    assert CashFlowEngine.free_cash_flow(200, -500) == -300
def test_cfo_quality_high():
    ratio, quality = CashFlowEngine.cfo_quality_score(
        [100, 120, 130, 140, 150],
        [80, 100, 110, 120, 130]
    )

    assert ratio > 1.0
    assert quality == "High Quality"
def test_cfo_quality_moderate():
    ratio, quality = CashFlowEngine.cfo_quality_score(
        [60, 70, 80, 90, 100],
        [100, 100, 100, 100, 100]
    )

    assert 0.5 <= ratio <= 1.0
    assert quality == "Moderate"
def test_cfo_quality_accrual_risk():
    ratio, quality = CashFlowEngine.cfo_quality_score(
        [20, 30, 40, 30, 20],
        [100, 100, 100, 100, 100]
    )

    assert ratio < 0.5
    assert quality == "Accrual Risk"
def test_cfo_quality_pat_zero():
    ratio, quality = CashFlowEngine.cfo_quality_score(
        [100, 120, 130, 140, 150],
        [100, 100, 0, 100, 100]
    )

    assert ratio is None
    assert quality is None
def test_capex_asset_light():
    value, category = CashFlowEngine.capex_intensity(-20, 1000)

    assert value == 2.0
    assert category == "Asset Light"
def test_capex_moderate():
    value, category = CashFlowEngine.capex_intensity(-50, 1000)

    assert value == 5.0
    assert category == "Moderate"
def test_capex_capital_intensive():
    value, category = CashFlowEngine.capex_intensity(-120, 1000)

    assert value == 12.0
    assert category == "Capital Intensive"

def test_fcf_conversion_rate():
    assert CashFlowEngine.fcf_conversion_rate(700, 1000) == 70.0
def test_fcf_conversion_zero_operating_profit():
    assert CashFlowEngine.fcf_conversion_rate(700, 0) is None

def test_pattern_reinvestor():
    assert CashFlowEngine.capital_allocation_pattern(
        100, -50, -20
    ) == ("+", "-", "-", "Reinvestor")
def test_pattern_shareholder_returns():
    assert CashFlowEngine.capital_allocation_pattern(
        100, -50, -20,
        "High Quality"
    ) == ("+", "-", "-", "Shareholder Returns")

def test_pattern_liquidating_assets():
    assert CashFlowEngine.capital_allocation_pattern(
        100, 50, -20
    ) == ("+", "+", "-", "Liquidating Assets")
def test_pattern_distress():
    assert CashFlowEngine.capital_allocation_pattern(
        -100, 50, 20
    ) == ("-", "+", "+", "Distress Signal")
def test_pattern_growth_debt():
    assert CashFlowEngine.capital_allocation_pattern(
        -100, -50, 20
    ) == ("-", "-", "+", "Growth Funded by Debt")
def test_pattern_cash_accumulator():
    assert CashFlowEngine.capital_allocation_pattern(
        100, 50, 20
    ) == ("+", "+", "+", "Cash Accumulator")
def test_pattern_pre_revenue():
    assert CashFlowEngine.capital_allocation_pattern(
        -100, -50, -20
    ) == ("-", "-", "-", "Pre-Revenue")
def test_pattern_mixed():
    assert CashFlowEngine.capital_allocation_pattern(
        100, -50, 20
    ) == ("+", "-", "+", "Mixed")
