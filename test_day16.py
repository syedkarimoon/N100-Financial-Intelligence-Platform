import pytest

from src.screener.presets import PresetScreeners


def test_quality_compounder():
    screener = PresetScreeners()

    df = screener.quality_compounder()

    assert df is not None
    assert len(df) > 0
    print(f"\nQuality Compounder: {len(df)} companies")


def test_growth_accelerator():
    screener = PresetScreeners()

    df = screener.growth_accelerator()

    assert df is not None
    assert len(df) > 0
    print(f"\nGrowth Accelerator: {len(df)} companies")


def test_dividend_champion():
    screener = PresetScreeners()

    df = screener.dividend_champion()

    assert df is not None
    assert len(df) > 0
    print(f"\nDividend Champion: {len(df)} companies")


def test_debt_free_bluechip():
    screener = PresetScreeners()

    df = screener.debt_free_bluechip()

    assert df is not None
    assert len(df) > 0
    print(f"\nDebt-Free Blue Chip: {len(df)} companies")


def test_value_pick_not_implemented():
    screener = PresetScreeners()

    with pytest.raises(NotImplementedError):
        screener.value_pick()


def test_turnaround_watch_not_implemented():
    screener = PresetScreeners()

    with pytest.raises(NotImplementedError):
        screener.turnaround_watch()