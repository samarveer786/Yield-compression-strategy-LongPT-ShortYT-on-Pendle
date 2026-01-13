#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install requests pandas pyarrow tqdm


# In[1]:


import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

BASE_URL = "https://api-v2.pendle.finance/core"
CHAIN_ID = 1  # Ethereum only
LOOKBACK_MONTHS = 9
MIN_DAYS_TO_EXPIRY = 21


# In[2]:


def safe_get(url, params):
    r = requests.get(url, params=params, timeout=30)
    if r.status_code == 429:
        time.sleep(8)
        r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r


def get_all_markets():
    url = f"{BASE_URL}/v1/markets/all"
    params = {"chainId": CHAIN_ID}
    r = safe_get(url, params)
    return pd.DataFrame(r.json()["markets"])


def get_market_history(market_address):
    start_ts = datetime.utcnow() - timedelta(days=30 * LOOKBACK_MONTHS)

    url = f"{BASE_URL}/v2/{CHAIN_ID}/markets/{market_address}/historical-data"
    params = {
        "time_frame": "day",
        "fields": "timestamp,ptPrice,ytPrice,impliedApy,underlyingApy,tradingVolume,tvl",
        "timestamp_start": start_ts.isoformat()
    }

    r = safe_get(url, params)
    data = r.json()["results"]

    if not data:
        return None

    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df


# In[3]:


# ==========================
# ASSET: sUSDe
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_sUSDe = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    # match asset name
    if "susde" not in name:
        continue

    # skip BERA markets
    if "bera" in name:
        continue

    # maturity filter
    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    # download data
    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "sUSDe"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_sUSDe.append(df)

df_sUSDe = pd.concat(df_sUSDe).sort_index()


# In[4]:


# ==========================
# ASSET: USDe
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_USDe = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "usde" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "USDe"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_USDe.append(df)

df_USDe = pd.concat(df_USDe).sort_index()


# In[5]:


# ==========================
# ASSET: USDf
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_USDf = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "usdf" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "USDf"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_USDf.append(df)

df_USDf = pd.concat(df_USDf).sort_index()


# In[6]:


# ==========================
# ASSET: sUSDf
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_sUSDf = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "susdf" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "sUSDf"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_sUSDf.append(df)

df_sUSDf = pd.concat(df_sUSDf).sort_index()


# In[7]:


# ==========================
# ASSET: fxSAVE
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_fxSAVE = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "fxsave" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "fxSAVE"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_fxSAVE.append(df)

df_fxSAVE = pd.concat(df_fxSAVE).sort_index()


# In[8]:


# ==========================
# ASSET: syrupUSDC
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_syrupUSDC = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "syrupusdc" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "syrupUSDC"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_syrupUSDC.append(df)

df_syrupUSDC = pd.concat(df_syrupUSDC).sort_index()


# In[9]:


# ==========================
# ASSET: upUSDC
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_upUSDC = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "upusdc" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "upUSDC"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_upUSDC.append(df)

df_upUSDC = pd.concat(df_upUSDC).sort_index()


# In[10]:


# ==========================
# ASSET: ysUSDC
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_ysUSDC = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "ysusdc" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "ysUSDC"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_ysUSDC.append(df)

df_ysUSDC = pd.concat(df_ysUSDC).sort_index()


# In[11]:


# ==========================
# ASSET: sfrxUSD
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_sfrxUSD = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "sfrxusd" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "sfrxUSD"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_sfrxUSD.append(df)

df_sfrxUSD = pd.concat(df_sfrxUSD).sort_index()


# In[12]:


# ==========================
# ASSET: reUSD
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_reUSD = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "reusd" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "reUSD"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_reUSD.append(df)

df_reUSD = pd.concat(df_reUSD).sort_index()


# In[13]:


# ==========================
# ASSET: coreUSDC
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_coreUSDC = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "coreusdc" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "coreUSDC"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_coreUSDC.append(df)

df_coreUSDC = pd.concat(df_coreUSDC).sort_index()


# In[14]:


# ==========================
# ASSET: wstUSR
# ==========================

markets = get_all_markets()
now = datetime.now(timezone.utc)

df_wstUSR = []

for _, row in markets.iterrows():
    name = str(row.get("name", "")).lower()

    if "wstusr" not in name:
        continue
    if "bera" in name:
        continue

    expiry = row.get("expiry")
    if expiry is None:
        continue

    expiry_dt = pd.to_datetime(expiry, utc=True)
    if (expiry_dt - now).days < MIN_DAYS_TO_EXPIRY:
        continue

    df = get_market_history(row["address"])
    if df is None:
        continue

    df["asset"] = "wstUSR"
    df["market"] = row["name"]
    df["expiry"] = expiry_dt
    df["market_address"] = row["address"]

    df_wstUSR.append(df)

df_wstUSR = pd.concat(df_wstUSR).sort_index()


# In[15]:


df = df.drop(columns=["market"], errors="ignore")


# In[16]:


final_df = pd.concat([
    df_upUSDC,
    df_sUSDe,
    df_USDe,
    df_sUSDf,
    df_USDf,
    df_syrupUSDC,
    df_ysUSDC,
    df_sfrxUSD,
    df_reUSD,
    df_coreUSDC,
    df_wstUSR,
    df_fxSAVE
])


# In[17]:


### Adding Yield_gap and maturity columns
df = final_df.copy()

df["days_to_expiry"] = (df["expiry"] - df.index).dt.days
df["yield_gap"] = df["impliedApy"] - df["underlyingApy"]


df.drop(columns=["market"], errors="ignore")


# In[21]:


def norm_window(days_to_expiry):
    return int(min(30, max(10, days_to_expiry / 4)))
df["expiry"] = pd.to_datetime(df["expiry"])
df["days_to_expiry"] = (df["expiry"] - df.index).dt.days
market_windows = (
    df.groupby("market_address")["days_to_expiry"]
      .first()
      .apply(norm_window)
)
df["yield_gap_std"] = (
    df.groupby("market_address")["yield_gap"]
      .transform(
          lambda x: x.rolling(
              window=market_windows.loc[x.name],
              min_periods=10
          ).std()
      )
)
df["yield_gap_norm"] = df["yield_gap"] / df["yield_gap_std"]


# In[22]:


df = df.sort_values(["market_address", df.index.name])
EMA_SPAN = 10  # 14-day EMA

df["ema_14"] = (
    df.groupby("market_address")["yield_gap_norm"]
      .transform(lambda x: x.ewm(span=EMA_SPAN, adjust=False).mean())
)
df["ema_14_slope"] = (
    df.groupby("market_address")["ema_14"]
      .diff()
)
df["rolling_std_7d"] = (
    df.groupby("market_address")["yield_gap_norm"]
      .transform(lambda x: x.rolling(window=7, min_periods=7).std())
)

df["rolling_std_14d"] = (
    df.groupby("market_address")["yield_gap_norm"]
      .transform(lambda x: x.rolling(window=14, min_periods=14).std())
)
df.head()


# In[23]:


df.groupby("asset")["market_address"].nunique()


# In[1]:


import matplotlib.pyplot as plt

asset_name = "USDf"

df_asset = df[df["asset"] == asset_name].copy()


# In[ ]:


import numpy as np

def backtest_pt_compression(df_mkt, initial_capital=1000):
    df = df_mkt.copy().sort_index()

    Z = df["yield_gap_norm"]
    EMA = df["ema_14"]

    # === ENTRY CONDITIONS ===
    entry_cond = (
        (df["ema_14_slope"] < 0) &
        (Z > 0) &
        (Z < EMA * 0.98) &
        #(df["rolling_std_7d"] < df["rolling_std_14d"]) &
        (df["days_to_expiry"] >= 21)
    )

    # === EXIT CONDITIONS ===
    exit_cond = (
        (Z > EMA * 1.01)| 
        #(Z < 0.25) |
        (df["days_to_expiry"] <= 1)
    )

    trades = []
    in_trade = False

    for t in range(1, len(df)):
        if not in_trade and entry_cond.iloc[t]:
            entry_time = df.index[t]
            in_trade = True

        elif in_trade and exit_cond.iloc[t]:
            exit_time = df.index[t]
            days_held = (exit_time - entry_time).days

            # ---- CARRY-BASED PnL ----
            avg_carry = df.loc[entry_time:exit_time, "yield_gap"].mean()
            trade_return = avg_carry * (days_held / 365)

            trades.append({
                "entry_time": entry_time,
                "exit_time": exit_time,
                "days_held": days_held,
                "carry_apy": avg_carry,
                "return_pct": trade_return
            })

            in_trade = False

    trades_df = pd.DataFrame(trades)

    if trades_df.empty:
        return None

    # === Capital Curve ===
    trades_df["capital"] = initial_capital * (1 + trades_df["return_pct"]).cumprod()

    # === Metrics ===
    num_trades = len(trades_df)
    profitable_trades = (trades_df["return_pct"] > 0).sum()
    win_rate = profitable_trades / num_trades

    avg_days_per_trade = trades_df["days_held"].mean()

    final_equity = trades_df["capital"].iloc[-1]
    final_roi = (final_equity / initial_capital - 1) * 100

    running_max = trades_df["capital"].cummax()
    drawdown = (trades_df["capital"] - running_max) / running_max
    max_dd = drawdown.min() * 100

    sharpe = (
        trades_df["return_pct"].mean() /
        trades_df["return_pct"].std()
    ) * np.sqrt(num_trades) if trades_df["return_pct"].std() > 0 else 0

    return {
        "num_trades": num_trades,
        "profitable_trades": profitable_trades,
        "win_rate": win_rate,
        "avg_days_per_trade": avg_days_per_trade,
        "final_equity": final_equity,
        "final_roi_pct": final_roi,
        "max_drawdown_pct": max_dd,
        "sharpe": sharpe,
        "trades": trades_df
    }


def run_backtest_all_markets(df, initial_capital=1000):
    results = []

    for mkt, g in df.groupby("market_address"):
        g = g.sort_index()

        if len(g) < 40:
            continue

        res = backtest_pt_compression(g, initial_capital)

        if res is None:
            continue

        results.append({
            "market_address": mkt,
            "num_trades": res["num_trades"],
            "profitable_trades": res["profitable_trades"],
            "win_rate": res["win_rate"],
            "avg_days_per_trade": round(res["avg_days_per_trade"],0),
            "final_equity": res["final_equity"],
            "final_roi_pct": res["final_roi_pct"],
            #"max_drawdown_pct": res["max_drawdown_pct"],
            "sharpe": res["sharpe"]
        })

    return pd.DataFrame(results)




# In[45]:


summary_df = run_backtest_all_markets(df_asset, initial_capital=1000)

summary_df.sort_values("final_roi_pct", ascending=False)


# In[35]:


import matplotlib.pyplot as plt
import pandas as pd

for mkt, g in df_asset.groupby("market_address"):
    g = g.sort_index()

    # Extract maturity (assume same for all rows of this market)
    expiry = pd.to_datetime(g["expiry"].iloc[0])

    plt.figure(figsize=(14, 5))

    # --- Raw normalized yield gap ---
    plt.plot(
        g.index,
        g["yield_gap_norm"],
        label="Yield Gap (Z)",
        linewidth=2,
        alpha=0.8
    )

    # --- EMA(7) overlay ---
    plt.plot(
        g.index,
        g["ema_14"],
        label="EMA(14)",
        linewidth=2.5,
        color="orange"
    )

    # Reference lines
    plt.axhline(0, color="black", linewidth=1)
    plt.axhline(2, color="red", linestyle="--", alpha=0.6)
    plt.axhline(-2, color="red", linestyle="--", alpha=0.6)

    # Maturity vertical line
    plt.axvline(
        expiry,
        color="purple",
        linestyle=":",
        linewidth=2,
        label=f"Maturity: {expiry.date()}"
    )

    plt.title(f"Normalized Yield Gap — {asset_name} | {mkt[:6]}")
    plt.ylabel("Yield Gap (Z-score)")
    plt.xlabel("Time")
    plt.legend(fontsize=9)
    plt.grid(True)
    plt.tight_layout()
    plt.show()




# In[38]:


import matplotlib.pyplot as plt

def plot_trades_with_ema(df_mkt, asset_name="Asset"):
    df = df_mkt.copy().sort_index()

    Z = df["yield_gap_norm"]
    EMA = df["ema_14"]

       # === ENTRY CONDITIONS ===
    entry_cond = (
        (df["ema_14_slope"] < 0) &
        (Z > 0) &
        (Z < EMA * 0.98) &
        #(df["rolling_std_7d"] < df["rolling_std_14d"]) &
        (df["days_to_expiry"] >= 21)
    )

    # === EXIT CONDITIONS ===
    exit_cond = (
        (Z > EMA * 1.01) |
        #(Z < 0.25) |
        (df["days_to_expiry"] <= 1)
    )

    entries = []
    exits = []

    in_trade = False

    for t in range(1, len(df)):
        if not in_trade and entry_cond.iloc[t]:
            entries.append(df.index[t])
            in_trade = True

        elif in_trade and exit_cond.iloc[t]:
            exits.append(df.index[t])
            in_trade = False

    # === PLOT ===
    plt.figure(figsize=(14, 6))

    plt.plot(df.index, Z, label="Yield Gap (Z)", linewidth=2)
    plt.plot(df.index, EMA, label="EMA 14", linewidth=2, linestyle="--")

    plt.scatter(
        entries,
        Z.loc[entries],
        marker="^",
        color="green",
        s=80,
        label="Entry"
    )

    plt.scatter(
        exits,
        Z.loc[exits],
        marker="v",
        color="red",
        s=80,
        label="Exit"
    )

    plt.axhline(0, color="black", linewidth=1)
    plt.axhline(2, color="red", linestyle="--", alpha=0.4)
    plt.axhline(-2, color="red", linestyle="--", alpha=0.4)

    plt.title(f"{asset_name} | Market {df['market_address'].iloc[0][:6]}")
    plt.xlabel("Time")
    plt.ylabel("Normalized Yield Gap (Z)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# In[39]:


for mkt, g in df_asset.groupby("market_address"):
    plot_trades_with_ema(g, asset_name="USDf")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




