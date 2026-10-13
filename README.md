# Interpretable Heart Disease Classification

An educational comparison of RuleFit, Fast Interpretable Greedy Tree Sums (FIGS), and CART on a heart-related binary classification dataset.

## Analytical value
Compare predictive performance with readable rules and tree structures. This demonstrates model evaluation and communication of accuracy–interpretability tradeoffs.

## Technical strengths
Python, Pandas, scikit-learn, imodels, Matplotlib, and Graphviz.
Training/test separation, scaling fitted on the training set, classification reports, confusion matrices, extracted rules, and ROC analysis.

## Saved results
| Model | Test accuracy | ROC-AUC |
| --- | --- | --- |
| RuleFit | 82.42% | Not reported |
| FIGS | 79.12% | 0.8685 |
| CART | Approximately 71% | Not reported |

These are saved outputs from one 70/30 split with random_state=42 and 91 test observations. They have not been reproduced in a clean environment.

## Explore and run
The repository includes heart.csv and [the notebook](interpretable_heart_disease.ipynb). Use the included CSV instead of the personal Google Drive path. Install the imported dependencies, correct the course-template setup paths, and run the notebook in order.

## Limitations and next steps
- Verify the original dataset source, class labels, and whether the target represents heart disease or another endpoint.
- Remove unused custom RuleFit code; the executed model uses the library's RuleFitClassifier.
- Add repeated or stratified validation and show rules with actual feature names and units.
- Pin dependencies and clean the initialization cells.

## Project context
Developed by Yiren Shen for Duke's AIPI 590 Explainable AI course. This is a teaching project; clinical performance and deployment have not been established.
