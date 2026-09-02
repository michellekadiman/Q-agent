# region imports
from AlgorithmImports import *
# endregion


class MarketOrderExecutor:
    """
    Execution organism for NewsSentimentAlpha.

    Applies target weights via SetHoldings — market orders only.
    Tickers absent from `targets` (or with weight 0.0) are liquidated.

    This does not need to change when the real news-tone signal replaces
    the baseline alpha/portfolio placeholders — it just applies whatever
    weight dict it is given (positive weights go long, negative weights
    will go short once the ranked long/short logic is wired in).

    Layer: ORGANISM (orchestrates order execution).
    """

    def execute(
        self,
        algorithm: QCAlgorithm,
        universe: list[str],
        targets: dict[str, float],
    ) -> None:
        for ticker in universe:
            weight = targets.get(ticker, 0.0)
            algorithm.SetHoldings(ticker, weight)
