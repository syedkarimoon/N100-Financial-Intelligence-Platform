import os
import pandas as pd
from src.analytics.cashflow import CashFlowEngine


class CapitalAllocationGenerator:

    @staticmethod
    def generate(input_file, output_file):
        """
        Generate capital allocation classification CSV.
        """

        df = pd.read_excel(
            input_file,
            header=1
        )

        results = []

        for _, row in df.iterrows():

            cfo_sign, cfi_sign, cff_sign, label = (
                CashFlowEngine.capital_allocation_pattern(
                    row["operating_activity"],
                    row["investing_activity"],
                    row["financing_activity"]
                )
            )

            results.append(
                {
                    "company_id": row["company_id"],
                    "year": row["year"],
                    "cfo_sign": cfo_sign,
                    "cfi_sign": cfi_sign,
                    "cff_sign": cff_sign,
                    "pattern_label": label
                }
            )

        output_df = pd.DataFrame(results)
        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )
        output_df.to_csv(
            output_file,
            index=False
        )

        return output_df