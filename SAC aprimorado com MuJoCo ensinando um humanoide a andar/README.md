# SAC aprimorado com MuJoCo: ensinando um humanoide a andar

Ensinar máquinas a se mover no mundo físico revela o quanto a locomoção é um processo delicado e desafiador. Equilibrar um robô humanoide em duas pernas e conduzi-lo até uma caminhada estável exige algoritmos robustos e várias decisões cuidadosas de engenharia.

Este projeto foi inspirado por um vídeo de 2023 do canal AI Warehouse, no qual eles utilizam Reinforcement Learning para ensinar o robô apelidado de Albert a aprender a andar a partir do zero. O processo de tentativa e erro mostrado no vídeo, em que Albert começa desajeitado e evolui gradualmente até alcançar uma caminhada funcional, destaca bem o potencial desse método.

Há também um aspecto conceitual que torna Reinforcement Learning particularmente interessante: o agente realmente começa sem saber nada e melhora a cada iteração. Do ponto de vista intuitivo, isso faz com que RL pareça um dos métodos de IA que mais se aproximam da ideia de aprendizado “real”, pois o conhecimento emerge exclusivamente da interação direta com o ambiente. Embora isso não represente inteligência humana no sentido estrito, a dinâmica incremental de aprendizado reforça essa impressão de progresso genuíno.

Neste repositório, revisitamos o clássico problema de ensinar um robô a andar utilizando um agente Soft Actor–Critic (SAC) aprimorado, randomização de domínio, aprendizado por currículo e um conjunto de escolhas de engenharia projetadas para aumentar estabilidade e robustez.

Como ponto de partida, um humanoide sem treinamento simplesmente colapsa repetidas vezes ao tentar dar os primeiros passos.

[Vídeo: baseline sem treino](https://youtu.be/hDH2jA9cpYw)

## Locomoção humanoide como desafio de RL

Em aprendizado por reforço (Reinforcement Learning, RL), um agente interage com um ambiente tomando ações e recebendo feedback na forma de recompensas. O objetivo é maximizar a recompensa acumulada ao longo do tempo. Em tarefas de locomoção, o ambiente é um simulador físico (neste projeto usamos o **MuJoCo** — <https://github.com/google-deepmind/mujoco>) e as recompensas incentivam comportamentos como ficar ereto, avançar e manter a estabilidade. O espaço de estados é contínuo (ângulos das juntas, velocidades, posições do corpo), assim como o espaço de ações (torques em cada junta), e a dinâmica é altamente não linear. Essas características tornam a locomoção um ótimo alvo para um método SAC moderno e eficiente.

## Soft Actor–Critic v2, em poucas palavras

Soft Actor-Critic (SAC) é um algoritmo off-policy de ator–crítico baseado no framework de RL de entropia máxima (Haarnoja et al., 2018 — artigo: <https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf>). Na prática, o SAC tenta maximizar a recompensa esperada **e** a entropia (ou seja: aprender a cumprir a tarefa mantendo a política estocástica, o que ajuda na exploração). O SAC aprende duas funções Q e uma política ao mesmo tempo.

Podemos pensar no SAC como um aprendiz explorando uma cidade desconhecida. As funções Q são como dois guias locais independentes, cada um dando sua estimativa do valor de seguir por determinadas ruas. A política é o próprio aprendiz decidindo para onde ir. Se ele sempre seguir só o guia que parece mais confiante, pode acabar preso em um caminho limitado. Por isso, o SAC incentiva manter um certo nível de “curiosidade” — essa é a entropia. É como se o aprendiz recebesse um pequeno incentivo para, ocasionalmente, tentar rotas que ainda não conhece bem. Ao equilibrar essas duas coisas — seguir direções promissoras e, ao mesmo tempo, não deixar de explorar — o SAC aprende caminhos cada vez melhores de forma estável, sem ficar preso cedo demais em soluções ruins.

**Política.** A política gera uma distribuição de ações contínuas a partir de uma Gaussiana passada por `tanh`, usando o truque de reparametrização:

$$
a = \tanh\big( \mu_\theta(s) + \sigma_\theta(s) \odot \epsilon \big), \quad \epsilon \sim \mathcal{N}(0, I).
$$

**Críticos gêmeos.** Duas funções de valor-ação estimam retornos:

$$
Q_{\phi_1}(s,a),\; Q_{\phi_2}(s,a).
$$

Ao contrário de métodos ator–crítico mais antigos, o SAC inclui um bônus de entropia controlado por um parâmetro de temperatura $\alpha$, que incentiva exploração mantendo a política estocástica.

- **Sem rede de valor explícita** – os críticos aprendem Q diretamente, e o alvo de ambos usa o mínimo das duas redes alvo.
- **Política Gaussiana com `tanh`** – a política produz uma Gaussiana e aplica `tanh` para respeitar os limites de ação.
- **Ajuste automático de entropia** – $\alpha$ é otimizado durante o treino para manter a entropia próxima de um valor-alvo. Se a política fica determinística demais, $\alpha$ aumenta; se fica aleatória demais, $\alpha$ diminui.
- **Retornos n-passos** – os alvos de Q misturam retornos de múltiplos passos com alvos de 1 passo para equilibrar viés e variância. (O padrão aqui usa $n=3$.)

Além disso, usamos inicialização ortogonal dos pesos nas camadas e *gradient clipping* para uma norma fixa, visando estabilizar o treinamento. O ator busca maximizar o objetivo:

$$
J_{\text{actor}} = \mathbb{E}_{s\sim D,\; a\sim \pi_\theta}\big[\min_i Q_{\phi_i}(s,a) - \alpha\, \log \pi_\theta(a\mid s)\big].
$$

Enquanto isso, cada crítico minimiza o erro quadrático entre seu Q e o alvo

$$
y = r + \gamma^n\big( \min_i Q_{\bar{\phi}_i}(s', a') - \alpha\, \log \pi_\theta(a'\mid s') \big),
$$

usando uma rede alvo para estabilidade. (Para detalhes, veja o código em `sac_rl/algo/sac_agent.py`.)

## Decisões de engenharia

### Ambientes vetorizados

Treinar uma política de locomoção costuma exigir milhões de passos no ambiente. Para acelerar a coleta de dados, usamos o `AsyncVectorEnv` do Gymnasium para rodar vários simuladores em paralelo. A configuração padrão inicia **16 ambientes MuJoCo Humanoid em paralelo** (tarefas `Humanoid-v5` do Gymnasium) para aumentar a taxa de amostragem. Você pode ajustar o número de ambientes paralelos com uma simples mudança no YAML ou via override na linha de comando. Ambientes vetorizados melhoram muito a eficiência de amostragem ao aproveitar múltiplos núcleos de CPU.

### Randomização de domínio

Políticas treinadas apenas em simulação muitas vezes sofrem quando são expostas a novas condições. Para ganhar robustez, o `DomainRandomizationWrapper` randomiza parâmetros físicos como massas dos elos do robô, atritos das juntas, atrito/inclinação do solo e também injeta uma pequena quantidade de ruído nas ações a cada episódio. Esses parâmetros são amostrados de forma uniforme dentro de faixas definidas no YAML. No código, os valores sorteados são armazenados no ambiente subjacente para inspeção — e os testes usam isso para verificar que a randomização de fato acontece. Ao longo do treinamento, a randomização de domínio expõe o agente a uma família maior de dinâmicas, deixando a política aprendida mais adaptável.

### Aprendizado por currículo

É implementado um *wrapper* de currículo que começa facilitando a tarefa: ele limita a velocidade do humanoide para frente (evitando que ele tente “correr” antes de saber se equilibrar) e recompensa o agente principalmente por manter a postura ereta. Quando um certo limiar é atingido (por exemplo, um número de passos ou um alvo de retorno médio), o *wrapper* remove o limite de velocidade e libera a tarefa completa de andar. Esses limiares são configuráveis (em termos de passos totais no ambiente ou retorno médio por episódio). A estratégia garante que o agente primeiro domine o equilíbrio e só então enfrente, gradualmente, o desafio completo de locomoção, deixando as fases iniciais do aprendizado mais estáveis.

### Normalização de observações e recompensas

Observações com alta variância ou recompensas mal escaladas podem desestabilizar o treinamento. *wrappers* opcionais de normalização foram incluídos, os quais acompanham estatísticas em tempo real (média e variância) para padronizar as observações e aplicam escalonamento de recompensas online. Na prática, observações são normalizadas para média zero e variância unitária (com base em uma estimativa contínua) e recompensas escaladas pelo desvio padrão de uma janela móvel de retornos recentes. Essa técnica, comum em controle contínuo, ajuda a manter as atualizações dos críticos em uma faixa mais saudável e evita que as estimativas de valor explodam por conta de magnitudes de recompensa muito grandes.

### Reprodutibilidade e rastreamento

Definir sementes de forma determinística é essencial para resultados reproduzíveis. Nosso script de treinamento permite configurar `algo.seed` no arquivo de configuração; esse valor é então usado para semear, em conjunto, o módulo `random` do Python, o NumPy e o PyTorch. Os arquivos YAML em `configs/` definem todos os parâmetros do experimento, e qualquer um deles pode ser sobrescrito via linha de comando. O *trainer* registra curvas de treino (retornos e durações de episódios), entropia da política, temperatura $\alpha$ e perdas no TensorBoard por padrão.

## Resultados

Depois de cerca de dez milhões de passos no ambiente, o agente SAC aprimorado aprende a levantar, se equilibrar e, por fim, dar passos para frente. Você pode gerar um gráfico parecido com o script de diagnósticos após sua execução. A política final mostra um caminhar estável.

[Vídeo: humanoide treinado](https://youtu.be/YBWMGkf241c)

As melhorias de engenharia fazem diferença de forma bem concreta no treinamento:

- **Normalização de observações e escalonamento de recompensas** reduzem a variância das atualizações do crítico, levando a curvas mais suaves e aprendizado mais estável.
- **Randomização de domínio** amplia a variedade de situações que o agente encontra, produzindo uma política mais robusta (com o custo de uma convergência um pouco mais lenta, já que a tarefa fica “mais difícil” em média).
- **Aprendizado por currículo** acelera o começo do treino ao simplificar a tarefa inicial. Ao mesmo tempo, foi importante garantir que o agente não se adaptasse demais à fase inicial; ele precisa conseguir fazer a transição para a tarefa completa quando chega a hora.

Vale notar que, embora o foco aqui seja o Humanoid 3D, o mesmo algoritmo resolve tarefas de locomoção mais simples também. Por exemplo, um **Walker2d** foi treinado usando esta base de código, e ele alcançou uma passada estável com bem menos passos que o humanoide (como esperado, dada a complexidade menor). O repositório inclui o arquivo `configs/mujoco_walker2d.yaml` para o Walker2d.

## Passos para reproduzir

Para reproduzir esses resultados ou rodar seus próprios experimentos, siga estes passos:

**Instale as dependências** – O código exige Python 3.10+ e PyTorch 2.x. Recomendamos criar um ambiente virtual. Em seguida, instale os pacotes necessários (MuJoCo, Gymnasium, PyBullet, etc.) usando os scripts fornecidos:

```bash
# Instalação apenas CPU (para máquinas sem GPUs CUDA)
bash scripts/install_cpu.sh
# Instalação com GPU (máquinas com CUDA)
bash scripts/install_gpu.sh
```

**Treine o agente** – Use a configuração do MuJoCo Humanoid para iniciar o treino:

```bash
python -m sac_rl.run_train --config configs/mujoco_humanoid.yaml
```

Isso inicia o treinamento do ambiente `Humanoid-v5` com 16 simuladores em paralelo, randomização de domínio e aprendizado por currículo (conforme definido no config). Treinar do zero até chegar em uma boa política pode levar algumas horas. Você pode sobrescrever parâmetros em tempo real adicionando pares `chave=valor` no comando. Por exemplo, para mudar o número de ambientes paralelos ou o horizonte de retorno:

```bash
python -m sac_rl.run_train --config configs/mujoco_humanoid.yaml env.vec_envs=32 algo.n_step=2
```

(O comando acima dobraria o número de instâncias do ambiente para 32 e usaria retornos de 2 passos em vez de 3.) **Nota:** se você quiser começar por uma tarefa mais simples, pode treinar o Walker2d usando `--config configs/mujoco_walker2d.yaml`. O Walker2d aprende a andar com bem menos passos, então o treino é bem mais rápido.

**Acompanhe o progresso** – Durante o treinamento, você pode monitorar o desempenho em tempo real. Rode o TensorBoard apontando para a pasta `runs/` para visualizar a curva de aprendizado e outras métricas:

```bash
tensorboard --logdir runs
```

O script de treinamento registra retornos e durações por episódio, perdas de Q, perda do ator, entropia da política e os valores de $\alpha$ (temperatura de entropia). Acompanhar isso no TensorBoard ajuda a verificar se o treino está indo como esperado (por exemplo, retornos aumentando ao longo do tempo, entropia sem colapsar cedo demais, etc.).

**Avalie uma política treinada** – Depois que o treino terminar (ou sempre que você tiver um checkpoint salvo), você pode avaliar a política:

```bash
python -m sac_rl.run_eval --checkpoint runs/mujoco_humanoid/checkpoints/actor_latest.pt --episodes 10 --config configs/mujoco_humanoid.yaml
```

Isso carrega o ator treinado e roda 10 episódios de avaliação, reportando o retorno médio e outras estatísticas. (Você também pode avaliar checkpoints intermediários durante o treino se habilitou o salvamento periódico de checkpoints no config.)

**Visualize a política aprendida** – Use o script do *viewer* interativo para assistir o humanoide em ação:

```bash
python scripts/viewer.py --checkpoint runs/mujoco_humanoid/checkpoints/actor_latest.pt --config configs/mujoco_humanoid.yaml --episodes 3 --deterministic
```

Isso abre uma janela (usando o viewer do MuJoCo) mostrando o humanoide executando a tarefa por alguns episódios. Passamos `--deterministic` para usar a política média (sem ruído de exploração), o que deixa a reprodução mais suave. Você deve ver o robô, que antes só caía, agora conseguindo levantar e andar para frente com consistência.

---
