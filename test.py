from bt.core import run, to_csv, to_json

r = run("AAPL", short=20, long=50, days=365)
print(r["strategy_return_pct"], r["buy_and_hold_pct"])
to_csv(r, "trades.csv")
to_json(r, "result.json")