# bt

Minimal SMA crossover backtester. CLI tool + importable library.

## Install

```sh
git clone https://github.com/Aaditya-Chunekar/bt
pip install -e .
```

## Project layout

```
bt/
  __init__.py
  __main__.py
  core.py
pyproject.toml
README.md
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

## CLI help

```sh
bt --help
```

```
usage: bt [-h] [-s N] [-l N] [-d N] [--csv FILE] [--json FILE] ticker

SMA crossover backtester

positional arguments:
  ticker         ticker symbol, e.g. AAPL or ^NSEI

options:
  -h, --help     show this help message and exit
  -s, --short N  short SMA window (default 20)
  -l, --long N   long SMA window (default 50)
  -d, --days N   lookback days (default 365)
  --csv FILE     dump trades to CSV
  --json FILE    dump full result to JSON
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
NVDA  SMA(20,50)  2025-06-24 → 2026-04-10

  2025-10-03  BUY             187.60
  2025-12-02  SELL            181.44  -3.28%
  2026-01-15  BUY             187.04
  2026-03-02  SELL            182.47  -2.44%
  2026-03-06  BUY             177.81
  2026-03-10  SELL            184.76  +3.91%

  trades          3
  strategy return -1.81%
  buy & hold      +27.56%
  edge            -29.37%
```
