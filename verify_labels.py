"""Audit the bundled CSV against the original Cleveland data; do not trust a mirror's target prose."""
from pathlib import Path
from urllib.request import urlopen
import hashlib, io, json
import pandas as pd
URL='https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
COLS=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','num']
KEYS=['age','sex','trestbps','chol','fbs','thalach','exang','oldpeak']
def verify():
    with urlopen(URL,timeout=60) as response: raw=response.read()
    original=pd.read_csv(io.BytesIO(raw),header=None,names=COLS,na_values='?')
    local=pd.read_csv(Path(__file__).parent/'heart.csv')
    matches=local.reset_index(names='row').merge(original[KEYS+['num']],on=KEYS,how='left')
    if len(matches)!=len(local) or matches['num'].isna().any():
        raise ValueError('Cannot establish an unambiguous match for every row')
    agreement=float(((1-matches['target'])==(matches['num']>0).astype(int)).mean())
    if agreement!=1:
        raise ValueError('Target inversion is not confirmed for all rows')
    result={'rows_matched':len(matches),'inverted_target_agreement':agreement,
            'original_source':URL,'original_sha256':hashlib.sha256(raw).hexdigest(),
            'bundled_sha256':hashlib.sha256((Path(__file__).parent/'heart.csv').read_bytes()).hexdigest(),
            'mapping':'bundled target 1 = UCI num 0 (absence); bundled target 0 = UCI num >0 (presence)',
            'analysis_target':'disease_present = 1 - bundled target'}
    out=Path(__file__).parent/'reports';out.mkdir(exist_ok=True)
    (out/'label_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return result
if __name__=='__main__':verify()
