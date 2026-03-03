# English Version
# Baye's Theorem
Bayes theorem (also known as the Bayes Rule or Bayes Law) is used to determine the conditional probability of event A when event B has already occurred, it's a formula used to calculate the probability of an outcome given a known previus outcome that occured in similar circumstances.
> KEY TAKEAWAYS
> - Baye's Theorem can be used to revise a probability analysis based on new information.
> - It is commonly used in finance to calculate or update risk evaluation.
> - And it is also used in other fields, such as analyses of medical test results.
<div align="center">
    <img src="https://i.postimg.cc/sx6YGXtc/data-science-bayes-theorem-2.png" alt="bayes_theorem" width="450">
</div>   
<br>   

## 🧪 Example 

Now let's see an simple example in the **medical test results** context about **Disease Testing**:  
A test for this disease is:

- 99% sensitive (true positive rate): If you **have** the disease, the test is positive 99% of the time.

- 95% specific (true negative rate): If you **don't** have the disease, the test is negative 95% of the time.

Now, if a person tests positive, what is the **probability they actually have the disease?**  

### 📊 Bayes' Theorem Formula
$$P(\text{Disease} \mid \text{Positive}) = \frac{P(\text{Positive} \mid \text{Disease}) \cdot P(\text{Disease})}{P(\text{Positive})}$$


### 🧮 Given:
- P(Disease) = 0.01
- P(No Disease) = 0.99
- P(Psitive | Disease) = 0.99
- P(Positive∣ No Disease) = 1−0.95 = 0.05
### 🧠 Step 1: Compute total probability of testing positive
P(Positive)=(0.99⋅0.01)+(0.05⋅0.99)=0.0099+0.0495=0.0594
### 🔍 Step 2: Apply Bayes' Theorem
$$P(\text{Disease} \mid \text{Positive}) = \frac{0.99 \times 0.01}{0.0594} = \frac{0.0099}{0.0594}$$

### ✅ Answer: About 16.7%
Even with a **positive test**, the chance of actually having the disease is only 16.7%, because the disease is rare and the test has some false positives.

# Portugues Version
# Teorema de Bayes  
O Teorema de Bayes (também conhecido como Regra de Bayes ou Lei de Bayes) é usado para determinar a probabilidade condicional de um evento A quando o evento B já ocorreu. É uma fórmula utilizada para calcular a probabilidade de um resultado dado um resultado anterior conhecido que ocorreu em circunstâncias semelhantes.  
> PRINCIPAIS PONTOS  
> - O Teorema de Bayes pode ser usado para revisar uma análise de probabilidade com base em novas informações.  
> - É comumente utilizado em finanças para calcular ou atualizar a avaliação de riscos.  
> - E também é usado em outras áreas, como análises de resultados de testes médicos.  

<div align="center">
    <img src="https://i.postimg.cc/sx6YGXtc/data-science-bayes-theorem-2.png" alt="bayes_theorem" width="450">
</div>   
<br>   

## 🧪 Exemplo  

Agora vamos ver um exemplo simples no contexto de **resultados de testes médicos** sobre **teste de doença**:  
Um teste para essa doença é:

- 99% sensível (taxa de verdadeiro positivo): Se você **tem** a doença, o teste dá positivo em 99% das vezes.  

- 95% específico (taxa de verdadeiro negativo): Se você **não tem** a doença, o teste dá negativo em 95% das vezes.  

Agora, se uma pessoa testa positivo, qual é a **probabilidade de ela realmente ter a doença?**  

### 📊 Fórmula do Teorema de Bayes  
$$P(\text{Doença} \mid \text{Positivo}) = \frac{P(\text{Positivo} \mid \text{Doença}) \cdot P(\text{Doença})}{P(\text{Positivo})}$$

### 🧮 Dados fornecidos:  
- P(Doença) = 0.01  
- P(Não Doença) = 0.99  
- P(Positivo | Doença) = 0.99  
- P(Positivo ∣ Não Doença) = 1 − 0.95 = 0.05  

### 🧠 Etapa 1: Calcular a probabilidade total de testar positivo  
P(Positivo) = (0.99 ⋅ 0.01) + (0.05 ⋅ 0.99) = 0.0099 + 0.0495 = 0.0594  

### 🔍 Etapa 2: Aplicar o Teorema de Bayes  
$$P(\text{Doença} \mid \text{Positivo}) = \frac{0.99 \times 0.01}{0.0594} = \frac{0.0099}{0.0594}$$  

### ✅ Resposta: Cerca de 16,7%  
Mesmo com um **teste positivo**, a chance de realmente ter a doença é de apenas 16,7%, porque a doença é rara e o teste apresenta alguns falsos positivos.

### References
- <[Baye's Theorem](https://www.investopedia.com/terms/b/bayes-theorem.asp)>. Acess 29 may 2025 
