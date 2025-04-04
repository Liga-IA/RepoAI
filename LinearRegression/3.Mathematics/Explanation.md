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

![Gif1](Figures/gif1.gif)

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
 
$error = y - \hat{y}$

- **$\hat{y}$**: Predicted value from the model.
- **$y$**: Real-world value. 

## Exercise 1

By analyzing a graph, such as the figure 1 one, how can we determine which blue dots have a bigger error?
<details>
  <summary>Click to see the answer</summary>
  The farther from the straight line the dot is, the bigger the error. Our goal is to have the blue dots as close as possible to the line, as this makes the model more accurate.
</details>




# The least squares method

Let's say we want to determine the straight line equation of the linear regression model. It would be wise to think that we should have an equation that minimizes errors.
 
 The most common method for determining the best equation to represent the predictions is the least squares method, in which we minimize the sum of squared errors: $e_1^2 + e_2^2 + \dots + e_n^2$
 
 > [!IMPORTANT]
 > Think about why we minimize the squared errors instead of simply minimizing the sum of the errors ($|e_1| + |e_2| + \dots + |e_n|$).
 <details>
   <summary>Click to see the answer</summary>
   One reason is that squaring the errors makes bigger ones count more, helping the model focus on fixing those larger errors and giving a better overall fit to the data 
 </details>

More formally, the equation can be represented as:
$$S = \sum_{i=1}^{N} (E_i - \hat{E}_i)^2$$

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

Another way to express the error is through the equation of the line. The error at a given point is defined as the difference between the real value ($y$) and the estimated value ($\hat{y}$), given by: $e = y - \hat{y}$. As mentioned, the estimated value can be expressed using the equation of the regression line: $\hat{y} = \beta_0 + \beta_1 x_1$. By substituting this equation into the error expression, the result is:

$$
e = y - (\beta_0 + \beta_1 x_1)
$$

Therefore, the general equation for the sum of squared residuals is expressed as:

$$ S = \sum_{i=1}^{N} (y - [\beta_0 + \beta_1 x_1])^2 $$

To determine the values of $\beta_0$ and $\beta_0$, partial derivatives are taken with respect to each parameter and set to zero. The partial derivative with respect to $\beta_0$ is:

$$
\frac{\partial S}{\partial B_0} = -2 \sum_{i=1}^{N} (y_i - \beta_0 - \beta_1 x_i) = 0
$$

Solving for $\beta_0$, the equation simplifies to: $\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1\bar{X}$, where **$(\bar{Y})$** is the mean of the observed values of the dependent variable ($y$) and **$(\bar{X})$** is the mean of the values of the independent variable ($x$). For $\beta_1$, the partial derivative is given by:

$$
\frac{\partial S}{\partial \beta_1} = -2 \sum_{i=1}^{N} (y_i - \beta_0 - \beta_1 x_i) x_i = 0
$$

Rearranging the equation leads to:

$$
\hat{\beta_1} = \frac{\sum_{i = 1}^{N} (x_i – \bar{x} ) ( y_i – \bar{y} )}{\sum_{i = 1}^{N} ( x_i - \bar{x} )^2}
$$

---------------------------------


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

## Example

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

### Least Squares Error Calculation for the Exam Score Example

In this example, we calculate the least squares error for a simple linear regression model based on the relationship between hours studied and exam scores. The dataset and regression line are provided below.

## Data and Regression Equation

The dataset is:

| Hours Studied (x) | Exam Score (y) |
|-------------------|----------------|
| 1.5               | 50             |
| 3.0               | 55             |
| 4.5               | 65             |
| 6.0               | 70             |
| 7.5               | 80             |
| 9.0               | 85             |

The regression equation is:

$$
\hat{y} = 42.05 + 4.85x
$$

The least squares error \( S \) is calculated as:

$$
S = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

## Step 1: Calculate Predicted Values (\(\hat{y}_i\))

For each \( x_i \), compute \(\hat{y}_i\):

- \( x = 1.5 \): \(\hat{y} = 42.05 + 4.85 \times 1.5 = 49.325\)
- \( x = 3.0 \): \(\hat{y} = 42.05 + 4.85 \times 3.0 = 56.6\)
- \( x = 4.5 \): \(\hat{y} = 42.05 + 4.85 \times 4.5 = 63.875\)
- \( x = 6.0 \): \(\hat{y} = 42.05 + 4.85 \times 6.0 = 71.15\)
- \( x = 7.5 \): \(\hat{y} = 42.05 + 4.85 \times 7.5 = 78.425\)
- \( x = 9.0 \): \(\hat{y} = 42.05 + 4.85 \times 9.0 = 85.7\)

## Step 2: Compute Differences (\( y_i - \hat{y}_i \))

Subtract the predicted values from the observed values:

- \( 50 - 49.325 = 0.675 \)
- \( 55 - 56.6 = -1.6 \)
- \( 65 - 63.875 = 1.125 \)
- \( 70 - 71.15 = -1.15 \)
- \( 80 - 78.425 = 1.575 \)
- \( 85 - 85.7 = -0.7 \)

## Step 3: Square the Differences

Square each difference:

- \( (0.675)^2 = 0.455625 \)
- \( (-1.6)^2 = 2.56 \)
- \( (1.125)^2 = 1.265625 \)
- \( (-1.15)^2 = 1.3225 \)
- \( (1.575)^2 = 2.480625 \)
- \( (-0.7)^2 = 0.49 \)

## Step 4: Sum the Squared Differences

Add the squared differences to find \( S \):

$$
S = 0.455625 + 2.56 + 1.265625 + 1.3225 + 2.480625 + 0.49 = 8.574375
$$

## Result

The least squares error for this model is approximately **8.57**.


<details>
  <summary>Portuguese version</summary>

# Representação geral da regressão linear

Matematicamente, a regressão linear é um modelo usado para prever um valor numérico baseado em uma ou mais variáveis independentes. Ele assume que a relação entre a variável dependente e as caracteríticas é linear.

Portanto, é representado por uma equação linear:

$$
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n
$$

- **$\hat{y}$**: Variável dependente ou valor previsto.
- **$\beta_0$**: Valor de intersecção em $y$ para quando todos os valores de $x$ são zero.
- **$\beta_1, \beta_2, \dots, \beta_n$**: Coeficientes de cada variável independente, que representam o quanto cada variável influencia na predição de y.
- **$x_1, x_2, \dots, x_n$**: Variáveis independentes ou características que são usadas para prever y.

Se um modelo tem dois ou mais valores independentes, é chamado de **regressão linear múltipla**. No entanto, esta explicação focará no caso mais simples, em que há apenas uma variável independente (**regressão linear simples**).

![Gif1](Figures/gif1.gif)

## Regressão linear simples (duas dimensões)

Em duas dimensões, podemos pensar na regressão linear como sendo uma linha reta, que segue a equação:

$$
\hat{y} = \beta_0 + \beta_1 x_1
$$

- **$\hat{y}$**: Variável dependente
- **$\beta_0$**: Intercepto.
- **$\beta_1$**: Coeficiente da variável independente.
- **$x_1$**: Variável independente (característica).

This representation can be viewed in figure 1:

![Figure1-pt](Figures/figure1.png)

Os pontos em azul representam os valores coletados de dados reais. A linha reta mostra a predição do modelo.

> [!IMPORTANTE]
> Tendo em vista que os pontos azuis não estão exatamente onde a linha reta está, há um erro associado que devemos considerar quando utilizarmos regressão linear. Para calcular o erro, faça o seguinte: 
$
error = y - \hat{y} 
$
- **$\hat{y}$**: Predicted value from the model.
- **$y$**: Real-world value. 


# O método dos minímos quadrados

(aqui tem que colocar a outra parte)

Outra forma de expressar o erro é por meio da equação da reta. O erro em um determinado ponto é definido como a diferença entre o valor real ($y$) e o valor estimado ($\hat{y}$), dado por: $e = y - \hat{y}$. Como mencionado, o valor estimado pode ser expresso usando a equação da reta de regressão: $\hat{y} = \beta_0 + \beta_1 x_1$. Substituindo essa equação na expressão do erro, obtém-se:

$$
e = y - (\beta_0 + \beta_1 x_1)
$$

Portanto, a equação geral para a soma dos resíduos quadráticos é expressa como:

$$
S = \sum_{i=1}^{N} (y - [\beta_0 + \beta_1 x_1])^2
$$

Para determinar os valores de $\beta_0$ e $\beta_0$, são tomadas as derivadas parciais em relação a cada parâmetro e igualadas a zero. A derivada parcial em relação a $\beta_0$ é:

$$
\frac{\partial S}{\partial B_0} = -2 \sum_{i=1}^{N} (y_i - \beta_0 - \beta_1 x_i) = 0
$$

Resolvendo para $\beta_0$, a equação se simplifica para: $\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1\bar{X}$, onde **$(\bar{Y})$** é a média dos valores observados da variável dependente ($y$) e **$(\bar{X})$** é média dos valores da variável independente ($x$). Já para $\beta_1$, a derivada parcial é dada por:

$$
\frac{\partial S}{\partial B_1} = -2 \sum_{i=1}^{N} (y_i - \beta_0 - \beta_1 x_i) x_i = 0
$$

Rearranjando a equação, obtém-se: 
$$
\hat{\beta_1} = \frac{\sum_{i = 1}^{N} (x_i – \bar{x}) (y_i – \bar{y} )}{\sum_{i = 1}^{N} (x_i - \bar{x})^2}
$$

---------------------------------

## Como encontrar a equação com base em um conjunto de dados

Como explicado anteriormente, a regressão linear pode ser representada pela equação de uma reta:

$$
\hat{y} = \beta_0 + \beta_1 x
$$

Os valores β₁ e β₀ são parâmetros desconhecidos, onde β₁ representa a inclinação da reta e β₀ representa a intersecção com o eixo y.

Portanto, para determinar os valores de β₁ e β₀, devemos primeiramente coletar todos os dados de treinamento e organizá-los em pares de coordenadas (x, y). No final, teremos um conjunto de coordenadas assim como representado abaixo:

$$
\(x1, y1), (x2, y2),..., (xn, yn)
$$

Em que n representa o número total de ponto de dados coletados. Enfim, podemos calcular os valores β1 e β0 utilizando as duas equações abaixo:

$$
\hat{\beta_1} = \frac{\sum_{i = 1}^{n} (x_i – \bar{x} ) ( y_i – \bar{y} )}{\sum_{i = 1}^{n} ( x_i - \bar{x} )^2}
$$

$$
\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1\bar{X}
$$

- xi: valores x de cada coordenada
- yi: valores y de cada coordenada
- x̄: média aritmética simples dos valores x
- ȳ: média aritmética simples dos valores y

## Exemplo

A partir de um dos exemplos de código, vamos analisar a relação entre horas de estudo e notas de um aluno.

| Horas Estudadas | Nota do exame |
|-----------------|---------------|
| 1.5             | 50            |
| 3.0             | 55            |
| 4.5             | 65            |
| 6.0             | 70            |
| 7.5             | 80            |
| 9.0             | 85            |

Com base nos dados mostrados na tabela acima, podemos calcular os valores de β₁ e β₀ e definir a equação da reta. Para isso, definiremos Horas de Estudo como valores x e Notas do Exame como valores y. Assim, organizando todos os dados em pares de coordenadas, teremos os seguintes pontos: (1.5, 50), (3.0, 55), (4.5, 65), (6.0, 70), (7.5, 80), (9.0, 85).

Para facilitar o desenvolvimento do cálculo de β₁, calcularemos as variáveis e os somatórios separadamente, conforme exemplificado abaixo:

- x̄ = (1.5 + 3.0 + 4.5 + 6.0 + 7.5 + 9.0)/6 = 5.25
- ȳ = (50 + 55 + 65 + 70 + 80 + 85)/6 = 67.5

$$
\sum_{i = 1}^{n} (x_i – \bar{x} ) ( y_i – \bar{y} ) = (1.5 - 5.25)(50 - 67.5) + (3.0 - 5.25)(55 - 67.5) + (4.5 - 5.25)(65  67.5) + (6.0 - 5.25)(70 - 67.5) + (7.5 - 5.25)(80 - 67.5) + (9.0 - 5.25)(85 - 67.5) = 191.25
$$

$$
\sum_{i = 1}^{n} ( x - \bar{x} )^2 = (1.5 - 5.25)^2 + (3.0 - 5.25)^2 + (4.5 - 5.25)^2 + (6.0 - 5.25)^2 + (7.5 - 5.25)^2 + (9.0 - 5.25)^2 = 39.375
$$

Substituindo os valores na equação original, chegaremos a:

$$
\hat{\beta}_1 = \frac{191.25}{39.375} = 4.85
$$

Com os passos anteriores concluídos, agora podemos calcular o valor de β₀, conforme indicado abaixo:

$$
\hat{\beta}_0 = 67.5 - 4.85*5.25 = 42.03
$$

Após a substituição dos valores de β₁ e β₀ na equação linear, a seguinte expressão é obtida:

$$
\hat{y} = 42.05 + 4.85 x
$$
 
</details>

# References
https://www.ufrgs.br/probabilidade-estatistica/livro/livro_completo/ch7-reg-simples.html

HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. An introduction to statistical learning. 2009.

