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
    @staticmethod
    def debt_to_equity(
        borrowings: float,
        equity_capital: float,
        reserves: float
    ) -> Optional[float]:
        """
        Calculate Debt-to-Equity Ratio.

        Formula:
            Borrowings / (Equity Capital + Reserves)

        Returns:
            0 if borrowings are zero.
            None if total equity is less than or equal to zero.
        """
        if borrowings == 0:
            return 0

        total_equity = equity_capital + reserves

        if total_equity <= 0:
            return None

        return borrowings / total_equity
    @staticmethod
    def high_leverage_flag(
        debt_to_equity: Optional[float],
        broad_sector: str
    ) -> bool:
        """
        Determine whether a company has high leverage.

        Returns:
            True if D/E > 5 and company is not in Financials.
            Otherwise False.
        """
        if debt_to_equity is None:
            return False

        if broad_sector.strip().lower() == "financials":
            return False

        return debt_to_equity > 5
    @staticmethod
    def interest_coverage_ratio(
        operating_profit: float,
        other_income: float,
        interest: float
    ) -> Optional[float]:
        """
        Calculate Interest Coverage Ratio (ICR).

        Formula:
            (Operating Profit + Other Income) / Interest

        Returns:
            None if interest is zero.
        """
        if interest == 0:
            return None

        return (operating_profit + other_income) / interest
    @staticmethod
    def icr_label(icr: Optional[float]) -> Optional[str]:
        """
        Return display label for Interest Coverage Ratio.

        Returns:
            "Debt Free" if ICR is None.
            Otherwise None.
        """
        if icr is None:
            return "Debt Free"

        return None
    @staticmethod
    def icr_warning_flag(icr: Optional[float]) -> bool:
        """
        Determine whether Interest Coverage Ratio indicates risk.

        Returns:
            True if ICR < 1.5
            False otherwise
        """
        if icr is None:
            return False

        return icr < 1.5
    @staticmethod
    def net_debt(
        borrowings: float,
        investments: float
    ) -> float:
        """
        Calculate Net Debt.

        Formula:
            Borrowings - Investments
        """
        return borrowings - investments
        
    @staticmethod
    def asset_turnover(
        sales: float,
        total_assets: float
    ) -> Optional[float]:
        """
        Calculate Asset Turnover Ratio.

        Formula:
            Sales / Total Assets

        Returns:
            None if total assets are less than or equal to zero.
        """
        if total_assets <= 0:
            return None

        return sales / total_assets