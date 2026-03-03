# English Version
## Naive Bayes Explained
Naive Bayes is a family of probabilistic algorithms based on Baye's theorem and its commonly used for classification tasks. Before understanting about naive bayes algorithms let's first jump into [Baye's Theorem](baye's_theorem_explained.md).

Now that we understand the basis of bayes rule let's understand a litle more of naive-bayes.

Naive Bayes uses probability to predict which category a data point belongs to, considering that all features, this is the data's characterisctics or atributtes, are independent and this simplifies the computation significantly.

> [!IMPORTANT]
> - Naive Bayes Classifier can predict at a faster speed than others classification algotithms because it's a simple probabilistic classifier and it doesn't have many parameters to build the ML models.
> - It is a probabilistic classifier because it assumes that one feature in the model is independent of existence of another feature. That means that each feature contributes to the predictions and has no relation between each other.

### Why the name *Naive Bayes*? 🤔
The term "Naive" comes from the fact that the model assumes that the presence of one feature does not affact other features, that the characteristic or attribute of the data are independent. And the "Bayes" part comes from to its basis in Bayes' Theorem.

### Types of Naive Bayes Model 📩
There are 3 types for classification in this model
1. Gaussian Naive Bayes
2. Multinomial Naive Bayes
3. Bernoulli Naive Bayes

The **first one** is speciaaly used for continuous data where features follow a Gaussian (normal) distribuition.  
The **second one**, also known as MNB, is well-suited for text classification tasks where term frequencies such as words counts in text are important.  
The **third one** deals with binary features like if a word appears or not in a document and it is often used in document classification tasks.

### Advantages of Naive Bayes Classifier 👍
- Simple to use and fast to compute.
- Works well even with many different characteristics.
- Good results even with a small amount of training information.
- Excellent with data that falls into categories (like "spam" or "not spam").
- For number-based data is assumed to come from normal distributions.

### Disadvantages of Naive Bayes Classifier 👎
- Assumes that all characteristics are separate from each other, which isn't always true in real life.  
- Can be affected by information that isn't important.  
- Might struggle with new information it hasn't seen before, which can lead to bad predictions.

### Applications of Naive Bayes Classifier 💡
- Spam Email Filtering: Sorts emails into "spam" or "not spam."
- Text Classification: Used for understanding feelings in text, sorting documents, and finding topics.
- Medical Diagnosis: Helps guess the chance of someone having a disease based on their symptoms.
- Credit Scoring: Checks how likely someone is to pay back a loan.
- Weather Prediction: Forecasts weather based on different factors.

# Portuguese Version
## Naive Bayes Explicado  
Naive Bayes é uma família de algoritmos probabilísticos baseada no Teorema de Bayes e é comumente usada para tarefas de classificação. Antes de entender os algoritmos *Naive Bayes*, vamos primeiro revisar o [Teorema de Bayes](baye's_theorem_explained.md).

Agora que entendemos a base da regra de Bayes, vamos entender um pouco mais sobre o *Naive Bayes*.

Naive Bayes usa probabilidade para prever a qual categoria um dado pertence, considerando que todas as características (isto é, os atributos ou propriedades dos dados) são independentes, o que simplifica bastante os cálculos.

> [!IMPORTANT]
> - O Classificador Naive Bayes pode prever com uma velocidade maior do que outros algoritmos de classificação porque é um classificador probabilístico simples e não possui muitos parâmetros para construir os modelos de aprendizado de máquina.  
> - É um classificador probabilístico porque assume que uma característica no modelo é independente da existência de outra. Isso significa que cada característica contribui para a previsão sem relação com as demais.

### Por que o nome *Naive Bayes*? 🤔  
O termo "Naive" (ingênuo) vem do fato de que o modelo assume que a presença de uma característica não afeta as outras — ou seja, os atributos dos dados são independentes. E a parte "Bayes" vem da sua base no Teorema de Bayes.

### Tipos de Modelo Naive Bayes 📩  
Há 3 tipos para classificação nesse modelo:  
1. Gaussian Naive Bayes  
2. Multinomial Naive Bayes  
3. Bernoulli Naive Bayes  

O **primeiro** é especialmente usado para dados contínuos em que as características seguem uma distribuição Gaussiana (normal).  
O **segundo**, também conhecido como MNB, é bem adequado para tarefas de classificação de texto, onde a frequência de termos, como contagem de palavras em um texto, é importante.  
O **terceiro** lida com características binárias, como se uma palavra aparece ou não em um documento, sendo frequentemente usado em tarefas de classificação de documentos.

### Vantagens do Classificador Naive Bayes 👍  
- Simples de usar e rápido para calcular.  
- Funciona bem mesmo com muitas características diferentes.  
- Bons resultados mesmo com uma pequena quantidade de dados de treinamento.  
- Excelente com dados categóricos (como "spam" ou "não spam").  
- Para dados numéricos, assume-se que vêm de distribuições normais.

### Desvantagens do Classificador Naive Bayes 👎  
- Assume que todas as características são independentes, o que nem sempre é verdade na vida real.  
- Pode ser afetado por informações que não são relevantes.  
- Pode ter dificuldades com informações novas que não viu antes, o que pode levar a previsões ruins.

### Aplicações do Classificador Naive Bayes 💡  
- **Filtro de E-mails Spam**: Classifica e-mails como "spam" ou "não spam".  
- **Classificação de Texto**: Usado para entender sentimentos em textos, organizar documentos e identificar tópicos.  
- **Diagnóstico Médico**: Ajuda a estimar a chance de uma pessoa ter uma doença com base nos sintomas.  
- **Análise de Crédito**: Avalia a probabilidade de uma pessoa pagar um empréstimo.  
- **Previsão do Tempo**: Faz previsões meteorológicas com base em diferentes fatores.

### References
- <[Naive Bayes Classifiers](https://www.geeksforgeeks.org/naive-bayes-classifiers/)>. Acess 29 may 2025 
