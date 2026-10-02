import csv, math
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss

SRC='PHASE56_HM8_EXACT_FUTURES.csv'
OUT='PHASE78_CLUSTER_BOOTSTRAP.csv'
rows=list(csv.DictReader(open(SRC,encoding='utf-8-sig')))
def fl(r,k):
    try:return float(r.get(k,''))
    except:return math.nan

base=[r for r in rows if r.get('base_frozen')=='True' and r.get('split') in ('D','V') and r.get('out2.0') in ('TARGET','STOP','TIME')]
D=[r for r in base if r['split']=='D']; V=[r for r in base if r['split']=='V']
DH=[r for r in D if r.get('h_m1','').lower()=='true']; VH=[r for r in V if r.get('h_m1','').lower()=='true']
G=['event_range_atr','close_loc20','priorret1','priorret3','priorret5','priorret10','priorret20','prior5dir','prior10dir']
def X(rs,cols): return np.array([[fl(r,c) for c in cols] for r in rs],float)
def fitpred(train,test,cols):
    y=np.array([1 if r['out2.0']=='TARGET' else 0 for r in train])
    m=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=4000)).fit(X(train,cols),y)
    return m.predict_proba(X(test,cols))[:,1]
yVH=np.array([1 if r['out2.0']=='TARGET' else 0 for r in VH])
pb=fitpred(DH,VH,G); pp=fitpred(DH,VH,G+['clip_pressure'])
days=sorted(set(r['dt'].split(' ')[0] for r in VH))
indices={d:[i for i,r in enumerate(VH) if r['dt'].split(' ')[0]==d] for d in days}
rng=np.random.default_rng(1702); vals=[]
for _ in range(10000):
    picks=rng.choice(days,size=len(days),replace=True)
    idx=np.concatenate([np.asarray(indices[d]) for d in picks])
    if len(np.unique(yVH[idx]))<2: continue
    vals.append((roc_auc_score(yVH[idx],pp[idx])-roc_auc_score(yVH[idx],pb[idx]),
                 brier_score_loss(yVH[idx],pp[idx])-brier_score_loss(yVH[idx],pb[idx])))
vals=np.asarray(vals)
with open(OUT,'w',newline='') as f:
    w=csv.writer(f); w.writerow(['comparison','observed_difference','ci_low_95','ci_high_95','bootstrap_p_le_zero','n_days','n_events'])
    w.writerow(['HM1 geometry + pressure vs HM1 geometry',float(roc_auc_score(yVH,pp)-roc_auc_score(yVH,pb)),float(np.quantile(vals[:,0],.025)),float(np.quantile(vals[:,0],.975)),float(np.mean(vals[:,0]<=0)),len(days),len(VH)])
    w.writerow(['HM1 geometry + pressure vs HM1 geometry (Brier change)',float(brier_score_loss(yVH,pp)-brier_score_loss(yVH,pb)),float(np.quantile(vals[:,1],.025)),float(np.quantile(vals[:,1],.975)),float(np.mean(vals[:,1]<=0)),len(days),len(VH)])
print('saved',OUT)
