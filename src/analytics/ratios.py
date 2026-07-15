"""
Financial Ratio Engine

Sprint 2 - Day 08
Profitability Ratios

Author: Your Name
"""

from typing import Optional


class FinancialRatioEngine:
    """
    Computes financial ratios for company financial statements.
    """

    @staticmethod
    def safe_divide(numerator: float, denominator: float) -> Optional[float]:
        """
        Safely divide two numbers.

        Returns:
            None if denominator is zero.
        """
        if denominator == 0:
            return None

        return numerator / denominator
    @staticmethod
    def net_profit_margin(
        net_profit: float,
        sales: float
    ) -> Optional[float]:
        """
        Calculate Net Profit Margin (%).

        Formula:
            (Net Profit / Sales) × 100

        Returns:
            None if sales is zero.
        """
        result = FinancialRatioEngine.safe_divide(net_profit, sales)

        if result is None:
            return None

        return result * 100
    @staticmethod
    def operating_profit_margin(
        operating_profit: float,
        sales: float
    ) -> Optional[float]:
        """
        Calculate Operating Profit Margin (%).

        Formula:
            (Operating Profit / Sales) × 100

        Returns:
            None if sales is zero.
        """
        result = FinancialRatioEngine.safe_divide(operating_profit, sales)

        if result is None:
            return None

        return result * 100
    @staticmethod
    def return_on_equity(
        net_profit: float,
        equity_capital: float,
        reserves: float
    ) -> Optional[float]:
        """
        Calculate Return on Equity (ROE).

        Formula:
            Net Profit / (Equity Capital + Reserves) × 100

        Returns:
            None if total equity is less than or equal to zero.
        """
        total_equity = equity_capital + reserves

        if total_equity <= 0:
            return None

        return (net_profit / total_equity) * 100
    @staticmethod
    def return_on_capital_employed(
        ebit: float,
        equity_capital: float,
        reserves: float,
        borrowings: float
    ) -> Optional[float]:
        """
        Calculate Return on Capital Employed (ROCE).

        Formula:
            EBIT / (Equity Capital + Reserves + Borrowings) × 100

        Returns:
            None if capital employed is less than or equal to zero.
        """
        capital_employed = equity_capital + reserves + borrowings

        if capital_employed <= 0:
            return None

        return (ebit / capital_employed) * 100
    @staticmethod
    def return_on_assets(
        net_profit: float,
        total_assets: float
    ) -> Optional[float]:
        """
        Calculate Return on Assets (ROA).

        Formula:
            Net Profit / Total Assets × 100

        Returns:
            None if total assets are less than or equal to zero.
        """
        if total_assets <= 0:
            return None

        return (net_profit / total_assets) * 100
    @staticmethod
    def validate_opm(
        operating_profit: float,
        sales: float,
        source_opm: float
    ) -> dict:
        """
        Validate calculated Operating Profit Margin against source OPM.

        Returns:
            Dictionary containing calculated value, source value,
            difference, and mismatch flag.
        """
        calculated_opm = FinancialRatioEngine.operating_profit_margin(
            operating_profit,
            sales
        )

        if calculated_opm is None:
            return {
                "calculated_opm": None,
                "source_opm": source_opm,
                "difference": None,
                "mismatch": False
            }

        difference = abs(calculated_opm - source_opm)

        return {
            "calculated_opm": round(calculated_opm, 2),
            "source_opm": source_opm,
            "difference": round(difference, 2),
            "mismatch": difference > 1
        }