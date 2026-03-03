# Exemplo: Classificação de e-mails com Naive Bayes

O principal objetivo deste algoritmo é demonstrar como o método Naive Bayes pode ser muito eficaz em tarefas de classificação, como a detecção de spam. A seguir, apresentamos um passo a passo didático e de fácil compreensão, para que você possa reproduzir a implementação com outros conjuntos de dados e, assim, praticar e se divertir! :smile:




<img src="https://media1.tenor.com/m/3AQDvhSiPpMAAAAC/dog-hacker.gif" width="300" />


## Código

### Importar bibliotecas
``` python
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
```
- pandas as pd → para ler o CSV e manipular o DataFrame.

- MultinomialNB → classificador Naive Bayes.

- train_test_split → divisão entre treino e teste.

- TfidfVectorizer → (importado dentro do código, mas usado corretamente).

- SMOTE → para balancear os dados.
  
- TfidfVectorizer → usada para transformar texto em números.

- Counter → é uma estrutura de dados que serve para contar a frequência de elementos em um iterável.

- confusion_matrix, seaborn, matplotlib.pyplot → para visualizar a matriz de confusão.

### Carregar e preparar os dados
``` python
ds = pd.read_csv("/content/spam.csv")
ds["spam"] = ds["Category"].apply(lambda x: 1 if x == "spam" else 0)
y = ds.iloc[:, 2].values
X = ds["Message"]
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)
X_treino, X_teste, y_treino, y_teste = train_test_split(X_tfidf, y, test_size=0.2, random_state=42, stratify=y)
```
- Carrega o dataset CSV → le o arquivo CSV chamado spam.csv e salva o conteúdo no DataFrame ds usando a biblioteca pandas.
  
- Cria uma nova coluna "spam" com rótulos binários (0 e 1).
  - Acessa a coluna Category, que contém rótulos de texto como "spam" ou "ham" (não-spam)
  - Usa apply() com uma função lambda para converter esses textos em números: "spam" → 1, qualquer outro valor (como "ham") → 0
  - Cria uma nova coluna chamada "spam" no DataFrame com esses valores
    
- Separa os rótulos (y).
  
- Separa as mensagens (X).

- Vetorização com TfidfVectorizer → transforma os textos da coluna Message em vetores numéricos esparsos com base na frequência e relevância de cada palavra (TF-IDF = Term Frequency – Inverse Document Frequency).

- Divide os dados em 80% para treino e 20% para teste → stratify=y garante que a proporção de classes (spam/ham) seja mantida igual nas duas partes.

- random_state = 42 → Garante que a divisão sempre ocorra da mesma forma (reprodutibilidade).

- stratify = y → Garante que a proporção de spam e não spam seja mantida em ambos os conjuntos.

> [!IMPORTANT]
> Sem stratify, o modelo poderia acabar com muito menos spam no teste ou no treino, o que prejudicaria o aprendizado e avaliação.

> [!Note]
>Por que usar TF-IDF?
>  - Dá peso maior às palavras que realmente têm importância.
>  - Ignora palavras comuns (como "e", "a", "de", etc.).
>  - É rápido e eficiente.
>  - Funciona muito bem com modelos lineares como Naive Bayes.

### Oversampling
gerar dados sintéticos para a classe minoritária (neste caso, spam).

> [!Note]
>Oversampling é uma técnica usada em machine learning para lidar com conjuntos de dados desbalanceados — ou seja, quando uma classe (ex: spam) tem muito menos exemplos do que a outra (ex: não spam).

``` python
print("Antes do oversampling:", Counter(y_treino))
```
[![image.png](https://i.postimg.cc/bwXXTV7s/image.png)](https://postimg.cc/D8cYf6yT)
``` python
smote = SMOTE(random_state=42)
X_treino_smote, y_treino_smote = smote.fit_resample(X_treino, y_treino)
```
- Cria um objeto SMOTE, que vai gerar dados sintéticos para a classe minoritária (neste caso, spam).
- SMOTE faz o "oversampling":
  - Ele gera exemplos sintéticos da classe minoritária (spam = 1).
  - O conjunto de treino resultante (X_treino_smote) agora tem a mesma quantidade de exemplos das duas classes.

``` python
print("Após o oversampling:", Counter(y_treino_smote))
```
[![image.png](https://i.postimg.cc/LX4hs8vK/image.png)](https://postimg.cc/jW9RgKGZ)

### Treinar, testar e visualizar os resultados
``` python
modelo = MultinomialNB()
modelo.fit(X_treino_smote, y_treino_smote)
previsoes = modelo.predict(X_teste)
previsoes
```
[![image.png](https://i.postimg.cc/pTBLjhqX/image.png)](https://postimg.cc/sQvzd2kt)
``` python
y_teste
```
[![image.png](https://i.postimg.cc/XJBTMTyM/image.png)](https://postimg.cc/5Y1PLK3p)
``` python
modelo.score(X_teste, y_teste)
```
[![image.png](https://i.postimg.cc/TwQW6489/image.png)](https://postimg.cc/jwwj6vSw)
``` python
cm = confusion_matrix(y_teste, previsoes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Previsto')
plt.ylabel('Real')
plt.title('Matriz de Confusão')
plt.show()
```
[![image.png](https://i.postimg.cc/gcC6PRQ1/image.png)](https://postimg.cc/XXgvfZVg)

- Para visualizar os resultados das previsões do modelo usamos a matriz de confusão, que mostra com detalhes quantos acertos e erros o modelo cometeu para cada classe (spam e não-spam).

### Conclusões
📌 ***O modelo é eficaz para detectar spam***
  - Acerta a maioria das mensagens, como mostrado pela alta acurácia de 97%.
  - Ele é capaz de prever corretamente tanto spam quanto não spam, o que é confirmado pela matriz de confusão.


📌 ***O uso do SMOTE foi essencial***
  - Com o oversampling, igualamos o número de exemplos de cada classe, o que ajuda o modelo a aprender melhor como identificar spam.
  - Evita que o modelo "ignore" a classe minoritária (spam).


📌 ***Pipeline bem estruturado***
  - Pré-processamento.
  - Vetorização.
  - Divisão estratificada.
  - Balanceamento com SMOTE.
  - Treinamento.
  - Avaliação com métrica e matriz.

## 👾 **Contribuidores**  
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/112569754?v=4" width=115><br><sub>Alice Motin</sub>](https://github.com/AliceMotin) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/206122594?v=4" width=115><br><sub>Arthur Janing</sub>](https://github.com/Arthur-Janing) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/147776134?v=4" width=115><br><sub>Caroline Lanzuolo</sub>](https://github.com/carol-lanzu) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/171816351?v=4" width=115><br><sub>Mateus Kramer</sub>](https://github.com/mateuskramer) 
| :---: | :---: | :---: | :---: |

