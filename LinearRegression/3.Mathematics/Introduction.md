# General representation of linear regression

Mathematically, linear regression is a model used to predict numerical values based on one or more independent variables. It assumes the relationship between the dependent variable and the features is linear.

Therefore, it is represented by a linear equation, such as:

$$
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n
$$

- $\hat{y}$: The dependent variable or the predicted value.
- $\beta_n$: The intercept term, which corresponds to the value of $y$ when all $x$ values are zero.
- $\beta_1, \beta_2, \dots, \beta_n$: The coefficients for each independent variable, which represent how much each variable influences the prediction of y.
- $x_1, x_2, \dots, x_n$: The independent variables or features that are used to predict y.

If a model has two or more independent values, it is called **multiple linear regression**. However, this explanation will focus more on the simplest case, in which there is only one independent variable (**simple linear regression**).

## Simple Linear Regression (two dimensions)

In two dimensions, we can think about linear regression as a straight line, which follows the equation:

$$
\hat{y} = \beta_0 + \beta_1 x_1
$$

- $\hat{y}$: Dependent variable (response).
- $\beta_0$: Intercept.
- $\beta_1$: Coefficient of the independent variable.
- $x_1$: Independent variable (feature).

This representation can be viewed in figure 1:

![Figure 1](Figures/figure1.png)

The blue dots represent the actual values collected from real-world data. The straight line shows the model's predictions.

> Important: Since the blue dots are not exactly where the straight line is, there is an associated error that we must consider when using linear regression. In order to calculate the error, do the following: 
$
error = y - \hat{y} 
$
- $\hat{y}$: Predicted value from the model.
- $y$: Real-world value. 

## Exercise 1

By analyzing a graph, such as the figure 1 one, how can we determine which blue dots have a bigger error?
<details>
  <summary>Click to see the answer</summary>
  The farther from the straight line the dot is, the bigger the error. Our goal is to have the blue dots as close as possible to the line, as this makes the model more accurate.
</details>

# The least squares method

Let's say we want to determine the straight line equation of the linear regression model. It would be wise to think that we should have an equation that minimizes errors.

The most common method for determining the best equation to represent the predictions is the least squares method.

> Important: 



From one of the coding examples, let's analyze the relationship between hours studied and grades of a student.

| Hours Studied | Exam Score |
|--------------|------------|
| 1.5          | 50         |
| 3.0          | 55         |
| 4.5          | 65         |
| 6.0          | 70         |
| 7.5          | 80         |
| 9.0          | 85         |


## Exercise 2

2. 
<details>
  <summary>Click to see the answer</summary>
  
</details>

# 

EXEMPLO DE RETA E MODELO!!

-> Calculo do erro.

-> Como minimizar os erros no modelo.

# References
https://www.ufrgs.br/probabilidade-estatistica/livro/livro_completo/ch7-reg-simples.html
https://www.youtube.com/watch?v=pg6cUaNi3EE

