# Duke-AI-XAI-Assignment4
This dataset is a Heart attack possibility dataset containing the health status and test results of a number of patients, with the ultimate goal of predicting whether or not they have heart disease (represented by the Target column).

### Attribute Information
1) age
2) sex
3) chest pain type(4 values:0--No chest pain/1--Typical angina/2--Atypical angina/3--Non-anginal pain)
4) trestbps: resting blood pressure
5) chol: serum cholestoral in mg/dl
6) fbs: fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
7) restecg: resting electrocardiographic results (values 0,1,2)
8) thalach: maximum heart rate achieved
9) exang: exercise induced angina
10) oldpeak: ST depression induced by exercise relative to rest
11) slope: the slop of the peak exercise ST segment
12) ca: number of major vessels (0-3) colored by flourosopy
13) thal: 0 = normal; 1 = fixed defect; 2 = reversable defect
14) **target**: The target variable, 0= less chance of heart attack 1= more chance of heart attack

### Model
In this project, I first preprocessed the dataset to ensure that each feature data type was appropriate, missing values were handled, and the dataset was divided into a training set and a test set. To predict the likelihood of a heart attack, I used three methods from the imodels library: the **RuleFit rule set**, **Greedy tree sums (FIGS)**, and **Greedy rule tree (CART)**.

**RuleFit rule set:** RuleFit is an algorithm that combines linear models and decision rules. I train the linear model by extracting decision rules from the training data and adding these rules as new features to the original data. With this approach, an easily interpretable model output is obtained while incorporating the regularized representation of decision trees.

**Greedy tree sums (FIGS):** FIGS (Fast Interpretable Greedy Tree Sums) is a fast and easy-to-interpret algorithm that uses a greedy algorithm to construct multiple decision trees and sum their predictions. I chose this algorithm because it strikes a balance between complexity and interpretability.FIGS is able to provide a high level of accuracy while keeping the model simple and interpretable, making each prediction step of the model traceable.

**Greedy rule tree (CART):** CART (Classification and Regression Trees) is a classical decision tree algorithm that recursively splits the dataset by a greedy algorithm in order to minimize the classification error. It generates a tree model that directly explains how each prediction was made.The CART model is particularly effective in dealing with this binary classification task and is suitable for exploring the effect of each health characteristic on heart disease risk.


.


