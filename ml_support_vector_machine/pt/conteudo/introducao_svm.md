
# Introdução

**Support Vector Machines (SVM)** é uma técnica de aprendizado de máquina supervisionado muito utilizada na categorização de textos, na análise de imagens e na bioinformática. Foi fundamentada pela **teoria de aprendizado estatístico (TAE)** criada por Vapnik, que estabelece princípios para a obtenção de classificadores com boa generalização.

> [!NOTE]
> Generalização é definida como a capacidade do classificador de prever corretamente a classe de novos dados não apresentados previamente

---

## Objetivo Principal

> [!IMPORTANT]
> O objetivo principal da SVM é encontrar o hiperplano que não apenas separe as classes, mas que também tenha a maior distância possível para os pontos de dados mais próximos de cada classe (pontos de suporte). Essa distância é chamada de margem.

<img src="https://i.postimg.cc/xjkSbRvG/1-a46Tz42Epfu3ys-Fnv-Wpz-WQ.gif" alt="Hiperplano SVM maximizando a margem" width="700" />

> [!NOTE]
> $1/||\mathbf{w}||$ é a distância mínima entre o hiperplano separador e os dados de treinamento. Essa distância é definida como a margem geométrica do classificador linear.

---

## Limites no Risco Esperado

O conceito-chave fornecido pela TAE é um limite superior para o **Risco Real** (ou Risco Esperado), $R(f)$, do classificador f.

### Fórmula da Cota de Generalização da Teoria Vapnik-Chervonenkis (VC)

$$R(f)\le R_{emp}(f)+\sqrt{\frac{h(ln(2n/h)+1)-ln(\theta/4)}{n}}$$

### Termos da Desigualdade:

* **$R(f)$ Risco Real (ou Risco Esperado)**: É a taxa de erro verdadeira do classificador f em toda a população de dados. É o que buscamos minimizar, mas é desconhecido.
* **$R_{emp}(f)$ Risco Empírico (ou Erro de Treinamento)**: É o erro que o classificador f cometeu no conjunto de treinamento de n amostras.
* **$h$ (Dimensão VC)**: É uma medida da complexidade ou capacidade da classe de funções à qual o classificador f pertence. Quanto maior $h$, mais complexo é o modelo, maior a chance de **overfitting** (o Risco Empírico $R_{emp}(f)$ é baixo, mas o Termo de Capacidade é alto).
* **$n$ (Tamanho da Amostra)**: O número de exemplos no conjunto de treinamento.
* **$\theta$ (Probabilidade de Falha)**: É um valor pequeno $(\theta\in[0,1])$ que define a confiança da cota. A desigualdade é válida com probabilidade de $1-\theta$.
  - Se você escolhe $\theta=0.05$, a cota é garantida com 95% de probabilidade.
  - Diminuir $\theta$ aumenta o termo $-ln(\theta/4)$, o que aumenta o limite superior, tornando a garantia mais confiável.
* **O logaritmo natural**: Utilizado para moderar o crescimento das variáveis $n$ e $h$.

Para que o classificador $f^*$ seja eficaz, o objetivo principal é minimizar o Risco Esperado $R(f)$. A desigualdade da Teoria VC mostra que isso pode ser alcançado através de uma estratégia de otimização de duplo objetivo:

1.  **Minimizar $R_{emp}(f)$**: O classificador deve ajustar-se bem aos dados de treinamento.
2.  **Minimizar o Termo de Capacidade**: O classificador deve pertencer a uma classe de funções com baixa Dimensão VC ($h$).

---

## SVMs com Margens Rígidas

O princípio da TAE estabelece que um classificador ideal deve minimizar o Risco Empírico (erro de treinamento) e pertencer a uma classe de funções de baixa complexidade (baixa Dimensão VC, $h$).

As SVMs lineares implementam a minimização da Dimensão VC ($h$) através da **maximização da margem geométrica ($\rho$)** $\rho\propto1/||\mathbf{w}||$. Portanto, maximizar a margem é equivalente a minimizar a norma $||\mathbf{w}||$.

$$Minim_{\mathbf{w}, b} \frac{1}{2} ||\mathbf{w}||^2$$

<img src="https://i.postimg.cc/GtYGtDtw/Captura-de-tela-de-2025-11-28-10-14-44.png" alt="Hiperplano SVM maximizando a margem" width="700" />

> [!NOTE]
> A minimização de $\frac{1}{2} ||\mathbf{w}||^2$ (em vez de $||\mathbf{w}||$) garante que a função objetivo seja convexa e diferenciável, facilitando a solução por métodos padrão de otimização quadrática.

---

## Minimização do Risco Estrutural (Margens Suaves)

Para lidar com a imperfeição e sobreposição dos dados, as SVMs adotam o **Princípio da Minimização do Risco Estrutural (MRS)**.

As **Margens Suaves** reformulam o problema introduzindo as **Variáveis de Folga ($\xi_i$)** para penalizar erros de classificação e violações da margem.



$$Minim_{\mathbf{w},b,\xi}\frac{1}{2}||\mathbf{w}||^{2}+C(\sum_{i=1}^{n}\xi_{i})$$

* **Termo $\frac{1}{2}||\mathbf{w}||^2$**: Controla a complexidade (**Maximização da Margem**).
* **Termo $C\sum\xi_i$**: Controla o erro de treinamento (**Minimização do Erro Marginal**).

<img src="https://i.postimg.cc/yxvnh5c0/Captura-de-tela-de-2025-11-27-22-59-30.png" alt="Hiperplano SVM maximizando a margem" width="700" />

> [!NOTE]
> A **Variável de Folga ($\xi_i$)** é uma invenção da SVM para permitir que o classificador funcione mesmo quando os dados não são perfeitamente separáveis (ou contêm ruído). Elas permitem que a SVM tolere essas imperfeições, penalizando os pontos que caem dentro da margem ou são classificados incorretamente, em vez de exigir uma separação rígida.

---

## Generalização em Problemas Não Lineares (Kernels)

A imagem abaixo demonstra o **Teorema de Cover**, que afirma que se os dados forem mapeados para um espaço de dimensão suficientemente alta através de uma transformação não linear, a probabilidade de separação linear aumenta.

[![Captura-de-tela-de-2025-11-26-22-30-19.png](https://i.postimg.cc/jjhFGWz2/Captura-de-tela-de-2025-11-26-22-30-19.png)](https://postimg.cc/jWLcfS3Y)

a) Para o conjunto de dados não linear (círculos e triângulos) é observável que não podem ser separados por uma única linha reta. 

b) A solução para separar as duas classes, seria uma fronteira de decisão circular (ou elíptica/curva).

c) Transformação dos dados para um novo espaço de dimensão 3D onde o hiperplano separador é um plano.

<img src="https://i.postimg.cc/y6FM3YGM/Captura-de-tela-de-2025-11-27-22-58-00.png" alt="plano 3D" width="700" />

> [!NOTE]
> Uma SVM linear simples não conseguiria encontrar essa fronteira.

O uso de **funções Kernel ($K$)** permite que o produto escalar dos dados no espaço de alta dimensão (**Phi(xi) . Phi(xj)**) seja calculado de forma eficiente no espaço de entrada $X$.

$$K(\mathbf{x}_{i},\mathbf{x}_{j})=\Phi(\mathbf{x}_{i})\cdot\Phi(\mathbf{x}_{j})$$

---

## Exemplo

Imagine que você está em um parque e há dois grupos de amigos brincando: um grupo de camisetas vermelhas e outro de camisetas azuis. Eles estão espalhados pelo gramado, mas há uma área onde os dois grupos estão mais próximos quase se misturando.
Agora, você quer esticar uma corda no chão para separar os dois grupos da melhor forma possível, sem passar por cima de ninguém. Mas não é só isso: você quer que a corda fique o mais distante possível dos amigos de cada grupo, para evitar confusões.

O que o SVM faz? 

- Ele procura a melhor posição para essa corda (o hiperplano) que separa os dois grupos.
- Os amigos mais próximos da corda são chamados de pontos de suporte eles são os que “definem” onde a corda pode passar.
- A SVM tenta maximizar a distância entre a corda e esses amigos mais próximos, criando uma margem de segurança entre os grupos.

Se alguém mudar de lugar e ficar mais perto da corda, a posição dela pode mudar porque os pontos de suporte mudaram!

---

### Referências

Este projeto utiliza conceitos descritos no artigo "Uma Introdução às Support Vector Machines" (Ana Carolina Lorena e André C. P. L. F. de Carvalho).
https://www.researchgate.net/publication/36409205_Uma_Introducao_as_Support_Vector_Machines

Support Vector Machine: Entenda o algoritmo SVM: https://www.blog.psicometriaonline.com.br/support-vector-machine-entenda-o-algoritmo-svm/

A Gentle Introduction to Support Vector Machines: https://www.kdnuggets.com/2023/07/gentle-introduction-support-vector-machines.html
