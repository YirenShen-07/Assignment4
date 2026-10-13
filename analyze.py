"""Compare interpretable classifiers on the bundled Cleveland-derived records."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, ConfusionMatrixDisplay, RocCurveDisplay
from imodels import RuleFitClassifier, FIGSClassifier
ROOT=Path(__file__).parent
LABELS={'age':'Age (years)','sex':'Sex (encoded)','cp':'Chest pain (encoded)','trestbps':'Resting BP (mm Hg)','chol':'Cholesterol (mg/dL)',
        'fbs':'Fasting glucose >120 mg/dL','restecg':'Resting ECG (encoded)','thalach':'Max heart rate (bpm)','exang':'Exercise angina (0/1)',
        'oldpeak':'ST depression','slope':'ST slope (encoded)','ca':'Vessels (encoded)','thal':'Stress test (encoded)'}
def run():
    data=pd.read_csv(ROOT/'heart.csv')
    rows_before=len(data);data=data.drop_duplicates()
    X=data.drop(columns='target');y=1-data['target']
    # These mirror codes correspond to '?' in the original Cleveland file.
    X.loc[X['ca']==4,'ca']=np.nan
    X.loc[X['thal']==0,'thal']=np.nan
    train,test,y_train,y_test=train_test_split(X,y,test_size=.3,stratify=y,random_state=42)
    estimators={'Majority baseline':DummyClassifier(strategy='most_frequent'),
            'RuleFit':RuleFitClassifier(n_estimators=100,tree_size=4,max_rules=20,random_state=42),
            'FIGS':FIGSClassifier(max_rules=12,random_state=42),
            'CART':DecisionTreeClassifier(max_depth=4,min_samples_leaf=5,random_state=42)}
    models={name:make_pipeline(SimpleImputer(strategy='most_frequent'),estimator) for name,estimator in estimators.items()}
    out=ROOT/'reports';out.mkdir(exist_ok=True);rows=[]
    cv=StratifiedKFold(n_splits=3,shuffle=True,random_state=42)
    fig,ax=plt.subplots(figsize=(7,5))
    for name,model in models.items():
        aucs=cross_val_score(model,train.to_numpy(),y_train,cv=cv,scoring='roc_auc')
        if name in ['RuleFit','FIGS']:
            step=list(model.named_steps)[-1]
            model.fit(train.to_numpy(),y_train.to_numpy(),**{step+'__feature_names':list(train.columns)})
        else:model.fit(train.to_numpy(),y_train)
        prob=model.predict_proba(test.to_numpy())[:,1];pred=(prob>=.5).astype(int)
        rows.append({'Model':name,'Accuracy':accuracy_score(y_test,pred),'Disease precision':precision_score(y_test,pred,zero_division=0),
            'Disease recall':recall_score(y_test,pred,zero_division=0),'Disease F1':f1_score(y_test,pred,zero_division=0),
            'ROC-AUC':roc_auc_score(y_test,prob),'Train CV AUC mean':aucs.mean(),'Train CV AUC std':aucs.std(ddof=1)})
        if name!='Majority baseline':RocCurveDisplay.from_predictions(y_test,prob,name=name,ax=ax)
    ax.plot([0,1],[0,1],ls='--',color='gray');ax.set_title('Held-out ROC — disease presence is the positive class');fig.tight_layout();fig.savefig(out/'roc_comparison.png',dpi=160);plt.close(fig)
    metrics=pd.DataFrame(rows).set_index('Model');metrics.to_csv(out/'metrics.csv')
    fig,ax=plt.subplots(figsize=(18,8));plot_tree(estimators['CART'],max_depth=3,feature_names=[LABELS[c].replace(' (','\n(') for c in X],class_names=['Absent','Present'],filled=True,rounded=True,fontsize=8,ax=ax);ax.set_title('CART: named features and original units (first 3 levels; complete rules exported)');fig.tight_layout();fig.savefig(out/'cart_rules.png',dpi=140);plt.close(fig)
    (out/'cart_rules.txt').write_text(export_text(estimators['CART'],feature_names=list(X.columns)))
    (out/'figs_rules.txt').write_text(str(estimators['FIGS'])+'\n')
    rulefit=estimators['RuleFit']
    if hasattr(rulefit,'_get_rules'):
        rules=rulefit._get_rules();rules=rules.loc[rules['coef']!=0];rules.to_csv(out/'rulefit_rules.csv',index=False)
    fig,ax=plt.subplots(figsize=(5,4));ConfusionMatrixDisplay.from_predictions(y_test,models['RuleFit'].predict(test.to_numpy()),display_labels=['Absent','Present'],cmap='Blues',colorbar=False,ax=ax);ax.set_title('RuleFit — 91 held-out records');fig.tight_layout();fig.savefig(out/'confusion_matrix.png',dpi=160);plt.close(fig)
    (out/'run.json').write_text(json.dumps({'seed':42,'split':'stratified 70/30','original_rows':rows_before,'deduplicated_rows':len(data),'removed_duplicates':rows_before-len(data),
      'train_rows':len(train),'test_rows':len(test),'target':'1 - bundled target; 1 means UCI disease presence','CV':'3 stratified folds on training rows only',
      'features':'original units; ca=4 and thal=0 treated as missing; imputer fitted inside each training fold; fixed hyperparameters'},indent=2)+'\n')
    print(metrics.round(4).to_string());return metrics
if __name__=='__main__':run()
