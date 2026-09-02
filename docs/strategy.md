# NewsSentimentAlpha - Strategy Logic

## Overview

Target strategy: a daily long/short equal-weight equity portfolio ranked
by a financial-media news-tone z-score signal per stock (GDELT), top half
of the ranked universe long / bottom half short, rebalanced daily.

**Current implementation status: baseline only.** The news-tone ranking
is not wired in. `main.py` currently runs an equal-weight, long-only,
buy-and-hold baseline across the full universe. Everything below is
split into "Implemented (baseline)" and "TODO (target strategy)".

## Strategy Type

- **Category**: Cross-sectional long/short, news-sentiment factor (target); equal-weight long-only (current baseline)
- **Asset Class**: US Equities
- **Holding Period**: Daily rebalance (positions turn over as ranks change)
- **Rebalance Frequency**: Daily, market open + 5 minutes

## Universe

Static 10-stock list, no dynamic selection:

GS, AAPL, JPM, BA, HD, IBM, VZ, V, NKE, CSCO

Defined in `domain/config.py::UNIVERSE`.

## Signal Generation (Alpha Model)

### Implemented (baseline)

`models/alpha.py::EqualWeightAlpha.compute_signals()` returns a flat
signal of `1.0` for every ticker in the universe — no ranking, no news
data read.

### TODO (target strategy)

| Parameter | Value | Description |
|-----------|-------|--------------|
| Sentiment source | `data/sentiment_panel.csv` | GDELT financial-media news-tone z-score, one row per (date, ticker) — **not yet added**, will be supplied by the parent session |
| Signal | Per-ticker z-score | Cross-sectional rank input for the current rebalance date |

Logic (planned):

```
1. Read data/sentiment_panel.csv (bundled, __file__-relative path)
2. For the current rebalance date, look up each ticker's news-tone z-score
3. Return {ticker: z_score} for the current date (point-in-time — no
   look-ahead past the rebalance date)
```

## Portfolio Construction

### Implemented (baseline)

`models/portfolio.py::EqualWeightPortfolio.to_targets()` divides `1.0`
gross exposure equally across every ticker with a signal (`1 / N` each),
long-only.

### TODO (target strategy)

| Parameter | Value | Description |
|-----------|-------|--------------|
| Long/short split | Top half / bottom half | Rank tickers by z-score, long the top 5, short the bottom 5 (10-stock universe) |
| Weighting | Equal-weight within each side (default) | Revisit if z-score-weighting is wanted instead |
| Gross exposure | 100% (default) | 50% long + 50% short, dollar-neutral by default — confirm with parent session before changing |

### Constraint Order (planned)

1. Rank tickers by z-score for the current date
2. Split into long half (top) / short half (bottom)
3. Equal-weight within each half, normalize to target gross exposure

## Execution

### Order Types

- **Entry**: Market order (`SetHoldings`)
- **Exit**: Market order (`SetHoldings` to new target weight, including 0.0 to flatten)

`models/execution.py::MarketOrderExecutor` does not need to change when
the real signal lands — it already applies any weight dict it's given,
positive or negative.

## Risk Management

Not yet defined beyond the implicit 100% gross exposure cap from
equal-weighting. No stop loss / take profit, no explicit per-position or
sector limits. Revisit once the target strategy is implemented.

## Backtest Configuration

| Setting | Value |
|---------|-------|
| Start Date | 2017-01-01 |
| End Date | 2021-12-31 |
| Starting Cash | $100,000 |
| Benchmark | SPY |
| Warmup Period | 5 days (baseline; TODO — target strategy may need a longer lookback for signal smoothing) |

Window chosen for dense GDELT news-tone coverage.

## Strategy Invariants

These rules must not change without explicit approval:

1. Universe is the static 10-stock list above — no dynamic universe selection.
2. Rebalance is daily.
3. Data sources are WRDS/CRSP daily equity prices (local) and the bundled GDELT news-tone CSV — no live API calls at runtime.
