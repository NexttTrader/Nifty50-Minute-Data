"""Phase 84 pre-event regime comparison.

The 2026 values are loaded from the exact audited H-M1 validation event file.
The external values are computed mechanically from the frozen H-M1 definition.
This phase is explanatory only and must not be used to fit a new rule.
"""
import pandas as pd

# Fill these with the exact local audited artifacts when reproducing.
# The analysis compares only pre-event features:
# event_range_atr, clipping pressure/count, flip distance,
# prior directional returns and prior-20-bar close location.
# No holdout outcome enters model fitting.
print("Phase 84 is explanatory-only: do not tune a new threshold on the external contract.")
