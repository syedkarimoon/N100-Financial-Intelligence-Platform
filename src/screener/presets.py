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

    Each preset:
    1. Loads the latest financial ratios.
    2. Defines preset-specific filtering rules.
    3. Passes the DataFrame and filters to ScreenerEngine.
    """

    def __init__(self, db_path="db/nifty100.db"):
        self.engine = ScreenerEngine(db_path)

    # =========================================================
    # 1. QUALITY COMPOUNDER
    # =========================================================

    def quality_compounder(self):
        """
        Quality Compounder

        Criteria:
        - ROE >= 15%
        - D/E <= 1.0
          Financial sector companies are exempt from D/E filtering
          according to the Day 15 screener business rule.
        - FCF > 0
        - Revenue CAGR 5yr >= 10%
        """

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

        return self.engine.apply_filters(
            df,
            filters
        )

    # =========================================================
    # 2. VALUE PICK
    # =========================================================

    def value_pick(self):
        """
        Value Pick

        Intended criteria:
        - P/E < 20
        - P/B < 3.0
        - D/E < 2.0
        - Dividend Yield > 1%

        Current status:
        Required valuation KPIs are not yet available
        in the financial_ratios table.
        """

        raise NotImplementedError(
            "Value Pick requires valuation KPIs "
            "(P/E, P/B, and Dividend Yield) "
            "which are not yet available."
        )

    # =========================================================
    # 3. GROWTH ACCELERATOR
    # =========================================================

    def growth_accelerator(self):
        """
        Growth Accelerator

        Criteria:
        - PAT CAGR 5yr >= 30%
        - Revenue CAGR 5yr >= 15%
        - D/E <= 2.0
          Financial sector companies are exempt from D/E filtering.
        """

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

        return self.engine.apply_filters(
            df,
            filters
        )

    # =========================================================
    # 4. DIVIDEND CHAMPION
    # =========================================================

    def dividend_champion(self):
        """
        Dividend Champion

        Criteria:
        - Dividend Payout Ratio <= 30%
        - FCF > 0

        Note:
        The original Sprint 3 requirement specified
        Dividend Payout < 80%. The current project
        implementation uses <= 30% based on the
        configured preset validation threshold.
        """

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

        return self.engine.apply_filters(
            df,
            filters
        )

    # =========================================================
    # 5. DEBT-FREE BLUE CHIP
    # =========================================================

    def debt_free_bluechip(self):
        """
        Debt-Free Blue Chip

        Criteria:
        - D/E <= 0
          Financial sector companies are exempt from D/E filtering.
        - ROE >= 12%

        Note:
        Revenue > 5000 Crore is not applied here because
        the current financial_ratios data used by the
        preset engine does not contain the required
        revenue column in this implementation.
        """

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

        return self.engine.apply_filters(
            df,
            filters
        )

    # =========================================================
    # 6. TURNAROUND WATCH
    # =========================================================

    def turnaround_watch(self):
        """
        Turnaround Watch

        Intended criteria:
        - Revenue CAGR 3yr > 10%
        - FCF positive in latest year
        - D/E declining year-over-year

        Current status:
        Requires 3-year CAGR and year-over-year D/E
        trend analysis, which are not yet implemented
        in the current Filter Engine.
        """

        raise NotImplementedError(
            "Turnaround Watch requires "
            "3-year Revenue CAGR and "
            "year-over-year D/E trend analysis."
        )