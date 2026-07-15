from src.analytics.growth_score import GrowthScoreEngine
def test_score_cagr_5():
    assert GrowthScoreEngine.score_cagr(25, None) == 5
def test_score_cagr_4():
    assert GrowthScoreEngine.score_cagr(18, None) == 4
def test_score_cagr_3():
    assert GrowthScoreEngine.score_cagr(12, None) == 3
def test_score_cagr_2():
    assert GrowthScoreEngine.score_cagr(8, None) == 2
def test_score_cagr_1():
    assert GrowthScoreEngine.score_cagr(3, None) == 1
def test_score_cagr_negative():
    assert GrowthScoreEngine.score_cagr(-5, None) == 0
def test_score_cagr_flag():
    assert GrowthScoreEngine.score_cagr(None, "TURNAROUND") == 0
def test_revenue_growth_score():
    assert GrowthScoreEngine.revenue_growth_score(25, None) == 5
def test_pat_and_eps_growth_score():
    assert GrowthScoreEngine.pat_growth_score(18, None) == 4
    assert GrowthScoreEngine.eps_growth_score(12, None) == 3
def test_overall_growth_score():
    assert GrowthScoreEngine.overall_growth_score(5, 4, 3) == 4.0
