import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path('/mnt/data/phase84')
EVENTS = BASE / 'SALMA_HM1_EXACT_AUDITED_EVENTS_APR_SEP_2026.csv'
FUT = BASE / 'NIFTY_FUT_5m_all_contracts_normalized.csv'
OUT = BASE / 'out'
OUT.mkdir(parents=True, exist_ok=True)

def thin_same_session(x: pd.DataFrame, cooldown_bars: int) -> pd.DataFrame:
    if cooldown_bars <= 0:
        return x.copy()
    keep, last = [], {}
    for idx, r in x.sort_values(['tradingsymbol','date','bar_index']).iterrows():
        key = (r.tradingsymbol, r.date)
        prev = last.get(key)
        if prev is None or r.bar_index - prev >= cooldown_bars:
            keep.append(idx)
            last[key] = r.bar_index
    return x.loc[keep].copy()

def bootstrap_day_block_delta(z: pd.DataFrame, B: int = 30000, seed: int = 8404):
    z = z[z.label.isin(['H-M6','CONTROL'])].copy()
    g = z.groupby(['date','label']).ret20atr.agg(['sum','count']).unstack(fill_value=0)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(g), size=(B, len(g)))
    h = g['sum']['H-M6'].to_numpy()[idx].sum(1) / g['count']['H-M6'].to_numpy()[idx].sum(1)
    c = g['sum']['CONTROL'].to_numpy()[idx].sum(1) / g['count']['CONTROL'].to_numpy()[idx].sum(1)
    vals = h - c
    return float(vals.mean()), float(np.quantile(vals, .025)), float(np.quantile(vals, .975)), float(np.mean(vals <= 0))

def main():
    e = pd.read_csv(EVENTS)
    f = pd.read_csv(FUT)
    e['datetime'] = pd.to_datetime(e['datetime'])
    f['datetime'] = pd.to_datetime(f['datetime'])
    e = e[e['split'] == 'V'].copy()
    f = f.sort_values(['tradingsymbol','datetime']).copy()
    f['bar_index'] = f.groupby('tradingsymbol').cumcount()
    e = e.merge(f[['tradingsymbol','datetime','bar_index']], on=['tradingsymbol','datetime'], how='left', validate='one_to_one')
    if e['bar_index'].isna().any():
        raise RuntimeError('At least one validation event did not map to its exact futures bar.')
    e['date'] = e['datetime'].dt.date
    e['label'] = np.where(e['h_m6'], 'H-M6', np.where(~e['h_m1'], 'CONTROL', 'H-M1-not6'))
    e = e.sort_values(['tradingsymbol','date','bar_index']).reset_index(drop=True)
    e['gap_from_prev_event_same_contract'] = e.groupby('tradingsymbol').bar_index.diff()
    e['same_day_prev_gap'] = np.where(e.date.eq(e.groupby('tradingsymbol').date.shift()), e.gap_from_prev_event_same_contract, np.nan)

    spacing_rows=[]
    for grp in ['H-M6','CONTROL']:
        g=e[e.label==grp]['same_day_prev_gap'].dropna()
        spacing_rows.append({'group':grp,'n_events_validation':len(e[e.label==grp]),'median_same_day_gap_bars':g.median(),'mean_same_day_gap_bars':g.mean(),'pct_gap_le_5':(g<=5).mean(),'pct_gap_le_10':(g<=10).mean(),'pct_gap_le_20':(g<=20).mean()})
    pd.DataFrame(spacing_rows).to_csv(OUT/'PHASE84_EVENT_SPACING.csv', index=False)

    rows=[]
    for cd in [0,5,10,20,30]:
        z = thin_same_session(e, cd)
        h=z[z.label=='H-M6']; c=z[z.label=='CONTROL']
        point=h.ret20atr.mean()-c.ret20atr.mean()
        meanb, lo, hi, p = bootstrap_day_block_delta(z)
        rows.append({'cooldown_bars_same_session':cd,'H_M6_n':len(h),'CONTROL_n':len(c),'H_M6_ret20_mean':h.ret20atr.mean(),'CONTROL_ret20_mean':c.ret20atr.mean(),'ret20_delta_ATR':point,'day_block_boot_mean':meanb,'day_block_CI95_lo':lo,'day_block_CI95_hi':hi,'P_delta_le_0':p,'H_M6_median':h.ret20atr.median(),'CONTROL_median':c.ret20atr.median(),'H_M6_10pct_trimmed_mean':h.ret20atr.sort_values().iloc[int(.1*len(h)):int(.9*len(h))].mean() if len(h)>=10 else np.nan})
        z.to_csv(OUT/f'PHASE84_VALIDATION_EVENTS_CD{cd}.csv', index=False)
    pd.DataFrame(rows).to_csv(OUT/'PHASE84_COOLDOWN_ROBUSTNESS.csv', index=False)

    z=e[e.label.isin(['H-M6','CONTROL'])].copy()
    d=z.groupby(['date','label']).ret20atr.mean().unstack().dropna()
    daily=(d['H-M6']-d['CONTROL']).rename('daily_delta')
    trim=daily.sort_values().iloc[int(.1*len(daily)):int(.9*len(daily))]
    pd.DataFrame([{'common_days':len(daily),'equal_day_mean_delta_ATR':daily.mean(),'equal_day_median_delta_ATR':daily.median(),'positive_day_share':(daily>0).mean(),'equal_day_10pct_trimmed_delta_ATR':trim.mean()}]).to_csv(OUT/'PHASE84_MATCHED_DAY_ROBUSTNESS.csv',index=False)
    daily.to_csv(OUT/'PHASE84_MATCHED_DAY_VALUES.csv', index=True, header=True)
    e.to_csv(OUT/'PHASE84_EVENT_SPACING_AUDIT.csv', index=False)

if __name__ == '__main__':
    main()
