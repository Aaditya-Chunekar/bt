# bt

Minimal SMA crossover backtester. CLI tool + importable library.

## Install

```sh
pip install -e .
```

## Usage

```sh
# basic
bt AAPL

# custom windows + lookback
bt ^NSEI -s 10 -l 30 -d 730

# dump output
bt MSFT --csv trades.csv --json result.json
```

## Library

```python
from bt.core import run, to_csv, to_json

r = run("AAPL", short=20, long=50, days=365)
print(r["strategy_return_pct"], r["buy_and_hold_pct"])
to_csv(r, "trades.csv")
to_json(r, "result.json")
```

## Output

```
AAPL  SMA(20,50)  2024-01-15 → 2025-01-14

  2024-03-01  BUY            170.42
  2024-05-12  SELL           182.91   +7.32%
  ...

  trades          4
  strategy return +11.20%
  buy & hold      +23.41%
  edge            -12.21%
```
