import pandas as pd
import numpy as np


class CompositeScoreEngine:
    """
    Composite Quality Score Engine

    Calculates:

    1. Profitability Score (35%)
        - ROE
        - Net Profit Margin

    2. Cash Quality Score (30%)
        - Free Cash Flow
        - CFO/PAT Ratio
        - Positive FCF Flag

    3. Growth Score (20%)
        - Revenue CAGR
        - PAT CAGR

    4. Leverage Score (15%)
        - Debt/Equity
        - Interest Coverage

    Final Output:
        Composite Score (0-100)
    """

    # ---------------------------------------------------------
    # Winsorization
    # ---------------------------------------------------------

    @staticmethod
    def winsorize(series):

        s = pd.to_numeric(
            series,
            errors="coerce"
        )

        p10 = s.quantile(0.10)
        p90 = s.quantile(0.90)

        return s.clip(
            lower=p10,
            upper=p90
        )


    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    @staticmethod
    def normalize(series, reverse=False):

        s = CompositeScoreEngine.winsorize(series)

        minimum = s.min()
        maximum = s.max()

        if pd.isna(minimum) or pd.isna(maximum):

            return pd.Series(
                0,
                index=s.index
            )


        if minimum == maximum:

            return pd.Series(
                100,
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

        return np.where(
            series > 0,
            100,
            0
        )


    # ---------------------------------------------------------
    # Safe Division
    # ---------------------------------------------------------

    @staticmethod
    def safe_divide(
        numerator,
        denominator
    ):

        denominator = denominator.replace(
            0,
            np.nan
        )

        return numerator / denominator



    # ---------------------------------------------------------
    # Sector Relative Score
    # ---------------------------------------------------------

    def sector_relative_score(
    self,
    df,
    score_column="composite_score",
    sector_column="broad_sector"
    ):
       """
       Calculate sector-relative percentile score.

       If sector information is unavailable,
       return the dataframe without failing.
       """

       df = df.copy()

       # Check required columns
       if sector_column not in df.columns:
         df["sector_relative_score"] = np.nan
         return df

       if score_column not in df.columns:
        raise KeyError(f"'{score_column}' column not found.")

       def normalize_sector(group):

         minimum = group[score_column].min()
         maximum = group[score_column].max()

         if minimum == maximum:
            group["sector_relative_score"] = 50
         else:
            group["sector_relative_score"] = (
                (group[score_column] - minimum)
                /
                (maximum - minimum)
            ) * 100

            return group

       return (
        df
        .groupby(
            sector_column,
            group_keys=False
        )
        .apply(normalize_sector)
    )



    # ---------------------------------------------------------
    # Profitability Score (35%)
    # ---------------------------------------------------------

    def calculate_profitability_score(
        self,
        df
    ):

        roe = self.normalize(
            df["return_on_equity_pct"]
        )


        npm = self.normalize(
            df["net_profit_margin_pct"]
        )


        score = (

            roe * 0.20
            +
            npm * 0.15

        )


        return score.round(2)



    # ---------------------------------------------------------
    # Cash Quality Score (30%)
    # ---------------------------------------------------------

    def calculate_cash_quality_score(
        self,
        df
    ):


        fcf = self.normalize(
            df["free_cash_flow_cr"]
        )


        cfo_pat = self.normalize(
            df["cfo_pat_ratio"]
        )


        positive_fcf = self.positive_flag(
            df["free_cash_flow_cr"]
        )


        score = (

            fcf * 0.15
            +
            cfo_pat * 0.10
            +
            positive_fcf * 0.05

        )


        return score.round(2)


    # ---------------------------------------------------------
    # Growth Score (20%)
    # ---------------------------------------------------------

    def calculate_growth_score(
        self,
        df
    ):


        revenue = self.normalize(
            df["revenue_cagr_5yr"]
        )


        pat = self.normalize(
            df["pat_cagr_5yr"]
        )


        score = (

            revenue * 0.10
            +
            pat * 0.10

        )


        return score.round(2)



    # ---------------------------------------------------------
    # Leverage Score (15%)
    # ---------------------------------------------------------

    def calculate_leverage_score(
        self,
        df
    ):


        debt = self.normalize(
            df["debt_to_equity"],
            reverse=True
        )


        icr = self.normalize(
            df["interest_coverage"]
        )


        score = (

            debt * 0.10
            +
            icr * 0.05

        )


        return score.round(2)



    # ---------------------------------------------------------
    # Final Composite Score
    # ---------------------------------------------------------

    def calculate_composite_score(
        self,
        df
    ):


        data = df.copy()


        # CFO / PAT Ratio

        data["cfo_pat_ratio"] = self.normalize(
           data["cash_from_operations_cr"]
        )
        
        data["profitability_score"] = (
            self.calculate_profitability_score(data)
        )


        data["cash_quality_score"] = (
            self.calculate_cash_quality_score(data)
        )


        data["growth_score"] = (
            self.calculate_growth_score(data)
        )


        data["leverage_score"] = (
            self.calculate_leverage_score(data)
        )



        data["composite_score"] = (

            data["profitability_score"]
            +
            data["cash_quality_score"]
            +
            data["growth_score"]
            +
            data["leverage_score"]

        )


        data["composite_score"] = (

            data["composite_score"]
            .clip(
                lower=0,
                upper=100
            )
            .round(2)

        )


        # Sector Relative Score (only if sector data is available)
        if "broad_sector" in data.columns:
          data = self.sector_relative_score(data)
          data["sector_relative_score"] = (
            data["sector_relative_score"]
            .round(2)
          )
        else:
          data["sector_relative_score"] = np.nan

        return data