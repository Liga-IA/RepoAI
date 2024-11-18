## Reconhecimento Facial 


## 📝 Descrição

Este projeto implementa um sistema de reconhecimento facial capaz de identificar pessoas mesmo quando elas estão usando máscaras. O sistema utiliza técnicas de Deep Learning e Metric Learning para realizar o reconhecimento facial.

O diferencial deste projeto é sua capacidade de reconhecer faces com máscara a partir do treinamento realizado com fotos sem máscara, tornando-o especialmente útil em diversos contexto.

## 🚀 Funcionalidades

- Cadastro de pessoas através de 3-5 fotos sem máscara
- Reconhecimento facial com máscara
- Classificação e identificação da pessoa mais próxima no dataset
- Análise vetorial através de Metric Learning
- Processamento utilizando CNN (Convolutional Neural Network)

## 🏗️ Estrutura do Projeto
#### Estrutura do Código  
```bash
Reconhecimento-Facial/
│
├── src/
│   ├── model.ipynb                  # Código para criação e treinamento do modelo
│   ├── ModelFaceRecognition.h5      # Modelo treinado (arquivo gerado após treinamento)
│   └── Reconhecimento_Facial.ipynb  # Código para realizar o reconhecimento facial
│
└── content/
    ├── post-processed/              # Dataset de treinamento e teste (imagens de rostos)
    ├── Gabriel_01.jpg               # Exemplos de imagens
    └── ...
```
### Descrição dos Componentes

- **src/**: Contém os arquivos principais do código
  - `model.ipynb`: Notebook com a implementação e treinamento da CNN
  - `ModelFaceRecognition.h5`: Modelo treinado exportado
  - `Reconhecimento_Facial.ipynb`: Notebook com a implementação do reconhecimento facial utilizando Metric Learning

- **content/**: Contém os datasets e imagens de teste
  - `post-processed/`: Dataset de pessoas famosas para treinamento
  - `imagens_teste/`: Imagens para teste do sistema

## 💻 Tecnologias Utilizadas

- Python
- TensorFlow/Keras
- Google Colab (para treinamento)
- Técnicas de Deep Learning
- Metric Learning
- CNN (Convolutional Neural Network)

## 🧰 Funcionamento

O projeto utiliza uma combinação de técnicas avançadas de Deep Learning para realizar o reconhecimento facial com máscaras. O processo é dividido em duas etapas principais:

### 1. Treinamento da CNN (model.ipynb)
- **Preparação do Dataset**
  - Utilização de um dataset de pessoas famosas como base
  - Pré-processamento das imagens para normalização
  - Divisão em conjuntos de treino e validação

- **Arquitetura da CNN**
  - Implementação usando TensorFlow/Keras
  - Camadas convolucionais para extração de características
  - Camadas de pooling para redução dimensional
  - Camadas densas para classificação

- **Processo de Treinamento**
  - Realizado no ambiente Google Colab (GPU)
  - Otimização dos parâmetros da rede
  - Geração do modelo final (ModelFaceRecognition.h5)

### 2. Metric Learning (Reconhecimento_Facial.ipynb)
- **Extração de Características**
  - Processamento das imagens de entrada
  - Extração dos vetores característicos das faces
  - Criação de embeddings faciais

- **Processo de Reconhecimento**
  - Cálculo de similaridade entre vetores
  - Comparação com faces cadastradas
  - Determinação do match mais próximo

- **Fluxo de Identificação**
  1. Carregamento da imagem com máscara
  2. Detecção da região facial
  3. Extração dos vetores característicos
  4. Comparação com banco de faces cadastradas
  5. Identificação da pessoa mais similar

### 3. Métricas de Similaridade
- Utilização de distância euclidiana entre vetores
- Definição de threshold para reconhecimento
- Análise de confiança da predição

### 4. Cadastro de Novas Pessoas
1. **Coleta de Imagens**
   - 3-5 fotos sem máscara
   - Diferentes ângulos e iluminações
   
2. **Processamento**
   - Extração dos vetores característicos
   - Armazenamento no banco de dados

3. **Validação**
   - Testes de reconhecimento
   - Ajustes de parâmetros se necessário

## 📊 Resultados

O sistema de reconhecimento facial demonstrou resultados promissores, atingindo métricas significativas de performance:

### Performance Geral
- **Acurácia**: 85% de acurácia no modelo ModelFaceRecognition.h5


### Análise dos Resultados
- O modelo apresenta melhor performance quando:
  - As fotos de cadastro são tiradas com boa iluminação
  - São fornecidas 4-5 fotos para cadastro
  - As máscaras utilizadas não cobrem todo o rosto

### Limitações Identificadas
- Redução da precisão em condições de baixa luminosidade
- Maior dificuldade com máscaras que cobrem além do nariz
- Necessidade de ao menos 3 fotos de boa qualidade para cadastro efetivo

### Casos de Teste
1. **Cenário Ideal**
   - 5 fotos de cadastro com boa iluminação
   - Máscara padrão 
   - Iluminação adequada

2. **Cenário Desafiador**
   - 3 fotos de cadastro
   - Iluminação variada
   - Diferentes tipos de máscara


### Comparativo
O resultado de 85% de acurácia coloca este projeto em um patamar competitivo, considerando:
- A complexidade do reconhecimento com máscaras
- O uso de apenas fotos sem máscara para treinamento
- A variedade de condições de teste
- A capacidade computacional disponivel para o treinamento da CNN

