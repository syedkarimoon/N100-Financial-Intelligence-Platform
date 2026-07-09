"""
normalizer.py

Data normalization utilities for the N100 Financial Intelligence Platform.
"""

import re
import pandas as pd


class DataNormalizer:
    """
    Collection of helper methods used during ETL.
    """

    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize DataFrame column names.
        """

        df = df.copy()

        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("%", "pct", regex=False)
            .str.replace(r"[^\w]", "", regex=True)
        )

        return df

    @staticmethod
    def normalize_year(value):
        """
        Normalize financial year into a standard format.

        Supported:
            Mar-23      -> 2023-03
            Mar-2024    -> 2024-03
            Dec-23      -> 2023-12
            Dec-2024    -> 2024-12
            FY24        -> 2024-03
            FY2024      -> 2024-03
            FY 2024     -> 2024-03
            2024        -> 2024-03
            2024-03     -> 2024-03
        """

        if pd.isna(value):
            return None

        value = str(value).strip()

        if value == "":
            return None

        # Already normalized
        if re.fullmatch(r"\d{4}-\d{2}", value):
            return value

        # Mar-23 / Mar-2023
        match = re.fullmatch(r"Mar-(\d{2}|\d{4})", value, flags=re.IGNORECASE)

        if match:
            year = match.group(1)

            if len(year) == 2:
                year = "20" + year

            return f"{year}-03"

        # Dec-23 / Dec-2023
        match = re.fullmatch(r"Dec-(\d{2}|\d{4})", value, flags=re.IGNORECASE)

        if match:
            year = match.group(1)

            if len(year) == 2:
                year = "20" + year

            return f"{year}-12"

        # FY24 / FY2024 / FY 2024
        match = re.fullmatch(r"FY\s?(\d{2}|\d{4})", value, flags=re.IGNORECASE)

        if match:
            year = match.group(1)

            if len(year) == 2:
                year = "20" + year

            return f"{year}-03"

        # Plain year
        if re.fullmatch(r"\d{4}", value):
            return f"{value}-03"

        return None

    @staticmethod
    def normalize_ticker(value):
        """
        Normalize company ticker.
        """

        if pd.isna(value):
            return None

        ticker = str(value).strip().upper()

        if ticker == "":
            return None

        # Remove NSE/BSE suffix
        ticker = re.sub(r"\.(NS|BO)$", "", ticker)

        # Remove spaces
        ticker = ticker.replace(" ", "")

        # Remove hyphen
        ticker = ticker.replace("-", "")

        return ticker

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
        """
        Remove duplicate rows.
        """

        return df.drop_duplicates(subset=subset).reset_index(drop=True)
    