"""
Configuration constants for NewsSentimentAlpha.

Layer: ATOMS (pure constants, no dependencies except stdlib)

Usage:
    from domain.config import *
"""

# === ObjectStore ===
OBJECTSTORE_NAMESPACE = "news_sentiment_alpha"

# === Universe ===
# 10-stock universe for the news-tone long/short signal.
UNIVERSE = [
    "GS", "AAPL", "JPM", "BA", "HD", "IBM", "VZ", "V", "NKE", "CSCO",
]
BENCHMARK = "SPY"

# === Backtest Configuration ===
# Window chosen for dense GDELT news-tone coverage.
START_DATE = (2017, 1, 1)
END_DATE = (2021, 12, 31)
CASH = 100_000

# === Strategy Parameters ===
# TODO (parent session): tune once the real signal is wired in.
# Baseline scaffold currently ignores these and holds the full universe
# equal-weight long-only — see models/alpha.py and models/portfolio.py.

# Example: news-tone signal parameters (not yet used by the baseline)
# SENTIMENT_LOOKBACK_DAYS = 5      # smoothing window for the tone z-score
# LONG_SHORT_SPLIT = 0.5           # top half long / bottom half short

# === Bundled Data ===
# TODO (parent session): add data/sentiment_panel.csv — a bundled per-project
# CSV of GDELT financial-media news-tone z-scores, one row per (date, ticker).
# Read it with an __file__-relative path (see workspace claude.md "Bundled
# per-project data") rather than a WRDS pipeline read, since this data has no
# extraction pipeline in this workspace and is supplied directly by the user.
SENTIMENT_PANEL_CSV = "data/sentiment_panel.csv"
