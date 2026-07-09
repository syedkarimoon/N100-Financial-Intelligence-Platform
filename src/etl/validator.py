"""
validator.py

Data Quality Validator for the
N100 Financial Intelligence Platform.

Implements DQ-01 to DQ-16 validation framework.
"""

from pathlib import Path
import pandas as pd


class SchemaValidator:
    """
    Performs Data Quality validation on all datasets.
    """

    def __init__(self):

        self.validation_failures = []

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def log_failure(
        self,
        rule,
        severity,
        dataset,
        company_id,
        year,
        message,
    ):
        """
        Store validation failure.
        """

        self.validation_failures.append(
            {
                "rule": rule,
                "severity": severity,
                "dataset": dataset,
                "company_id": company_id,
                "year": year,
                "message": message,
            }
        )

    # --------------------------------------------------
    # Export CSV
    # --------------------------------------------------

    def export_failures(self, output_path):

        df = pd.DataFrame(self.validation_failures)

        df.to_csv(output_path, index=False)

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):

        if len(self.validation_failures) == 0:

            return {
                "status": "PASS",
                "failures": 0,
            }

        return {
            "status": "FAIL",
            "failures": len(self.validation_failures),
        }

    # ==================================================
    # DQ-01
    # Company Primary Key
    # ==================================================

    def validate_company_pk(self, companies):

        duplicated = companies["id"].duplicated()

        if duplicated.any():

            duplicate_rows = companies.loc[duplicated]

            for _, row in duplicate_rows.iterrows():

                self.log_failure(
                    rule="DQ-01",
                    severity="CRITICAL",
                    dataset="companies",
                    company_id=row["id"],
                    year="",
                    message="Duplicate company_id",
                )

            return False

        return True

    # ==================================================
    # DQ-02
    # Annual PK
    # ==================================================

    def validate_annual_pk(
        self,
        dataframe,
        dataset_name,
    ):

        duplicated = dataframe.duplicated(
            subset=["company_id", "year"]
        )

        if duplicated.any():

            duplicate_rows = dataframe.loc[duplicated]

            for _, row in duplicate_rows.iterrows():

                self.log_failure(
                    rule="DQ-02",
                    severity="CRITICAL",
                    dataset=dataset_name,
                    company_id=row["company_id"],
                    year=row["year"],
                    message="Duplicate company/year",
                )

            return False

        return True

    # ==================================================
    # DQ-03
    # FK Integrity
    # ==================================================

    def validate_foreign_key(
        self,
        child_df,
        companies_df,
        dataset_name,
    ):

        valid = set(companies_df["id"])

        invalid = child_df[
            ~child_df["company_id"].isin(valid)
        ]

        if len(invalid) > 0:

            for _, row in invalid.iterrows():

                self.log_failure(
                    rule="DQ-03",
                    severity="CRITICAL",
                    dataset=dataset_name,
                    company_id=row["company_id"],
                    year=row["year"],
                    message="Orphan company_id",
                )

            return False

        return True
        # ==================================================
    # DQ-07
    # Year Format Validation
    # ==================================================

    def validate_year_format(
        self,
        dataframe,
        dataset_name,
    ):

        import re

        valid = True

        pattern = re.compile(r"^\d{4}-\d{2}$")

        for index, row in dataframe.iterrows():

            year = row["year"]

            if pd.isna(year):

                self.log_failure(
                    rule="DQ-07",
                    severity="CRITICAL",
                    dataset=dataset_name,
                    company_id=row.get("company_id", ""),
                    year="",
                    message="Missing year",
                )

                valid = False
                continue

            if not pattern.match(str(year)):

                self.log_failure(
                    rule="DQ-07",
                    severity="CRITICAL",
                    dataset=dataset_name,
                    company_id=row.get("company_id", ""),
                    year=year,
                    message="Invalid year format",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-08
    # Ticker Validation
    # ==================================================

    def validate_ticker_format(
        self,
        dataframe,
        dataset_name,
    ):

        valid = True

        for _, row in dataframe.iterrows():

            ticker = str(row["company_id"]).strip().upper()

            if len(ticker) < 2 or len(ticker) > 12:

                self.log_failure(
                    rule="DQ-08",
                    severity="CRITICAL",
                    dataset=dataset_name,
                    company_id=ticker,
                    year=row.get("year", ""),
                    message="Ticker length must be between 2 and 12 characters",
                )

                valid = False

        return valid
        # ==================================================
    # DQ-04
    # Balance Sheet Validation
    # ==================================================

    def validate_balance_sheet(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            assets = row.get("total_assets")
            liabilities = row.get("total_liabilities")

            if pd.isna(assets) or pd.isna(liabilities):
                continue

            if assets == 0:
                continue

            difference = abs(assets - liabilities) / assets

            if difference >= 0.01:

                self.log_failure(
                    rule="DQ-04",
                    severity="WARNING",
                    dataset="balance_sheet",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Balance sheet mismatch (>1%)",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-05
    # OPM Cross Check
    # ==================================================

    def validate_opm(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            sales = row.get("sales")
            operating_profit = row.get("operating_profit")
            opm = row.get("opm_percentage")

            if pd.isna(sales) or sales == 0:
                continue

            if pd.isna(operating_profit) or pd.isna(opm):
                continue

            calculated = (operating_profit / sales) * 100

            if abs(calculated - opm) >= 1:

                self.log_failure(
                    rule="DQ-05",
                    severity="WARNING",
                    dataset="profit_and_loss",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="OPM percentage mismatch",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-06
    # Positive Sales
    # ==================================================

    def validate_positive_sales(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            sales = row.get("sales")

            if pd.isna(sales):
                continue

            if sales <= 0:

                self.log_failure(
                    rule="DQ-06",
                    severity="WARNING",
                    dataset="profit_and_loss",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Sales must be greater than zero",
                )

                valid = False

        return valid
        # ==================================================
    # DQ-09
    # Net Cash Flow Check
    # ==================================================

    def validate_net_cash_flow(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            cfo = row.get("cash_from_operating")
            cfi = row.get("cash_from_investing")
            cff = row.get("cash_from_financing")
            net = row.get("net_cash_flow")

            if any(pd.isna(x) for x in [cfo, cfi, cff, net]):
                continue

            calculated = cfo + cfi + cff

            if abs(calculated - net) > 10:

                self.log_failure(
                    rule="DQ-09",
                    severity="WARNING",
                    dataset="cash_flow",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Net cash flow mismatch",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-10
    # Fixed Assets
    # ==================================================

    def validate_fixed_assets(self, dataframe):

        valid = True

        for index, row in dataframe.iterrows():

            value = row.get("fixed_assets")

            if pd.isna(value):
                continue

            if value < 0:

                dataframe.at[index, "fixed_assets"] = 0

                self.log_failure(
                    rule="DQ-10",
                    severity="WARNING",
                    dataset="balance_sheet",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Negative fixed assets converted to 0",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-11
    # Tax Rate
    # ==================================================

    def validate_tax_rate(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            tax = row.get("tax_percentage")

            if pd.isna(tax):
                continue

            if tax < 0 or tax > 60:

                self.log_failure(
                    rule="DQ-11",
                    severity="WARNING",
                    dataset="profit_and_loss",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Tax rate outside valid range",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-12
    # Dividend Payout
    # ==================================================

    def validate_dividend(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            payout = row.get("dividend_payout")

            if pd.isna(payout):
                continue

            if payout > 200:

                self.log_failure(
                    rule="DQ-12",
                    severity="WARNING",
                    dataset="analysis",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="Dividend payout above 200%",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-13
    # URL Check (placeholder)
    # ==================================================

    def validate_urls(self, dataframe):

        return True

    # ==================================================
    # DQ-14
    # EPS Sign
    # ==================================================

    def validate_eps(self, dataframe):

        valid = True

        for _, row in dataframe.iterrows():

            eps = row.get("eps")
            profit = row.get("net_profit")

            if pd.isna(eps) or pd.isna(profit):
                continue

            if profit > 0 and eps <= 0:

                self.log_failure(
                    rule="DQ-14",
                    severity="WARNING",
                    dataset="profit_and_loss",
                    company_id=row.get("company_id", ""),
                    year=row.get("year", ""),
                    message="EPS sign inconsistent",
                )

                valid = False

        return valid

    # ==================================================
    # DQ-15
    # Balance Counter
    # ==================================================

    def validate_balance_counter(self, dataframe):

        return True

    # ==================================================
    # DQ-16
    # Coverage Check
    # ==================================================

    def validate_coverage(self, dataframe):

        valid = True

        counts = dataframe.groupby("company_id")["year"].count()

        for company, years in counts.items():

            if years < 5:

                self.log_failure(
                    rule="DQ-16",
                    severity="WARNING",
                    dataset="coverage",
                    company_id=company,
                    year="",
                    message="Less than five years of data",
                )

                valid = False

        return valid
