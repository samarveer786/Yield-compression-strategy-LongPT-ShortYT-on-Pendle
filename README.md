# Pendle Long PT / Short YT Yield Compression Strategy

This repository contains two research scripts that implement a **yield mispricing / compression strategy** on Pendle Finance markets.

The strategy trades the dislocation between **Implied Yield (from PT pricing)** and **Underlying Realized Yield** of yield-bearing assets.

---

## Strategy Thesis

Pendle PT prices embed the market’s *forward expectation of yield*. During regime shifts, liquidity shocks, or sentiment extremes, this implied yield often deviates materially from the actual realized yield of the underlying asset.

This creates a systematic opportunity:

```
Yield Gap = Implied APY − Underlying APY
```

We normalize this yield gap and trade mean-reversion in forward yield expectations.

---

## Trade Construction

| Signal         | Trade Setup        | Payoff Logic                            |
| -------------- | ------------------ | --------------------------------------- |
| Yield Gap > +Z | Long PT + Short YT | Implied yield too high → compress lower |
| Yield Gap < −Z | Short PT + Long YT | Implied yield too low → revert higher   |

This repo currently focuses on:

• **Stablecoin markets**  → `Stable_LongPT_ShortYT_Yield_compression_strategy.py`
• **stETH / ETH markets** → `ETH_LongPT_ShortYT_Yield_compression_strategy.py`

---

## Files

| File                                                  | Description                                         |
| ----------------------------------------------------- | --------------------------------------------------- |
| `Stable_LongPT_ShortYT_Yield_compression_strategy.py` | Backtest engine for stable yield PT/YT pairs        |
| `ETH_LongPT_ShortYT_Yield_compression_strategy.py`    | Backtest engine for stETH / ETH based yield markets |

---

## Core Pipeline

1. **Fetch Pendle Markets**
2. **Pull historical PT prices & underlying APY**
3. **Compute Implied APY from PT discount curve**
4. **Compute Yield Gap**
5. **Z-score normalization of Yield Gap**
6. **Trade Long PT / Short YT when Z threshold is breached**
7. **Hold until gap mean-reverts to exit band**

---

## Yield Gap Calculation

```python
df["yield_gap"] = df["impliedApy"] - df["underlyingApy"]
```

This gap is then normalized using rolling mean & volatility to generate the Z-score signal.

---

## Entry / Exit Logic

```text
Entry Long PT / Short YT   → yield_gap_z > entry_z
Exit Trade                → abs(yield_gap_z) < exit_z
```

Each trade is sized equally across capital and trades do not overlap unless explicitly enabled.

---

## PnL Attribution

For each position:

```
Long PT / Short YT PnL = (Underlying Yield − Implied Yield) × Holding Period
Short PT / Long YT PnL = (Implied Yield − Underlying Yield) × Holding Period
```

The strategy does NOT rely on price prediction — only yield convergence.

---

## Output Metrics

The backtest reports:

• ROI, CAGR
• Sharpe / Sortino
• Max Drawdown
• Convexity Ratio
• Tail Loss Frequency
• Worst 5% PnL
• Time Underwater
• Trade Win Rate

---

## Assumptions

• PT & YT liquidity is sufficient
• No slippage / gas modeled
• No liquidation or depeg risk
• Daily compounding
• Strategy is delta-neutral to price, not to volatility

---

## Why This Works

Implied yields overshoot during:

• Liquidation cascades
• Funding squeezes
• Risk-off macro regimes

Underlying yields lag because they are mechanically generated from staking / lending loops.

This inertia creates predictable **yield compression**.

---

## Disclaimer

This is research code. Do not deploy without:

• Slippage modeling
• Liquidity stress testing
• Depeg protection
• Execution cost simulation
