# region imports
from AlgorithmImports import *

from datetime import timedelta

from domain.config import UNIVERSE, BENCHMARK, START_DATE, END_DATE, CASH
from models import (
    EqualWeightAlpha,
    EqualWeightPortfolio,
    MarketOrderExecutor,
    PortfolioLogger,
)
# endregion


class NewsSentimentAlphaAlgorithm(QCAlgorithm):
    """
    NewsSentimentAlpha — BASELINE SCAFFOLD.

    Target strategy (not yet implemented — see TODOs below and in
    models/alpha.py, models/portfolio.py, domain/config.py):
      Daily long/short equal-weight portfolio across a 10-stock universe,
      ranked by a financial-media news-tone z-score signal per stock
      (GDELT). Top half of the ranked universe is long, bottom half is
      short, rebalanced daily.

    Current baseline behavior (this scaffold):
      Equal-weight, long-only, buy-and-hold across the full 10-stock
      universe, rebalanced daily back to equal weight. This exists to
      prove the project compiles and backtests locally against WRDS/CRSP
      daily equity data before the real signal is layered on top.

    Data sources:
      - WRDS/CRSP daily equity prices (already local):
        infrastructure/pipelines/wrds/lean-data/equity/usa/daily/{ticker}.zip
      - Bundled GDELT financial-media news-tone z-score CSV
        (data/sentiment_panel.csv) — NOT YET ADDED. To be supplied directly
        by the parent session; no extraction pipeline needed.

    Architecture: Atomic Structure
    - Composition Root: This file (main.py)
    - Organisms: models/ (alpha, portfolio, execution, logger)
    - Molecules + Atoms: domain/ (business logic, DTOs, config)

    Pattern: teaching/direct SetHoldings (not the QC AlphaModel framework
    lifecycle) — see AGENTS.md "Pattern Choice" and
    MyProjects/ElectionIndustryBeta/ for the worked example this mirrors.
    """

    def Initialize(self):
        # === Backtest Configuration ===
        self.SetStartDate(*START_DATE)
        self.SetEndDate(*END_DATE)
        self.SetCash(CASH)
        self.SetBenchmark(BENCHMARK)

        # === Universe — manual AddEquity per ticker (static universe) ===
        self._symbols: dict[str, Symbol] = {}
        for ticker in UNIVERSE:
            self._symbols[ticker] = self.AddEquity(
                ticker, Resolution.Daily
            ).Symbol
        # Benchmark needs its own subscription so scheduling on its
        # calendar works even though it isn't traded.
        if BENCHMARK not in self._symbols:
            self.AddEquity(BENCHMARK, Resolution.Daily)

        # === Warmup ===
        # Baseline placeholder needs no history. Keep a small warmup so the
        # scheduled handler doesn't fire before data is flowing; the real
        # news-tone signal will likely need a longer lookback for smoothing
        # (see domain/config.py TODO).
        self.SetWarmUp(timedelta(days=5))

        # === Wire organisms ===
        self._alpha = EqualWeightAlpha(universe=UNIVERSE)
        self._portfolio = EqualWeightPortfolio()
        self._executor = MarketOrderExecutor()
        self._logger = PortfolioLogger(self)

        # === Scheduled Events — daily rebalance ===
        self.Schedule.On(
            self.DateRules.EveryDay(BENCHMARK),
            self.TimeRules.AfterMarketOpen(BENCHMARK, 5),
            self._rebalance,
        )

    # ------------------------------------------------------------------
    # Lifecycle hooks
    # ------------------------------------------------------------------

    def OnData(self, data: Slice):
        """Process incoming data. Rebalancing is schedule-driven; nothing
        to do here for the baseline."""
        pass

    def OnOrderEvent(self, orderEvent: OrderEvent):
        """Log fills to the ObjectStore trade record."""
        if orderEvent.Status != OrderStatus.Filled:
            return
        action = "BUY" if orderEvent.FillQuantity > 0 else "SELL"
        self._logger.log_trade(
            date=self.Time,
            symbol=orderEvent.Symbol,
            action=action,
            quantity=float(orderEvent.FillQuantity),
            price=float(orderEvent.FillPrice),
        )

    def OnEndOfAlgorithm(self):
        """Finalize and save data to ObjectStore."""
        self._logger.save_all()

    # ------------------------------------------------------------------
    # Scheduled handler
    # ------------------------------------------------------------------

    def _rebalance(self) -> None:
        if self.IsWarmingUp:
            return

        # 1. Compute signal.
        #    TODO (parent session): replace with the GDELT news-tone
        #    z-score ranking (see models/alpha.py TODO).
        signals = self._alpha.compute_signals()
        if not signals:
            return

        # 2. Convert to portfolio targets.
        #    TODO (parent session): replace with top-half-long /
        #    bottom-half-short ranked construction (see
        #    models/portfolio.py TODO).
        targets = self._portfolio.to_targets(signals)

        # 3. Execute.
        self._executor.execute(self, UNIVERSE, targets)

        # 4. Snapshot for ObjectStore analysis.
        gross = sum(abs(w) for w in targets.values())
        n_long = sum(1 for w in targets.values() if w > 0)
        n_short = sum(1 for w in targets.values() if w < 0)
        self._logger.log_daily_snapshot(
            date=self.Time,
            nav=float(self.Portfolio.TotalPortfolioValue),
            gross_exposure=gross,
            n_long=n_long,
            n_short=n_short,
        )
        for ticker, weight in targets.items():
            if weight == 0.0:
                continue
            symbol = self._symbols[ticker]
            price = float(self.Securities[symbol].Price)
            qty = float(self.Portfolio[symbol].Quantity)
            self._logger.log_position(
                date=self.Time,
                symbol=ticker,
                quantity=qty,
                price=price,
                target_weight=weight,
            )
