# region imports
from AlgorithmImports import *
# endregion


class EqualWeightAlpha:
    """
    Alpha organism for NewsSentimentAlpha — BASELINE PLACEHOLDER.

    Emits a flat (equal) signal for every ticker in the universe so the
    scaffold has a known-good local baseline before the real signal is
    wired in.

    TODO (parent session): replace `compute_signals` with the GDELT
    financial-media news-tone z-score per ticker (read from the bundled
    `data/sentiment_panel.csv` — see domain/config.py SENTIMENT_PANEL_CSV).
    The real signal should return one z-score per ticker per rebalance;
    models/portfolio.py then ranks and splits top half long / bottom half
    short instead of this placeholder's equal-weight-long-only behavior.

    Layer: ORGANISM (orchestrates signal generation).
    Dependencies: none yet — pure Python, no domain/signals atom required
    for the baseline. The real version should delegate the z-score math to
    a pure function under domain/signals/ (see workspace shared-signals
    convention) if that logic becomes reusable across projects.
    """

    def __init__(self, universe: list[str]):
        self.name = "EqualWeightAlpha"
        self.universe = universe

    def compute_signals(self) -> dict[str, float]:
        """Flat signal (1.0) for every ticker in the universe.

        Returns:
            dict[ticker, signal]: baseline placeholder — every ticker gets
            an identical positive signal, so downstream portfolio
            construction holds the full universe equal-weight long-only.
        """
        return {ticker: 1.0 for ticker in self.universe}
