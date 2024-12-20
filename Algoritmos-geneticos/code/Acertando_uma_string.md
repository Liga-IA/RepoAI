# Exemplo de Algoritmo Genético: Acertando uma String em Python

Este código implementa um **algoritmo genético** para gerar uma string que seja idêntica a uma string alvo. Ele começa com uma população de strings aleatórias e, através de seleção, cruzamento e mutação, evolui as strings até que uma solução exata seja encontrada.

### 1. Definindo o alfabeto e a classe `Agent`
```python
import random
import string

alfabeto = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.,"

class Agent:
    def __init__(self, length):
        self.string = ''.join(random.choice(alfabeto) for _ in range(length))
        self.fitness = -1
    def __str__(self):
        return ('String: ' + str(self.string) + ' Fitness: ' + str(self.fitness))
```
Aqui, é definido o alfabeto usado para gerar as strings aleatórias, que inclui letras maiúsculas e minúsculas, além de alguns símbolos. A classe Agent representa um indivíduo da população, com um atributo string que é inicializado aleatoriamente com caracteres do alfabeto. A classe também tem um atributo fitness que será calculado posteriormente para avaliar a qualidade da string gerada.

---

### 2. Parâmetros principais do algoritmo
```python
in_str = None
in_str_len = None
populacao = 30
geracoes = 10000
```
Define os parâmetros principais do algoritmo, como o número de gerações (10000), a população inicial (30 agentes) e o comprimento da string de entrada (a string alvo a ser encontrada).

---
### 3. Inicializando os agentes (população)
```python
def init_agents(populacao, length):
    print(Agent(length) for _ in range(populacao))
    return [Agent(length) for _ in range(populacao)]
```
Inicializa a população de agentes. Cada agente é um indivíduo com uma string aleatória gerada de acordo com o comprimento especificado. A função retorna uma lista de agentes.

---
### 4. Calculando a aptidão de um agente
```python
def get_fitness(string, target):
    points = sum(1 for expected, actual in zip(target, string) if expected == actual)
    return ((points*10)/in_str_len)
```
Calcula a aptidão de um agente, comparando a string do agente com a string alvo. A pontuação é dada pelo número de caracteres que coincidem entre a string do agente e a string alvo, com um fator de normalização.

---
### 5. Avaliação da população (aptidão = "fitness")
```python
def fitness(agents):
    for agent in agents:
        agent.fitness = get_fitness(agent.string, in_str)
    return agents
```
Avalia todos os agentes da população, calculando sua fitness com base na correspondência entre sua string e a string alvo. O valor de fitness é atribuído a cada agente.

---
### 6. Seleção dos melhores agentes
```python
def selecao(agents):
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print('\n'.join(map(str, agents)))
    agents = agents[:int(0.2 * len(agents))]
    return agents
```
Realiza a seleção dos agentes, ordenando-os de acordo com sua fitness e mantendo os 20% mais aptos da população para a próxima geração.

---
### 7. Cruzamento dos agentes
```python
def crossover(agents):
    offspring = []
    for _ in range(int((populacao - len(agents) / 2))):
        pai1 = random.choice(agents)
        pai2 = random.choice(agents)
        filho1 = Agent(in_str_len)
        filho2 = Agent(in_str_len)
        split = random.randint(0, in_str_len)
        filho1.string = pai1.string[0:split] + pai2.string[split:in_str_len]
        filho2.string = pai2.string[0:split] + pai1.string[split:in_str_len]
        offspring.append(filho1)
        offspring.append(filho2)
    agents.extend(offspring)
    return agents
```
Realiza o cruzamento entre pares de agentes, criando descendentes a partir de partes das strings dos pais. A operação de cruzamento mistura aleatoriamente partes das strings dos pais para formar os filhos.

---
### 8. Mutação nos agentes
```python
def mutacao(agents):
    for agent in agents:
        for idx, param in enumerate(agent.string):
            if random.uniform(0.0, 1.0) <= 0.1:
                agent.string = agent.string[0:idx] + random.choice(alfabeto) + agent.string[idx+1:in_str_len]
    return agents
```
Aplica a mutação em cada agente com uma probabilidade de 10%. Se a mutação ocorrer, um caractere aleatório substitui um caractere da string do agente, introduzindo diversidade genética.

---

### 9. Função principal do algoritmo genético `ga()`
```python
def ga():
    agents = init_agents(populacao, in_str_len)
    for geracao in range(geracoes):
        print('Geração: ' + str(geracao))
        agents = fitness(agents)
        agents = selecao(agents)
        agents = crossover(agents)
        agents = mutacao(agents)
        if any(agent.fitness >= 10.0 for agent in agents):
            print('Solução encontrada')
            break
```
Esta é a função principal do algoritmo genético. Ela chama as funções de inicialização, avaliação, seleção, cruzamento e mutação para cada geração. Se algum agente atingir um fitness suficientemente alto (indicando que encontrou a solução), o algoritmo é interrompido.

---
### 10. Execução do algoritmo com uma string alvo
```python
if __name__ == '__main__':
    in_str = 'Boa tarde, turma de IA!'
    in_str_len = len(in_str)
    ga()
```

Se você chegou até aqui, pode testar essa implementação diretamente no [Google Colab](https://colab.research.google.com/drive/1Swfo0E4IUXoHBbH06Pf5UgxG9duQb0zt?usp=sharing).
