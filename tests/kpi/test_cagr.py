from src.analytics.cagr import CAGREngine


def test_calculate_cagr_normal():
    value, flag = CAGREngine.calculate_cagr(100, 180, 5)

    assert round(value, 2) == 12.47
    assert flag is None

def test_revenue_cagr():
    value, flag = CAGREngine.revenue_cagr(100, 180, 5)

    assert round(value, 2) == 12.47
    assert flag is None

def test_revenue_cagr():
    value, flag = CAGREngine.revenue_cagr(100, 180, 5)

    assert round(value, 2) == 12.47
    assert flag is None

def test_pat_cagr():
    value, flag = CAGREngine.pat_cagr(200, 300, 3)

    assert round(value, 2) == 14.47
    assert flag is None

def test_eps_cagr():
    value, flag = CAGREngine.eps_cagr(10, 20, 10)

    assert round(value, 2) == 7.18
    assert flag is None

def test_calculate_cagr_turnaround():
    value, flag = CAGREngine.calculate_cagr(-100, 100, 5)

    assert value is None
    assert flag == "TURNAROUND"

def test_calculate_cagr_decline_to_loss():
    value, flag = CAGREngine.calculate_cagr(100, -50, 5)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"

def test_calculate_cagr_both_negative():
    value, flag = CAGREngine.calculate_cagr(-100, -50, 5)

    assert value is None
    assert flag == "BOTH_NEGATIVE"

def test_calculate_cagr_zero_base():
    value, flag = CAGREngine.calculate_cagr(0, 100, 5)

    assert value is None
    assert flag == "ZERO_BASE"

def test_calculate_cagr_insufficient():
    value, flag = CAGREngine.calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == "INSUFFICIENT"

def test_calculate_cagr_rounding():
    value, flag = CAGREngine.calculate_cagr(100, 150, 5)

    assert value == round(value, 2)
    assert flag is None
