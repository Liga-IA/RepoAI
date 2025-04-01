# 📌 Predicting Student Scores Based on Study Hours  

## 🎯 Objective  
The goal is to predict a student's exam score based on the number of hours they studied. The idea is to determine whether there is a linear relationship between study time and academic performance.  

---

## 📊 Dataset  
We can use the **Students Performance Dataset**, available on [Kaggle](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams), or create a synthetic dataset for illustration.  

Example dataset structure:  

| Hours Studied | Exam Score |
|--------------|------------|
| 1.5          | 50         |
| 3.0          | 55         |
| 4.5          | 65         |
| 6.0          | 70         |
| 7.5          | 80         |
| 9.0          | 85         |

---

## 🔧 Implementation Using Python and Scikit-Learn  

Here, we implement a **Simple Linear Regression Model** to predict student scores based on study hours.  

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Creating a synthetic dataset
data = {'hours_studied': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'exam_score': [45, 50, 55, 60, 65, 70, 75, 85, 90, 95]}

df = pd.DataFrame(data)

# Defining independent (X) and dependent (y) variables
X = df[['hours_studied']]
y = df['exam_score']

# Splitting into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating and training the model
model = LinearRegression()
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Model evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Coefficient (Slope): {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")

# Plotting the results
plt.scatter(X, y, color='blue', label="Actual Data")
plt.plot(X, model.predict(X), color='red', linewidth=2, label="Linear Regression")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.legend()
plt.show()
