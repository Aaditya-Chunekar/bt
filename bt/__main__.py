#!/usr/bin/env python3
import argparse
import sys
from bt.core import run, to_csv, to_json

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"


def fmt_pnl(v):
    c = GREEN if v >= 0 else RED
    sign = "+" if v >= 0 else ""
    return f"{c}{sign}{v:.2f}%{RESET}"


def print_result(r):
    print(f"\n{BOLD}{r['ticker']}{RESET}  SMA({r['short_window']},{r['long_window']})  {DIM}{r['start']} → {r['end']}{RESET}\n")
    for t in r["trades"]:
        if t["action"].startswith("SELL"):
            pnl_str = fmt_pnl(t["pnl_pct"])
            print(f"  {DIM}{t['date']}{RESET}  {t['action']:<10}  {t['price']:>10.2f}  {pnl_str}")
        else:
            print(f"  {DIM}{t['date']}{RESET}  {t['action']:<10}  {t['price']:>10.2f}")

    print()
    print(f"  trades          {r['n_trades']}")
    print(f"  strategy return {fmt_pnl(r['strategy_return_pct'])}")
    print(f"  buy & hold      {fmt_pnl(r['buy_and_hold_pct'])}")
    edge = r["strategy_return_pct"] - r["buy_and_hold_pct"]
    print(f"  edge            {fmt_pnl(edge)}")
    print()


def main():
    p = argparse.ArgumentParser(prog="bt", description="SMA crossover backtester")
    p.add_argument("ticker", help="ticker symbol, e.g. AAPL or ^NSEI")
    p.add_argument("-s", "--short", type=int, default=20, metavar="N", help="short SMA window (default 20)")
    p.add_argument("-l", "--long", type=int, default=50, metavar="N", help="long SMA window (default 50)")
    p.add_argument("-d", "--days", type=int, default=365, metavar="N", help="lookback days (default 365)")
    p.add_argument("--csv", metavar="FILE", help="dump trades to CSV")
    p.add_argument("--json", metavar="FILE", help="dump full result to JSON")
    args = p.parse_args()

    try:
        r = run(args.ticker, args.short, args.long, args.days)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    print_result(r)

    if args.csv:
        to_csv(r, args.csv)
        print(f"trades written to {args.csv}")
    if args.json:
        to_json(r, args.json)
        print(f"result written to {args.json}")


if __name__ == "__main__":
    main()
