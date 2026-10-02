import csv, math, os
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss

SRC='PHASE56_HM8_EXACT_FUTURES.csv'
OUTDIR='phase78_out'
os.makedirs(OUTDIR, exist_ok=True)

with open(SRC, newline='', encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))

def fl(r,k):
    try: return float(r.get(k,''))
    except: return math.nan

for r in rows:
    r['_split']=r.get('split','').strip()
    r['_h1']=r.get('h_m1','').strip().lower() in ('true','1')
    r['hm1_num']='1' if r['_h1'] else '0'
    r['_y2']=1 if r.get('out2.0','').strip()=='TARGET' else 0 if r.get('out2.0','').strip() in ('STOP','TIME') else None

base=[r for r in rows if r.get('base_frozen','').strip()=='True' and r['_split'] in ('D','V') and r['_y2'] is not None]
D=[r for r in base if r['_split']=='D']; V=[r for r in base if r['_split']=='V']
G=['event_range_atr','close_loc20','priorret1','priorret3','priorret5','priorret10','priorret20','prior5dir','prior10dir']

def X(rs, cols):
    return np.array([[fl(r,c) for c in cols] for r in rs], dtype=float)

yD=np.array([r['_y2'] for r in D]); yV=np.array([r['_y2'] for r in V])

models={
    'geometry_only':G,
    'geometry_plus_HM1':G+['hm1_num'],
    'geometry_plus_HM1_pressure':G+['hm1_num','clip_pressure'],
    'geometry_plus_HM1_clipcount':G+['hm1_num','clip_count'],
    'geometry_plus_HM1_all_SALMA_context':G+['hm1_num','clip_pressure','clip_count','flip_dist'],
}
results=[]
for name,cols in models.items():
    m=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=4000))
    m.fit(X(D,cols),yD); p=m.predict_proba(X(V,cols))[:,1]
    results.append((name,len(D),len(V),float(yD.mean()),float(yV.mean()),float(roc_auc_score(yV,p)),float(brier_score_loss(yV,p)),len(cols)))

DH=[r for r in D if r['_h1']]; VH=[r for r in V if r['_h1']]
yDH=np.array([r['_y2'] for r in DH]); yVH=np.array([r['_y2'] for r in VH])
for name,cols in {
    'HM1_geometry_only':G,
    'HM1_geometry_plus_pressure':G+['clip_pressure'],
    'HM1_geometry_plus_clipcount':G+['clip_count'],
    'HM1_geometry_plus_pressure_count':G+['clip_pressure','clip_count']
}.items():
    m=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=4000))
    m.fit(X(DH,cols),yDH); p=m.predict_proba(X(VH,cols))[:,1]
    results.append((name,len(DH),len(VH),float(yDH.mean()),float(yVH.mean()),float(roc_auc_score(yVH,p)),float(brier_score_loss(yVH,p)),len(cols)))

with open(os.path.join(OUTDIR,'PHASE78_GEOMETRY_MODEL_RESULTS.csv'),'w',newline='') as f:
    w=csv.writer(f); w.writerow(['model','train_n','test_n','train_base_rate','test_base_rate','auc','brier','feature_count']); w.writerows(results)
print('saved', os.path.join(OUTDIR,'PHASE78_GEOMETRY_MODEL_RESULTS.csv'))
