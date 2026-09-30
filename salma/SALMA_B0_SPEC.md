# SALMA-B0 Frozen Specification

Source: user-supplied RedK SALMA v3.0 Pine code.

## Parameters
- Source: Close
- Length: 10
- Smooth: 3
- Width / Mult: 0.30
- SD Length: 5

## Exact formula
1. baseline = WMA(close, 5)
2. dev = 0.30 * ta.stdev(close, 5)
3. cprice = close clipped to [baseline - dev, baseline + dev]
4. REMA = WMA(WMA(cprice, 10), 3)
5. SALMA state = REMA > REMA[1]
6. SwingUp = state changes false -> true on a confirmed bar
7. SwingDn = state changes true -> false on a confirmed bar

## Pine semantic audit
TradingView documents the optional biased argument of ta.stdev as defaulting to true, which is the population-style estimator. The research reconstruction therefore uses rolling population standard deviation (ddof=0). Earlier sample-standard-deviation exploratory artifacts are superseded.

TradingView documents ta.wma as the built-in weighted moving average. The research implementation uses standard descending WMA weights.

## Signal policy
Research signals are evaluated only after candle close. Intrabar state changes are not treated as confirmed trading events.

## Governance
SALMA-B0 parameters are frozen during validation of H-M1/H-M6. Any alternative parameterization is a separate experiment and cannot overwrite B0 results.
