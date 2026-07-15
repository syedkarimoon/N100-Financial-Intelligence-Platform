class CAGREngine:

    @staticmethod
    def calculate_cagr(start, end, years):
        """
        Calculate CAGR with edge case handling.

        Returns:
            (cagr_value, flag)
        """

        # Check for insufficient years
        if years is None or years <= 0:
            return None, "INSUFFICIENT"

        # Zero base value
        if start == 0:
            return None, "ZERO_BASE"

        # Positive -> Negative
        if start > 0 and end < 0:
            return None, "DECLINE_TO_LOSS"

        # Negative -> Positive
        if start < 0 and end > 0:
            return None, "TURNAROUND"

        # Negative -> Negative
        if start < 0 and end < 0:
            return None, "BOTH_NEGATIVE"

        # Normal CAGR calculation
        cagr = ((end / start) ** (1 / years) - 1) * 100

        return round(cagr, 2), None
    @staticmethod
    def revenue_cagr(start, end, years):
        """Calculate Revenue CAGR."""
        return CAGREngine.calculate_cagr(start, end, years)

    @staticmethod
    def pat_cagr(start, end, years):
        """Calculate PAT CAGR."""
        return CAGREngine.calculate_cagr(start, end, years)

    @staticmethod
    def eps_cagr(start, end, years):
        """Calculate EPS CAGR."""
        return CAGREngine.calculate_cagr(start, end, years)

    