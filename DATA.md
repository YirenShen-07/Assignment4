# Source audit and data dictionary

Original source: [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease), Cleveland subset. The original course notebook cited [Naresh Bhat's Kaggle mirror](https://www.kaggle.com/datasets/nareshbhat/health-care-data-set-on-heart-attack-possibility).

verify_labels.py matches all 303 bundled rows to the original processed Cleveland records using age, sex, resting BP, cholesterol, fasting glucose indicator, maximum heart rate, exercise angina and ST depression. The audit found an unambiguous inverse target mapping for every row. The unchanged original and bundled byte fingerprints are recorded in reports/label_audit.json.

UCI num=0 means absence; num=1,2,3,4 mean presence. Bundled target=1 corresponds to absence and target=0 to presence. analyze.py uses disease_present=1-target. The bundled CSV is retained unchanged for traceability.

| Field | Bundled coding or unit |
| --- | --- |
| age | years |
| sex | 0=female, 1=male, per original dataset coding |
| cp | 0=UCI 4 asymptomatic; 1=UCI 2 atypical angina; 2=UCI 3 non-anginal pain; 3=UCI 1 typical angina |
| trestbps | resting blood pressure, mm Hg |
| chol | serum cholesterol, mg/dL |
| fbs | 1 if fasting glucose exceeds 120 mg/dL |
| restecg | 0=UCI 2 LV-hypertrophy coding; 1=UCI 0 normal; 2=UCI 1 ST-T abnormality coding |
| thalach | maximum heart rate achieved, bpm |
| exang | exercise-induced angina, 0/1 |
| oldpeak | ST depression relative to rest |
| slope | 0=UCI 3 downsloping; 1=UCI 2 flat; 2=UCI 1 upsloping |
| ca | number of vessels; bundled 4 corresponds to UCI missing '?' and is imputed |
| thal | 1=UCI 6 fixed defect; 2=UCI 3 normal; 3=UCI 7 reversible defect; bundled 0 corresponds to UCI missing '?' |

Categorical fields remain encoded categories, not measurements on a meaningful continuous scale. Classification describes disease presence in this benchmark; it does not estimate future heart-attack risk.

Model references: [imodels](https://csinva.io/imodels/), [scikit-learn trees](https://scikit-learn.org/stable/modules/tree.html).
