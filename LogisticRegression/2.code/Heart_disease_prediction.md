# English version
## What is logistic regression?
&nbsp;&nbsp;&nbsp;&nbsp; Logistic regression is one of the most widely used algorithms due to its simplicity and versatility, and it is extensively applied to solve classification problems.
&nbsp;&nbsp;&nbsp;&nbsp; It is a type of statistical model that estimates the probability of an event occuring. Since the model analises a probability the output is a number between zero and one. 
## Logistic Regression to predict heart disease 
### Objective   
The 'TenYearCHD' column in the Framingham dataset is the target variable of the study, meaning it is what the machine learning model aims to predict based on risk factors such as age, blood pressure, cholesterol, smoking, diabetes, etc. It is a binary classification task: predicting whether a person will develop CHD within 10 years.  
### Importing Libraries 

```python 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
```
- `pandas` - data analysis and manipulation.

- `train_test_split` - splits data into training and test sets.

- `LogisticRegression` - class for the Logistic Regression model.

- `seaborn` - data visualization library based on matplotlib.

- `matplotlib.pyplot` - core library for plotting.

- `confusion_matrix` - evaluates the performance of classification models.

### Creating/Loading the Dataset
```python 
ds = pd.read_csv("/content/framingham.csv")
ds.head()
```
<img src="https://i.postimg.cc/85LV9MRT/Captura-de-tela-2025-05-05-222415.png" alt="heart_disease" width="500">

<[Dataset in this example](https://www.kaggle.com/datasets/dileep070/heart-disease-prediction-using-logistic-regression/data)>   

```python 
ds = ds.dropna(subset=['TenYearCHD', 'glucose', 'heartRate', 'male', 'age',	'education',	'currentSmoker',	'cigsPerDay',	'BPMeds',	'prevalentStroke',	'prevalentHyp', 'diabetes',	'totChol',	'sysBP',	'diaBP',	'BMI'])
```
### Removing the lines containing colunms with empty values on dataset using panda library

```python 
y = ds.iloc[:, 15].values
X = ds.iloc[:, 0:15].values
X, y
```
<img src="https://i.postimg.cc/jqwrpVhM/Captura-de-tela-2025-05-05-222837.png" alt="heart_disease" width="400">

### Defining the column 'TenYearCHD' as the output, and the others as input (predictor variables).

```python 
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=.3)
```

### Splitting the dataset into 30% for testing and 70% for training

```python 
modelo = LogisticRegression()
modelo.fit(X_treino, y_treino)
```

### Creating and Training the Model

```python 
previsoes = modelo.predict(X_teste)
```
### Making Predictions

```python 
modelo.score(X_teste, y_teste)
```
<img src="https://i.postimg.cc/52tgrJB0/Captura-de-tela-2025-05-05-222957.png" alt="heart_disease" width="300">

### Calculating accuracy

```python 
sns.countplot(data=ds, x='TenYearCHD')
plt.xticks([0, 1], ['Não teve CHD', 'Teve CHD'])
plt.title('Distribuição de Doença Cardíaca em 10 Anos')
plt.xlabel('TenYearCHD')
plt.ylabel('Número de Pessoas')
plt.show()
```
<img src="https://i.postimg.cc/9X4qKS9b/bf17e336-f42a-40c0-a3f9-e9c71726858f.jpg" alt="heart_disease" width="400">

### Plotting the count plot, showing how many people had or did not have heart disease in 10 years.
```python 
cm = confusion_matrix(y_teste, previsoes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Previsto')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.show()
```
<img src="https://i.postimg.cc/wxkSKfdt/14d309ce-bd94-421a-b494-61aa8386adb6.jpg" alt="heart_disease" width="400">

### Plotting the confusion matrix graph, showing the number of correct and incorrect predictions.

### References
- <[Logistic Regression](https://www.web.stanford.edu/~jurafsky/slp3/5.pdf)>. Acess 02 may 2025 
- <[What is logistic regression?](https://www.ibm.com/think/topics/logistic-regression)>. Acess 02 may 2025   


