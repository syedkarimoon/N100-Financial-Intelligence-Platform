class CashFlowEngine:

    @staticmethod
    def free_cash_flow(operating_activity, investing_activity):
        """
        Calculate Free Cash Flow.

        Formula:
        FCF = Operating Cash Flow + Investing Cash Flow

        Returns:
            float
        """
        return operating_activity + investing_activity

    @staticmethod
    def cfo_quality_score(cfo_values, pat_values):
        """
        Calculate average CFO/PAT ratio over multiple years.

        Returns:
            (average_ratio, quality_label)
        """

        if len(cfo_values) != len(pat_values):
            raise ValueError("CFO and PAT lists must have the same length.")

        ratios = []

        for cfo, pat in zip(cfo_values, pat_values):
            if pat == 0:
                return None, None

            ratios.append(cfo / pat)

        average_ratio = sum(ratios) / len(ratios)

        if average_ratio > 1.0:
            quality = "High Quality"
        elif average_ratio >= 0.5:
            quality = "Moderate"
        else:
            quality = "Accrual Risk"

        return round(average_ratio, 2), quality

    @staticmethod
    def capex_intensity(investing_activity, sales):
        """
        Calculate CapEx Intensity.

        Returns:
            (capex_percentage, category)
        """

        if sales == 0:
            return None, None

        capex = (abs(investing_activity) / sales) * 100

        if capex < 3:
            category = "Asset Light"
        elif capex <= 8:
            category = "Moderate"
        else:
            category = "Capital Intensive"

        return round(capex, 2), category

    @staticmethod
    def fcf_conversion_rate(fcf, operating_profit):
        """
        Calculate FCF Conversion Rate.
        """

        if operating_profit == 0:
            return None

        return round((fcf / operating_profit) * 100, 2)

    @staticmethod
    def capital_allocation_pattern(
        operating_activity,
        investing_activity,
        financing_activity,
        cfo_quality=None
    ):
        """
        Classify capital allocation pattern.

        Returns:
            (
                cfo_sign,
                cfi_sign,
                cff_sign,
                pattern_label
            )
        """

        cfo = "+" if operating_activity >= 0 else "-"
        cfi = "+" if investing_activity >= 0 else "-"
        cff = "+" if financing_activity >= 0 else "-"

        pattern = (cfo, cfi, cff)

        if pattern == ("+", "-", "-"):
            if cfo_quality == "High Quality":
                label = "Shareholder Returns"
            else:
                label = "Reinvestor"

        elif pattern == ("+", "+", "-"):
            label = "Liquidating Assets"

        elif pattern == ("-", "+", "+"):
            label = "Distress Signal"

        elif pattern == ("-", "-", "+"):
            label = "Growth Funded by Debt"

        elif pattern == ("+", "+", "+"):
            label = "Cash Accumulator"

        elif pattern == ("-", "-", "-"):
            label = "Pre-Revenue"

        elif pattern == ("+", "-", "+"):
            label = "Mixed"

        else:
            label = "Unknown"

        return cfo, cfi, cff, label