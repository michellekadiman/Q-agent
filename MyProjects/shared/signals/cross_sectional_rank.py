"""
Cross-sectional ranking signal atoms.

Layer: ATOM (pure Python — no LEAN imports, no I/O, no external dependencies).

Used by any strategy that ranks a cross-section of securities by a score and
trades the extremes: long the top fraction, short the bottom fraction,
equal-weighted within each side, dollar-neutral overall.

Run this file directly for a sanity check:
    python MyProjects/shared/signals/cross_sectional_rank.py
"""


def tercile_long_short_targets(scores, frac=1.0 / 3.0, gross=1.0, min_names=6):
    """Dollar-neutral long/short target weights from a cross-section of scores.

    Args:
        scores: {symbol: score} for the securities scored on this rebalance.
        frac: fraction of the cross-section to take on each side (1/3 = terciles,
            0.2 = quintiles, 0.1 = deciles).
        gross: total gross exposure; half goes long and half short.
        min_names: below this many scored names the cross-section is too thin to
            rank meaningfully and the book goes flat.

    Returns:
        {symbol: weight}, positive for longs and negative for shorts, summing to
        zero net and `gross` in absolute value. Empty when the cross-section is
        thinner than `min_names`.
    """
    n = len(scores)
    if n < min_names:
        return {}

    ranked = sorted(scores, key=scores.get)
    k = max(1, min(round(n * frac), n // 2))
    shorts, longs = ranked[:k], ranked[-k:]

    w = gross / (2 * k)
    targets = {t: -w for t in shorts}
    targets.update({t: w for t in longs})
    return targets


if __name__ == "__main__":
    demo = {"AAA": 5.0, "BBB": 4.0, "CCC": 3.0, "DDD": 2.0, "EEE": 1.0, "FFF": 0.0}

    t = tercile_long_short_targets(demo, frac=1.0 / 3.0)
    assert set(t) == {"AAA", "BBB", "EEE", "FFF"}, t
    assert abs(sum(t.values())) < 1e-12, "book must be dollar-neutral"
    assert abs(sum(abs(v) for v in t.values()) - 1.0) < 1e-12, "gross must be 1.0"

    d = tercile_long_short_targets(demo, frac=0.1)
    assert set(d) == {"AAA", "FFF"}, d
    assert abs(d["AAA"] - 0.5) < 1e-12 and abs(d["FFF"] + 0.5) < 1e-12, d

    assert tercile_long_short_targets({"AAA": 1.0}) == {}, "thin cross-section goes flat"

    print("cross_sectional_rank: all checks passed")
