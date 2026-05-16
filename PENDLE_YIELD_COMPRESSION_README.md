# Pendle Long PT / Short YT Yield Compression Strategy
### Yield Mispricing Research | Ethereum Mainnet | Live Pendle API Data

> A systematic yield compression strategy on Pendle Finance that trades dislocations between implied APY (embedded in PT pricing) and realized underlying APY. Covers two asset classes: stablecoin markets (sUSDe, USDe, USDf, syrupUSDC, sfrxUSD and more) and ETH LST/LRT markets (wstETH, rsETH, weETH, pufETH and more). Data fetched live from the Pendle v2 API.

---

## Strategy Thesis

Pendle PT prices embed the market's forward expectation of yield. During regime shifts, liquidity shocks, or sentiment extremes, implied yield often deviates materially from the actual realized yield of the underlying asset.

```
Yield Gap = Implied APY − Underlying APY
```

Underlying yields lag because they are **mechanically generated** from staking and lending loops — they cannot reprice instantly. Implied yields overshoot during liquidation cascades, funding squeezes, and risk-off macro regimes.

This inertia creates **predictable yield compression** — a systematic edge with no directional price exposure.

---

## Trade Construction

| Signal | Trade Setup | Payoff Logic |
|--------|-------------|--------------|
| Yield Gap Z > +threshold | **Long PT + Short YT** | Implied too high → compresses lower |
| Yield Gap Z < −threshold | **Short PT + Long YT** | Implied too low → reverts higher |
| \|Z\| < exit threshold | **Exit** | Gap mean-reverted |

The strategy is **delta-neutral to ETH/USD price** — PnL comes purely from yield convergence, not price direction.

---

## Signal Construction

```python
# Core yield gap
yield_gap = implied_apy - underlying_apy

# Adaptive normalization window (scales with time-to-expiry)
norm_window = min(30, max(10, days_to_expiry / 4))

# Rolling std normalization per market
yield_gap_std  = yield_gap.rolling(norm_window).std()
yield_gap_norm = yield_gap / yield_gap_std

# EMA + slope for trend detection
ema_14       = yield_gap_norm.ewm(span=10).mean()
ema_14_slope = ema_14.diff()
```

The normalization window **adapts to time-to-expiry** — shorter windows for near-expiry markets where yield dynamics compress faster.

---

## Data Pipeline

Live data pulled directly from **Pendle Finance v2 API** — no static CSV required:

```python
BASE_URL = "https://api-v2.pendle.finance/core"

def get_market_history(market_address):
    url = f"{BASE_URL}/v2/{CHAIN_ID}/markets/{market_address}/historical-data"
    params = {
        "time_frame": "day",
        "fields": "timestamp,ptPrice,ytPrice,impliedApy,underlyingApy,tradingVolume,tvl",
        "timestamp_start": (now - 9_months).isoformat()
    }
    ...
```

Markets are auto-discovered from Pendle's market registry, filtered by:
- Asset name match (e.g. "wsteth", "susde")
- Minimum 21 days to expiry (avoids near-maturity noise)
- Excludes BERA chain markets

---

## Markets Covered

### Stablecoin Markets (`Stable_LongPT_ShortYT_Yield_compression_strategy.py`)

| Asset | Type |
|-------|------|
| sUSDe | Ethena staked USDe |
| USDe | Ethena synthetic dollar |
| USDf / sUSDf | Fluid stable |
| fxSAVE | fx Protocol savings |
| syrupUSDC | Maple syrup USDC |
| upUSDC | Usual USDC |
| ysUSDC | Yearn staked USDC |
| sfrxUSD | Frax staked USD |

### ETH LST/LRT Markets (`ETH_LongPT_ShortYT_Yield_compression_strategy.py`)

| Asset | Type |
|-------|------|
| wstETH | Lido wrapped staked ETH |
| swETH | Swell staked ETH |
| rsETH | KelpDAO restaked ETH |
| weETH | ether.fi restaked ETH |
| pufETH | Puffer restaked ETH |
| uniETH | Bedrock staked ETH |
| hgETH | Hourglass ETH |

---

## PnL Attribution

```python
# Long PT / Short YT
pnl = notional * (underlying_yield - implied_yield) * holding_period

# Short PT / Long YT
pnl = notional * (implied_yield - underlying_yield) * holding_period
```

No price prediction required — only yield convergence. The strategy profits whether ETH goes up, down, or sideways.

---

## Output Metrics

The backtest reports:

- ROI, CAGR
- Sharpe / Sortino
- Max Drawdown
- Convexity Ratio
- Tail Loss Frequency
- Worst 5% PnL
- Time Underwater
- Trade Win Rate

---

## Connection to Live Strategies

The Long PT / Short YT yield compression logic is conceptually the same as the **Stable PT sleeve** in the Solana Yield Vault:

> *"The stable-asset sleeve deploys into principal token (PT) yield loops... This sleeve carries zero price risk — both legs are stable assets, making it a pure yield harvesting position independent of SOL price movement."*

This Pendle research on Ethereum informed the PT/YT allocation design in both the Solana vault and the Boros yield strategy.

---

## Assumptions & Limitations

- No slippage or gas costs modeled
- No liquidation or depeg risk modeled
- Daily compounding assumed
- Delta-neutral to price, not to volatility
- PT/YT liquidity assumed sufficient at all times

For production deployment, add: slippage modeling, liquidity stress testing, depeg protection, execution cost simulation.

---

## Requirements

```bash
pip install requests pandas pyarrow tqdm matplotlib
```

No API key required — Pendle's public API is used directly.

---

## Related Work

- [boros-yield-strategy](../boros-yield-strategy/) — Live yield strategy using similar implied vs realized yield logic (175.5% ROI)
- [solana-yield-vault](../solana-yield-vault/) — Regime-based vault with PT yield sleeve
- [Detecting-Crowd-Chasing](../Detecting-Crowd-Chasing-in-Funding-Yield-Markets-on-Boros-and-Rho/) — Signal discovery research behind the live strategy
