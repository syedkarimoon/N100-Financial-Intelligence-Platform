"""
Preset Screeners
Sprint 3 - Day 16

Provides predefined stock screening strategies
using the Filter Engine.
"""

from src.screener.engine import ScreenerEngine


class PresetScreeners:
    """
    Collection of predefined stock screeners.
    """

    def __init__(self, db_path="db/nifty100.db"):
        self.engine = ScreenerEngine(db_path)

    # ---------------------------------------------------------
    # 1. Quality Compounder
    # ---------------------------------------------------------
    def quality_compounder(self):

        df = self.engine.load_financial_ratios()

        filters = {
            "roe": {
                "column": "return_on_equity_pct",
                "operator": ">=",
                "value": 15
            },
            "debt": {
                "column": "debt_to_equity",
                "operator": "<=",
                "value": 1.0
            },
            "fcf": {
                "column": "free_cash_flow_cr",
                "operator": ">",
                "value": 0
            },
            "revenue_cagr": {
                "column": "revenue_cagr_5yr",
                "operator": ">=",
                "value": 10
            }
        }

        return self.engine.apply_filters(df, filters)

    # ---------------------------------------------------------
    # 2. Value Pick
    # ---------------------------------------------------------
    def value_pick(self):
        """
        Requires valuation KPIs
        (P/E, P/B, Dividend Yield)
        """

        raise NotImplementedError(
            "Value Pick requires valuation KPIs which are not yet available."
        )

    # ---------------------------------------------------------
    # 3. Growth Accelerator
    # ---------------------------------------------------------
    def growth_accelerator(self):

        df = self.engine.load_financial_ratios()

        filters = {
            "pat_cagr": {
                "column": "pat_cagr_5yr",
                "operator": ">=",
                "value": 30
            },
            "revenue_cagr": {
                "column": "revenue_cagr_5yr",
                "operator": ">=",
                "value": 15
            },
            "debt": {
                "column": "debt_to_equity",
                "operator": "<=",
                "value": 2.0
            }
        }

        return self.engine.apply_filters(df, filters)

    # ---------------------------------------------------------
    # 4. Dividend Champion
    # ---------------------------------------------------------
    def dividend_champion(self):

        df = self.engine.load_financial_ratios()

        filters = {
            "dividend_payout": {
                "column": "dividend_payout_ratio_pct",
                "operator": "<=",
                "value": 30
            },
            "fcf": {
                "column": "free_cash_flow_cr",
                "operator": ">",
                "value": 0
            }
        }

        return self.engine.apply_filters(df, filters)

    # ---------------------------------------------------------
    # 5. Debt-Free Blue Chip
    # ---------------------------------------------------------
    def debt_free_bluechip(self):

        df = self.engine.load_financial_ratios()

        filters = {
            "debt": {
                "column": "debt_to_equity",
                "operator": "<=",
                "value": 0
            },
            "roe": {
                "column": "return_on_equity_pct",
                "operator": ">=",
                "value": 12
            }
        }

        return self.engine.apply_filters(df, filters)

    # ---------------------------------------------------------
    # 6. Turnaround Watch
    # ---------------------------------------------------------
    def turnaround_watch(self):
        """
        Requires:
        - Revenue CAGR (3Y)
        - Debt-to-Equity trend analysis
        """

        raise NotImplementedError(
            "Turnaround Watch requires 3-year CAGR and D/E trend analysis."
        )