# Transfer Learning e Fine Tuning com CNN

[![Abrir no Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1KG_nZ4Yf1_IodwdqszUjJv05UGuTGvkB?usp=sharing)

## Visão geral

Este material apresenta uma introdução prática ao uso de redes neurais convolucionais pré treinadas para classificação de imagens. O projeto utiliza a arquitetura MobileNetV2 em um problema de visão computacional com imagens meteorológicas, mostrando como aproveitar um modelo já treinado em larga escala para resolver uma tarefa mais específica com menor custo computacional.

## O que será abordado

Ao longo desta pasta, o foco está na preparação do dataset, no preprocessamento das imagens, na montagem do modelo, no treinamento inicial com a base convolucional congelada e na etapa posterior de ajuste fino. A explicação completa da implementação, das decisões técnicas e das etapas do pipeline está documentada diretamente no código principal.

## Transfer learning

Transfer learning é a técnica de reutilizar o conhecimento aprendido por um modelo em uma tarefa anterior para acelerar o aprendizado em uma nova tarefa. Em vez de treinar uma rede do zero, usamos pesos obtidos em um grande conjunto de imagens, como o ImageNet, para extrair características visuais importantes, como bordas, texturas, formas e padrões mais complexos.

## Fine tuning

Fine tuning é a etapa em que parte desse modelo pré treinado deixa de ficar congelada e passa a ser ajustada com os dados do novo problema. Isso permite adaptar melhor as representações aprendidas ao domínio do projeto, preservando o conhecimento geral útil e refinando as camadas mais altas para a tarefa de classificação das condições do tempo.

## Estratégia do projeto

Neste projeto, a estratégia consiste em treinar primeiro apenas a cabeça de classificação adicionada sobre a MobileNetV2 e, depois, liberar parte das camadas superiores da rede com uma taxa de aprendizado menor. Essa abordagem ajuda a obter melhor desempenho sem perder de forma brusca o conhecimento previamente aprendido pelo modelo.

## Código principal

O arquivo principal desta pasta demonstra, de forma comentada, como carregar os dados, aplicar augmentation, treinar o modelo, executar o ajuste fino e avaliar os resultados finais.
