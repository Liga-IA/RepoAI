# SVM Variants
[![image.png](https://i.postimg.cc/pXjjvwZ8/image.png)](https://postimg.cc/56xyqkDN)

This term refers to the entire family of algorithms. It is consider to be a versatile machine learning algorithm because it can handle both **classification** and **regression** problems.
The two algorithm to solve the problems mentions are:
- Support Vector Classifier (SVC): Used when the target variable consists of discrete class labels. For example, classifying if a person may have diabetes or not. [Diabetes dataset](https://www.kaggle.com/datasets/akshaydattatraykhare/diabetes-dataset).
- Support Vector Regressor (SVR): Used when the target variable is continuous. For example predicting house prices. [House price prediction dataset](https://www.kaggle.com/datasets/zafarali27/house-price-prediction-dataset)

[![image.png](https://i.postimg.cc/9Mj8P6BS/image.png)](https://postimg.cc/McdmqrNb)

## Support Vector Classifier (SVC)
In a context of binary classification, where the target **y** has two classes, like **logistic regression**, SVC try to find the best fit line (decision boundary) to separate the two classes.   

[![image.png](https://i.postimg.cc/PNG9cCW0/image.png)](https://postimg.cc/RJRgJVbT)

But it's worth mentioning, that this classification algorithm has an addicional concept, which is **marginal planes**. We can see them on the picture bellow, the dotted red line placed on each side of the best fit line, equidistant from it.

[![image.png](https://i.postimg.cc/8PjLXycx/image.png)](https://postimg.cc/xcVkc3KP)

The main goal of SVC is to maximize the distance between this two dotted red line. And the datapoints (orange and green circles) that lie on them are called **support vectors**. Here is where the name comes from, they are crucial because they _support_ the position and orientation of the best fit line.

## Support Vector Regression (SVR)

This variant of SVM is used for regression problems, when we want to predict a continuos output. For example, the algorithm has to analyse the features of a dataset to give an estimeted value for the target - like area of the house, how many bedrooms and bathrooms there are, and location to predict the price of the house.

> [!IMPORTANT]   
> It works by minimizing the distance between the predicted output and the actual output.

## Comparison of all variants:

[![image.png](https://i.postimg.cc/MZCqQHkG/image.png)](https://postimg.cc/QVJ2LXdL)

Alternative or similar models for each of them:

[![image.png](https://i.postimg.cc/vTfRzrJS/image.png)](https://postimg.cc/5Q4k9CNw)

## Reference
Mastering Support Vector Machines. https://medium.com/@sangeeth.pogula_25515/mastering-support-vector-machines-classification-regression-and-kernels-157ddc6f8d0a. Opened in: nov/2025

SVM Variants and comparisons. https://abhishek005.medium.com/svm-variants-and-comparisons-251253f36bf2. Opened in: nov/2025
