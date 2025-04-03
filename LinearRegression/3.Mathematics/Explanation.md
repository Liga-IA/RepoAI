# General representation of linear regression

Mathematically, linear regression is a model used to predict numerical values based on one or more independent variables. It assumes the relationship between the dependent variable and the features is linear.

Therefore, it is represented by a linear equation, such as:

$$
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n
$$

- **$\hat{y}$**: The dependent variable or the predicted value.
- **$\beta_0$**: The intercept term, which corresponds to the value of $y$ when all $x$ values are zero.
- **$\beta_1, \beta_2, \dots, \beta_n$**: The coefficients for each independent variable, which represent how much each variable influences the prediction of y.
- **$x_1, x_2, \dots, x_n$**: The independent variables or features that are used to predict y.

If a model has two or more independent values, it is called **multiple linear regression**. However, this explanation will focus more on the simplest case, in which there is only one independent variable (**simple linear regression**).

## Simple Linear Regression (two dimensions)

In two dimensions, we can think about linear regression as a straight line, which follows the equation:

$$
\hat{y} = \beta_0 + \beta_1 x_1
$$

- **$\hat{y}$**: Dependent variable (response).
- **$\beta_0$**: Intercept.
- **$\beta_1$**: Coefficient of the independent variable.
- **$x_1$**: Independent variable (feature).

This representation can be viewed in figure 1:

![Figure 1](Figures/figure1.png)

The blue dots represent the actual values collected from real-world data. The straight line shows the model's predictions.

> [!IMPORTANT]
> Since the blue dots are not exactly where the straight line is, there is an associated error that we must consider when using linear regression. In order to calculate the error, do the following: 
$
error = y - \hat{y} 
$
- **$\hat{y}$**: Predicted value from the model.
- **$y$**: Real-world value. 

## Exercise 1

By analyzing a graph, such as the figure 1 one, how can we determine which blue dots have a bigger error?
<details>
  <summary>Click to see the answer</summary>
  The farther from the straight line the dot is, the bigger the error. Our goal is to have the blue dots as close as possible to the line, as this makes the model more accurate.
</details>




# The least squares method


This technique is extremely important because it has many applications in exact sciences, especially in engineering and data analysis.

The least squares method is the mathematical foundation of linear regression. Its goal is to minimize the sum of the squares of the differences between observed and predicted values by the model (errors). 

This directly connects the least squares method with linear regression, as it provides the exact way to find the parameters of the line or hyperplane that best fit the observed data.

The general equation of the sum of squared residuals is given by:
$S = \sum_{i=1}^{N} (E_i - \hat{E}_i)^2$

In this equation:


* $E_i$ represents the observed value of the dependent variable for each observation $i$;

* $\hat{E}_i$ represents the value estimated by the model;

* $S$ is the total sum of squared residuals, which we want to minimize;

* $N$ is the total number of observations.


The mathematical solution that minimizes this sum and, therefore, provides the best values for the model coefficients, is given by the matrix equation:

$\hat{B} = (X^TX)^{-1}X^TE$

Here:

* $X$ is a matrix containing the independent variables;

* $E$ is the vector with the dependent variable values;

* $\hat{B}$ is the vector with the coefficients we want (values of $A$, $B$, etc.).






## How to find the equation based on a data set

As previously explained, linear regression can be represented by the equation of a straight line: 

$$
\hat{y} = \beta_0 + \beta_1 x
$$

The values β₁ and β₀ are unknown parameters, where β₁ represents the slope of the line and β₀ represents the y-intercept.

Therefore, to determine the values of β₁ and β₀, we must first collect all training data and organize it into pairs of coordinates (x, y). Ultimately, we will have a set of coordinates as represented below:

$$
\(x1, y1), (x2, y2),..., (xn, yn)
$$

Where n represents the total number of data points collected. Finally, we can calculate the values of β₁ and β₀ using the equations below:

$$
\hat{\beta_1} = \frac{\sum_{i = 1}^{n} (x_i – \bar{x} ) ( y_i – \bar{y} )}{\sum_{i = 1}^{n} ( x_i - \bar{x} )^2}
$$

$$
\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1\bar{X}
$$

- xi: x values of each coordinate
- yi: y values of each coordinate
- x̄: simple arithmetic mean of the x values 
- ȳ: simple arithmetic mean of the y values

(exemplo:) (aqui não sei se a gente faz alguma introdução ou só coloca como titulo exemplo)

From one of the coding examples, let's analyze the relationship between hours studied and grades of a student.

| Hours Studied | Exam Score |
|--------------|------------|
| 1.5          | 50         |
| 3.0          | 55         |
| 4.5          | 65         |
| 6.0          | 70         |
| 7.5          | 80         |
| 9.0          | 85         |

Based on the data shown in the table above, we can calculate the values of β₁ and β₀ and define the equation of the line. For this purpose, we will define Hours Studied as x values and Exam Scores as y values. Thus, organizing all the data into pairs of coordinates, we will have the following points: (1.5, 50), (3.0, 55), (4.5, 65), (6.0, 70), (7.5, 80), (9.0, 85).

To facilitate the development of the β₁ calculation, we will compute the variables and the summations independently, as exemplified below:

- x̄ = (1.5 + 3.0 + 4.5 + 6.0 + 7.5 + 9.0)/6 = 5.25
- ȳ =(50 + 55 + 65 + 70 + 80 + 85)/6 = 67.5
  
$$
\sum_{i = 1}^{n} (x_i – \bar{x} ) ( y_i – \bar{y} ) = (1.5 - 5.25)(50 - 67.5) + (3.0 - 5.25)(55 - 67.5) + (4.5 - 5.25)(65  67.5) + (6.0 - 5.25)(70 - 67.5) + (7.5 - 5.25)(80 - 67.5) + (9.0 - 5.25)(85 - 67.5) = 191.25
$$

$$
\sum_{i = 1}^{n} ( x - \bar{x} )^2 = (1.5 - 5.25)^2 + (3.0 - 5.25)^2 + (4.5 - 5.25)^2 + (6.0 - 5.25)^2 + (7.5 - 5.25)^2 + (9.0 - 5.25)^2 = 39.375
$$

By substituting the values into the original equation, we will arrive at:

$$
\hat{\beta}_1 = \frac{191.25}{39.375} = 4.85
$$

With the preceding steps completed, we are now able to calculate the value of β₀, as indicated below:

$$
\hat{\beta}_0 = 67.5 - 4.85*5.25 = 42.03
$$

Upon substitution of the β₁ and β₀ values into the linear equation, the following expression is obtained:

$$
\hat{y} = 42.05 + 4.85 x
$$

## Exercise 2

2. (pergunta sobre encontrar equacao a partir de dados. Calcular o erro tambem.)
<details>
  <summary>Click to see the answer</summary>
  
</details>



# References
https://www.ufrgs.br/probabilidade-estatistica/livro/livro_completo/ch7-reg-simples.html

