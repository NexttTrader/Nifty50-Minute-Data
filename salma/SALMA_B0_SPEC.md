# SALMA-B0 Frozen Specification

Source: user-supplied RedK SALMA v3.0 Pine code.

Parameters:
- Source: Close
- Length: 10
- Smooth: 3
- Width / Mult: 0.30
- SD Length: 5

Formula:
1. baseline = WMA(close, 5)
2. dev = 0.30 * stdev(close, 5)
3. clip close to baseline +/- dev
4. REMA = WMA(WMA(clipped close, 10), 3)
5. SALMA state = REMA > REMA[1]
6. SwingUp/Down are confirmed changes in SALMA slope state.

Research uses close-confirmed events to avoid realtime/historical ambiguity.
No parameter changes are permitted during validation of a frozen hypothesis.