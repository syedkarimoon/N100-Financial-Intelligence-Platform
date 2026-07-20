import pandas as pd
import numpy as np


class CompositeScoreEngine:
    """
    Composite Quality Score Engine

    Calculates:
        • Profitability Score
        • Cash Quality Score
        • Growth Score
        • Leverage Score

    Final output:
        Composite Score (0–100)
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Winsorization
    # ---------------------------------------------------------

    @staticmethod
    def winsorize(series):
        """
        Cap extreme values using the
        10th and 90th percentiles.
        """

        s = series.copy()

        s = pd.to_numeric(s, errors="coerce")

        p10 = s.quantile(0.10)
        p90 = s.quantile(0.90)

        s = s.clip(
            lower=p10,
            upper=p90
        )

        return s

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    @staticmethod
    def normalize(series, reverse=False):
        """
        Convert values to 0–100 scale.

        reverse=True
            Used for metrics where
            smaller is better
            (Debt/Equity)
        """

        s = CompositeScoreEngine.winsorize(series)

        minimum = s.min()
        maximum = s.max()

        if pd.isna(minimum) or pd.isna(maximum):
            return pd.Series(
                np.zeros(len(s)),
                index=s.index
            )

        if maximum == minimum:
            return pd.Series(
                np.full(len(s), 100),
                index=s.index
            )

        score = (
            (s - minimum)
            /
            (maximum - minimum)
        ) * 100

        if reverse:
            score = 100 - score

        return score.round(2)

    # ---------------------------------------------------------
    # Positive Flag
    # ---------------------------------------------------------

    @staticmethod
    def positive_flag(series):
        """
        Positive values -> 100

        Zero/Negative -> 0
        """

        return np.where(series > 0, 100, 0)

    # ---------------------------------------------------------
    # Safe Division
    # ---------------------------------------------------------

    @staticmethod
    def safe_divide(numerator, denominator):
        """
        Prevent divide-by-zero.
        """

        denominator = denominator.replace(0, np.nan)

        return numerator / denominator
        # ---------------------------------------------------------
    # Profitability Score (35%)
    # ---------------------------------------------------------

    def calculate_profitability_score(self, df):

        roe = self.normalize(df["return_on_equity_pct"])

        npm = self.normalize(df["net_profit_margin_pct"])

        # ROCE not available in current project.
        # Redistribute its 10% weight equally.
        profitability = (
            roe * 0.20 +
            npm * 0.15
        )

        return profitability.round(2)

    # ---------------------------------------------------------
    # Cash Quality Score (30%)
    # ---------------------------------------------------------

    def calculate_cash_quality_score(self, df):

        fcf = self.normalize(df["free_cash_flow_cr"])

        cfo_pat = self.normalize(df["cfo_pat_ratio"])

        fcf_flag = self.positive_flag(
            df["free_cash_flow_cr"]
        )

        cash_score = (
            fcf * 0.15 +
            cfo_pat * 0.10 +
            fcf_flag * 0.05
        )

        return cash_score.round(2)

    # ---------------------------------------------------------
    # Growth Score (20%)
    # ---------------------------------------------------------

    def calculate_growth_score(self, df):

        revenue = self.normalize(
            df["revenue_cagr_5yr"]
        )

        pat = self.normalize(
            df["pat_cagr_5yr"]
        )

        growth = (
            revenue * 0.10 +
            pat * 0.10
        )

        return growth.round(2)

    # ---------------------------------------------------------
    # Leverage Score (15%)
    # ---------------------------------------------------------

    def calculate_leverage_score(self, df):

        debt = self.normalize(
            df["debt_to_equity"],
            reverse=True
        )

        icr = self.normalize(
            df["interest_coverage"]
        )

        leverage = (
            debt * 0.10 +
            icr * 0.05
        )

        return leverage.round(2)

    # ---------------------------------------------------------
    # Composite Score
    # ---------------------------------------------------------

    def calculate_composite_score(self, df):

        data = df.copy()

        # CFO / PAT Ratio
        data["cfo_pat_ratio"] = self.normalize(
            data["cash_from_operations_cr"],
    
        )

        data["profitability_score"] = \
            self.calculate_profitability_score(data)

        data["cash_quality_score"] = \
            self.calculate_cash_quality_score(data)

        data["growth_score"] = \
            self.calculate_growth_score(data)

        data["leverage_score"] = \
            self.calculate_leverage_score(data)

        data["composite_score"] = (
            data["profitability_score"] +
            data["cash_quality_score"] +
            data["growth_score"] +
            data["leverage_score"]
        ).round(2)

        data["composite_score"] = data[
            "composite_score"
        ].clip(
            lower=0,
            upper=100
        )

        return data