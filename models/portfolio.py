# region imports
from AlgorithmImports import *
# endregion


class EqualWeightPortfolio:
    """
    Portfolio construction organism for NewsSentimentAlpha — BASELINE
    PLACEHOLDER.

    Converts the flat baseline signal into equal-weight long-only targets
    (simple buy-and-hold across the universe, rebalanced back to equal
    weight on each scheduled call).

    TODO (parent session): replace `to_targets` with the ranked long/short
    construction — sort tickers by news-tone z-score, go long the top half
    and short the bottom half, weights equal-weighted (or z-score-weighted)
    within each side, normalized to the desired gross exposure.

    Layer: ORGANISM (orchestrates portfolio construction).
    """

    def to_targets(self, signals: dict[str, float]) -> dict[str, float]:
        """Equal-weight long-only targets across every ticker with a signal.

        Args:
            signals: dict[ticker, signal] from EqualWeightAlpha.

        Returns:
            dict[ticker, weight]: equal weight (1/N) per ticker, long only,
            summing to 1.0 gross exposure.
        """
        if not signals:
            return {}
        weight = 1.0 / len(signals)
        return {ticker: weight for ticker in signals}
