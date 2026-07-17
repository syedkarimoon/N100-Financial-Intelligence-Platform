"""
Sprint 3 - Day 15
Filter Engine Core

Loads financial ratios from SQLite,
reads analyst-editable YAML configuration,
applies threshold filters,
and returns filtered companies.
"""

import sqlite3
from pathlib import Path

import pandas as pd
import yaml


class ScreenerEngine:
    """
    Financial Screener Engine
    """

    def __init__(
        self,
        db_path="db/nifty100.db",
        config_path="config/screener_config.yaml"
    ):
        self.db_path = Path(db_path)
        self.config_path = Path(config_path)

        self.conn = sqlite3.connect(self.db_path)

        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    def load_financial_ratios(self):
        """
        Load financial ratios along with sector information.
        """

        query = """
        SELECT
            fr.*,
            s.broad_sector,
            s.sub_sector
        FROM financial_ratios fr
        LEFT JOIN sectors s
            ON fr.company_id = s.company_id
        """

        df = pd.read_sql_query(query, self.conn)

        return df

    def apply_filters(self, df, filters):
        """
        Apply threshold filters.

        Parameters
        ----------
        df : pandas.DataFrame
            Financial ratios dataframe.

        filters : dict
            Dictionary containing filter definitions.
        """

        filtered_df = df.copy()
        filtered_df = self.prepare_interest_coverage(filtered_df)

        for filter_name, rule in filters.items():

            column = rule["column"]
            operator = rule["operator"]
            value = rule["value"]

            if column not in filtered_df.columns:
                continue

            if operator == ">=":
                filtered_df = filtered_df[
                    filtered_df[column] >= value
                ]

            elif operator == ">":
                filtered_df = filtered_df[
                    filtered_df[column] > value
                ]

            elif operator == "<=":

                if column == "debt_to_equity":

                    financial_companies = filtered_df[
                        filtered_df["broad_sector"] == "Financials"
                    ]

                    non_financial_companies = filtered_df[
                        filtered_df["broad_sector"] != "Financials"
                    ]

                    non_financial_companies = non_financial_companies[
                        non_financial_companies[column] <= value
                    ]

                    filtered_df = pd.concat(
                        [financial_companies, non_financial_companies],
                        ignore_index=True
                    )

                else:

                    filtered_df = filtered_df[
                        filtered_df[column] <= value
                    ]

            elif operator == "<":
                filtered_df = filtered_df[
                    filtered_df[column] < value
                ]

        filtered_df = filtered_df.sort_values(
            by="composite_quality_score",
            ascending=False,
            na_position="last"
        )

        return filtered_df

    def prepare_interest_coverage(self, df):
        """
        Handle special Interest Coverage values.

        Treat 'Debt Free' as infinity.
        """

        df = df.copy()

        df["interest_coverage"] = (
            df["interest_coverage"]
            .replace("Debt Free", float("inf"))
        )

        df["interest_coverage"] = pd.to_numeric(
            df["interest_coverage"],
            errors="coerce"
        )

        return df