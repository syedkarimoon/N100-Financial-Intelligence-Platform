class GrowthScoreEngine:

    @staticmethod
    def score_cagr(cagr, flag):
        """
        Convert CAGR into a growth score.

        Returns:
            int: Score between 0 and 5
        """

        # Invalid CAGR
        if flag is not None or cagr is None:
            return 0

        # Negative CAGR
        if cagr < 0:
            return 0

        # Score bands
        if cagr > 20:
            return 5
        elif cagr > 15:
            return 4
        elif cagr > 10:
            return 3
        elif cagr > 5:
            return 2
        else:
            return 1

    @staticmethod
    def revenue_growth_score(cagr, flag):
        return GrowthScoreEngine.score_cagr(cagr, flag)

    @staticmethod
    def pat_growth_score(cagr, flag):
        return GrowthScoreEngine.score_cagr(cagr, flag)

    @staticmethod
    def eps_growth_score(cagr, flag):
        return GrowthScoreEngine.score_cagr(cagr, flag)
        
    @staticmethod
    def overall_growth_score(revenue_score, pat_score, eps_score):
        """
        Calculate overall growth score.
        """
        overall = (revenue_score + pat_score + eps_score) / 3
        return round(overall, 2)