import json
import csv
from datetime import datetime, timedelta

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    raise ImportError("pip install yfinance pandas")


def fetch(ticker, days=365):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data for {ticker}")
    return df["Close"].squeeze()


def sma_crossover(prices, short=20, long=50):
    df = pd.DataFrame({"price": prices})
    df["sma_short"] = df["price"].rolling(short).mean()
    df["sma_long"] = df["price"].rolling(long).mean()
    df.dropna(inplace=True)

    position = 0
    entry = 0.0
    trades = []

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        date = df.index[i]

        if prev["sma_short"] <= prev["sma_long"] and curr["sma_short"] > curr["sma_long"]:
            if position == 0:
                position = 1
                entry = curr["price"]
                trades.append({"date": str(date.date()), "action": "BUY", "price": round(float(curr["price"]), 2)})

        elif prev["sma_short"] >= prev["sma_long"] and curr["sma_short"] < curr["sma_long"]:
            if position == 1:
                position = 0
                pnl = (curr["price"] - entry) / entry * 100
                trades.append({"date": str(date.date()), "action": "SELL", "price": round(float(curr["price"]), 2), "pnl_pct": round(float(pnl), 2)})
                entry = 0.0

    # close open position at last price
    if position == 1:
        last_price = float(df.iloc[-1]["price"])
        pnl = (last_price - entry) / entry * 100
        trades.append({"date": str(df.index[-1].date()), "action": "SELL(open)", "price": round(last_price, 2), "pnl_pct": round(float(pnl), 2)})

    first = float(df.iloc[0]["price"])
    last = float(df.iloc[-1]["price"])
    bah = (last - first) / first * 100

    strategy_return = sum(t.get("pnl_pct", 0) for t in trades if "pnl_pct" in t)
    n_trades = sum(1 for t in trades if t["action"].startswith("SELL"))

    return {
        "ticker": None,
        "short_window": short,
        "long_window": long,
        "trades": trades,
        "n_trades": n_trades,
        "strategy_return_pct": round(strategy_return, 2),
        "buy_and_hold_pct": round(bah, 2),
        "start": str(df.index[0].date()),
        "end": str(df.index[-1].date()),
    }


def run(ticker, short=20, long=50, days=365):
    prices = fetch(ticker, days)
    result = sma_crossover(prices, short, long)
    result["ticker"] = ticker.upper()
    return result


def to_csv(result, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "action", "price", "pnl_pct"])
        w.writeheader()
        for t in result["trades"]:
            w.writerow({k: t.get(k, "") for k in ["date", "action", "price", "pnl_pct"]})


def to_json(result, path):
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
