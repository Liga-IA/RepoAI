# Fine-tuning do Qwen2.5 em um dataset de flashcards médicos com QLoRA

O Fine-tuning de um modelo de linguagem de grande escala (LLM) consiste em utilizar um modelo base pré-treinado e **treiná-lo adicionalmente em um dataset menor e específico de domínio**, com o objetivo de adaptar o conhecimento do modelo a uma tarefa ou área. Essa abordagem é mais eficiente do que treinar do zero, pois o modelo base já codifica padrões gerais de linguagem e fatos aprendidos a partir de um corpus amplo. Com o fine-tuning, **preserva-se o conhecimento geral do modelo** e **o comportamento é especializado** para o caso de uso.

Este artigo descreve o fine-tuning de um LLM open-source — **Qwen2.5-1.5B Instruct** (modelo com 1,5 bilhão de parâmetros) — em um **dataset de perguntas e respostas médicas** no formato de flashcards. O objetivo é especializar o Qwen2.5 como um assistente médico capaz de responder perguntas clínicas e biomédicas com maior precisão. Para viabilizar o treinamento em uma única GPU, é utilizado um método parameter-efficient chamado **QLoRA (Quantized LoRA)** no Google Colab (NVIDIA T4 com 16 GB de VRAM), com tempo de treinamento em torno de 2 horas. Ao longo do texto, são apresentados conceitos como LoRA e QLoRA, são fornecidos trechos de código para cada etapa e é comparado o desempenho do **modelo base vs. modelo com fine-tuning** em perguntas médicas.

## O que é LoRA (Low-Rank Adaptation)?

**LoRA** é uma técnica de *parameter-efficient fine-tuning* que reduz drasticamente a quantidade de parâmetros treináveis necessária para adaptar um LLM a uma nova tarefa. Em vez de atualizar todos os pesos do modelo durante o fine-tuning (o que envolveria bilhões de parâmetros em modelos grandes), o LoRA **injeta duas matrizes pequenas de baixa dimensão (low-rank)** em cada camada alvo e **congela os pesos originais**. Essas matrizes (comumente chamadas de *LoRA adapters*) são treinadas para capturar os ajustes necessários nos pesos. Ao final do treinamento, os pesos originais permanecem inalterados, e o adapter aprendido (em geral com poucos megabytes) pode ser acoplado ao modelo para incorporar o conhecimento da nova tarefa. Com isso, **apenas uma fração mínima dos parâmetros (tipicamente <1%) é atualizada** durante o fine-tuning, o que torna o processo **eficiente em memória** e reduz o risco de degradação do conhecimento previamente aprendido.

*Benefícios principais do LoRA:* redução substancial de uso de memória de GPU (a maior parte do modelo permanece congelada) e redução de custo de armazenamento (salva-se apenas o adapter, sem necessidade de um checkpoint completo do modelo para cada tarefa). Em termos de qualidade, o LoRA frequentemente atinge **desempenho comparável ao full fine-tuning** apesar de atualizar muito menos pesos. Na inferência, o adapter pode ser mesclado aos pesos do modelo base, **sem introduzir latência adicional** em relação a um modelo integralmente ajustado.

## O que é QLoRA (Quantized LoRA)?

Embora o LoRA reduza o número de parâmetros treináveis, ainda é necessário **carregar o modelo base completo em memória** durante o treinamento. Em modelos muito grandes, isso pode se tornar um gargalo. **QLoRA** contorna esse problema ao combinar LoRA com *quantization*. Em QLoRA, os pesos do modelo base são carregados em **precisão de 4 bits** (em vez de 16 bits), reduzindo drasticamente a ocupação de memória, e os adapters LoRA são aplicados sobre esse modelo quantizado. O modelo base permanece congelado nessa forma comprimida, e o fine-tuning é realizado apenas nos adapters LoRA. A técnica foi apresentada por Dettmers et al. (2023) e permite fine-tuning de modelos muito grandes (dezenas de bilhões de parâmetros) em uma única GPU **sem perda significativa de desempenho** em comparação ao treinamento em 16 bits.

Na prática, o QLoRA pode reduzir o uso de memória em ~75% ou mais ao utilizar pesos em 4 bits. Há demonstrações de fine-tuning de um modelo com 65 bilhões de parâmetros em uma única GPU de 48GB usando QLoRA, algo inviável com métodos tradicionais. A pequena perda de precisão associada ao quantization é compensada por esquemas cuidadosamente projetados (como o formato 4-bit NormalFloat — NF4 — e **double quantization** para outliers) que preservam a acurácia do modelo. Em síntese, **QLoRA combina a eficiência do LoRA com uma redução agressiva do footprint do modelo**, o que viabiliza fine-tuning em hardware mais limitado, como uma T4.

---

Com esses conceitos estabelecidos, o fluxo completo do projeto é descrito a seguir, do setup do ambiente ao treinamento e avaliação, espelhando um workflow típico de fine-tuning de um LLM em um dataset customizado com QLoRA.

## Ambiente e setup

O ambiente é configurado em um notebook do Google Colab com GPU. O Colab (ou qualquer ambiente Jupyter com GPU) facilita a execução interativa do código de treinamento. O runtime utilizado disponibiliza uma NVIDIA T4 (~16 GB de VRAM), suficiente para um modelo de 1.5B com quantization em 4 bits. O processo completo (uma epoch em ~34k exemplos) leva aproximadamente **2 horas** nessa configuração.

Instalação das bibliotecas necessárias: Transformers (modelo e tokenizer), Datasets (carregamento de dados), Accelerate e PEFT (suporte a LoRA/QLoRA), BitsAndBytes (quantization em 4 bits), TRL (opcional, utilitários de treinamento) e Evaluate (métricas):

```bash
!pip -q install -U pip

!pip -q install "numpy>=2,<2.1"

!pip -q install -U \
  "transformers>=4.41,<5" \
  "datasets>=2.19.0" \
  "accelerate>=0.28.0" \
  "peft>=0.10.0" \
  "bitsandbytes>=0.43.0" \
  "trl>=0.9.6" \
  "evaluate>=0.4.1" \
  "fsspec==2025.3.0" \
  "gcsfs==2025.3.0"
```

Após a instalação, o PyTorch é importado e a disponibilidade de GPU e memória é verificada:

```python
import torch
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
    print(round(torch.cuda.get_device_properties(0).total_memory/1024**3, 2), "GB")
else:
    print("CUDA indisponível")
```

A seguir, são definidos parâmetros de configuração para o fine-tuning:

```python
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
DATASET_NAME = "flwrlabs/medical-meadow-medical-flashcards"
MAX_SEQ_LEN = 1024
BATCH_SIZE = 4
GRAD_ACCUM_STEPS = 4
LEARNING_RATE = 2e-4
NUM_EPOCHS = 1
OUTPUT_DIR = "outputs"
ADAPTER_OUTPUT_DIR = "outputs/adapter"
```

É adotado um batch pequeno (4) com *gradient accumulation* para obter batch efetivo de 16 sem exceder memória. É selecionado learning rate de 2e-4 (comumente adequado para LoRA) e uma epoch para demonstração. Uma epoch significa que cada exemplo do treinamento é visto uma vez; para ~34k flashcards, esse volume costuma ser suficiente para melhorar desempenho em um domínio específico.

## Carregamento do dataset de flashcards médicos

O dataset `flwrlabs/medical-meadow-medical-flashcards`, disponível no Hugging Face, contém pares de perguntas e respostas formatados para instruction tuning. Cada amostra possui **instruction**, **input** e **output**:

- **instruction:** um prompt ou diretriz (por exemplo *"Answer this question truthfully"*, frequentemente usada para orientar a resposta).
- **input:** a pergunta médica (por exemplo *"What are the contraindications for using β-blockers?"*).
- **output:** a resposta de referência.

O dataset possui apenas o split "train" (33.955 flashcards no total), portanto é criado manualmente um split de teste com 5% para avaliação:

```python
from datasets import load_dataset

dataset = load_dataset(DATASET_NAME, split="train")
data_split = dataset.train_test_split(test_size=0.05, seed=SEED)
train_dataset = data_split["train"]
eval_dataset = data_split["test"]

print(f"Train samples: {len(train_dataset)}, Eval samples: {len(eval_dataset)}")
```

Após o split, ficam aproximadamente 32k exemplos em treino e ~1,7k em avaliação.

## Preparação dos dados em chat prompt format

O Qwen2.5-1.5B é um modelo instruction-tuned para chat. A entrada esperada segue um formato conversacional, tipicamente com mensagens de *system*, *user* e (no treinamento) *assistant*. Para aproveitar o formato nativo do modelo, cada exemplo do dataset é convertido em uma única string que representa uma conversa: o *user* faz a pergunta e o *assistant* fornece a resposta.

Template adotado:
- Mensagem **system** no início: *"You are a helpful medical assistant."* (define contexto e tom).
- Mensagem **user** contendo `instruction` + `input`.
- Mensagem **assistant** contendo `output` (a resposta de referência).

O tokenizer do Qwen oferece um utilitário para gerar o chat prompt format. Uma função aplica esse template:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def apply_template(example):
    user_content = example["instruction"] + "\n" + example["input"]
    messages = [
        {"role": "system", "content": "You are a helpful medical assistant."},
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": example["output"]},
    ]
    formatted_text = tokenizer.apply_chat_template(messages, tokenize=False)
    return {"text": formatted_text}

train_dataset = train_dataset.map(apply_template, remove_columns=train_dataset.column_names)
eval_dataset  = eval_dataset.map(apply_template, remove_columns=eval_dataset.column_names)
```

O método `tokenizer.apply_chat_template` formata a lista de mensagens para a serialização exata esperada pelo modelo. Após o mapeamento, cada item do dataset contém um único campo `"text"`, com um conteúdo semelhante a:

```
<system>You are a helpful medical assistant.</system>
<user>Answer this question truthfully. What are the precautions and contraindications for the use of β-blockers?</user>
<assistant>β-blockers must be used cautiously in decompensated heart failure and are contraindicated in cardiogenic shock...</assistant>
```

## Tokenization e data collation

Em seguida, o texto formatado é convertido em tokens (`input_ids`). Também são preparados `labels` para treinamento. Em causal language modeling, `labels` costuma ser uma cópia de `input_ids`, pois o objetivo é prever o próximo token da sequência (incluindo a resposta do assistant, condicionada ao prompt). Para simplificar, o prompt e a resposta são tratados como uma única sequência para o modelo prever.

Cada exemplo é tokenizado com limite de 1024 tokens:

```python
def tokenize_function(sample):
    result = tokenizer(sample["text"], truncation=True, max_length=MAX_SEQ_LEN, padding=False)
    result["labels"] = result["input_ids"].copy()
    return result

train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
eval_dataset  = eval_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
```

O campo `"text"` é removido, ficando `"input_ids"`, `"attention_mask"` e `"labels"`.

```python
import torch

def data_collator(features):
    input_ids = [torch.tensor(f["input_ids"], dtype=torch.long) for f in features]
    attention_masks = [torch.tensor(f["attention_mask"], dtype=torch.long) for f in features]
    labels = [torch.tensor(f["labels"], dtype=torch.long) for f in features]
    batch = {}
    batch["input_ids"] = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    batch["attention_mask"] = torch.nn.utils.rnn.pad_sequence(attention_masks, batch_first=True, padding_value=0)
    batch["labels"] = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=-100)
    return batch
```

Nesse ponto, o dataset está pronto: prompts formatados e tokenizados.

## Carregamento do Qwen2.5 em 4-bit e aplicação de LoRA

Com os dados preparados, o setup do modelo para QLoRA envolve:

1. **Carregar o Qwen2.5-1.5B Instruct** com quantization em 4 bits.
2. **Preparar o modelo para k-bit training** (ajustes necessários ao treinar com pesos 4-bit/8-bit).
3. **Configurar LoRA** e anexar adapters ao modelo.

**BitsAndBytes 4-bit Quantization:** `BitsAndBytesConfig` (Transformers) é usado para especificar carregamento em 4-bit. As opções seguem recomendações do paper de QLoRA: `bnb_4bit_quant_type="nf4"` (NormalFloat, melhora a acurácia do quantization) e `bnb_4bit_use_double_quant=True` (double quantization para outliers, reduzindo memória). `bnb_4bit_compute_dtype=torch.bfloat16` é definido para realizar compute em bfloat16 (preferível para estabilidade).

Carregamento do modelo:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)
```

A função `prepare_model_for_kbit_training` aplica ajustes internos (por exemplo, cast de layer norms para FP32 e modificações relacionadas a gradientes) para reduzir problemas ao treinar um modelo quantizado. A partir daí, o modelo está em 4-bit e pronto para receber o LoRA.

**Configuração de LoRA:** o LoRA é aplicado as principais matrizes de pesos. No Qwen (arquitetura Transformer decoder), os módulos-alvo incluem:
- Projeções de self-attention: `q_proj`, `k_proj`, `v_proj`, `o_proj`
- Projeções do feed-forward: `gate_proj`, `up_proj`, `down_proj`

Essa seleção cobre os componentes de attention e feed-forward, onde estão as matrizes de maior dimensão. Parâmetros:
- `r=16` (rank dos adapters; bom trade-off entre capacidade e tamanho)
- `lora_alpha=32` (escala das atualizações)
- `lora_dropout=0.05` (regularização)
- `bias="none"` (sem bias)
- `task_type="CAUSAL_LM"`

```python
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
```

Para verificar quantos parâmetros são treináveis:

```python
def print_trainable_parameters(model):
    trainable = 0
    total = 0
    for _, param in model.named_parameters():
        total += param.numel()
        if param.requires_grad:
            trainable += param.numel()
    print(trainable)
    print(total)
    print(trainable/total)
print_trainable_parameters(model)
```

O esperado é que apenas uma fração muito pequena seja treinável (bem abaixo de 1%), confirmando a eficiência: **mais de 99% dos pesos permanece congelado**, e o ajuste ocorre nos adapters.

## Fine-tuning do modelo com QLoRA

O treinamento é conduzido com o `Trainer` (Hugging Face), por simplicidade. `TrainingArguments` é configurado com hiperparâmetros e opções relevantes:

- `gradient_accumulation_steps=4` para simular batch maior.
- `fp16=True` para mixed precision (os adapters podem ser treinados com FP16).
- `optim="paged_adamw_8bit"` (8-bit AdamW do bitsandbytes), reduzindo memória do estado do optimizer.
- `logging_steps=10` para logs frequentes; `eval_steps=50` e `save_steps=50` para avaliação e checkpointing periódicos.
- `report_to="none"` para desativar reporting/telemetria.

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM_STEPS,
    num_train_epochs=NUM_EPOCHS,
    learning_rate=LEARNING_RATE,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=50,
    save_total_limit=1,
    fp16=True,
    bf16=False,
    optim="paged_adamw_8bit",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator
)
```

Início do treinamento:

```python
trainer.train()
```

Durante o treinamento, o loss tende a diminuir, e avaliações ocorrem a cada 50 steps. Com ~32k exemplos de treino e batch efetivo 16, foram realizados 2017 update steps em uma epoch.

Ao final, uma avaliação adicional pode ser executada:

```python
trainer.evaluate()
```

Isso fornece o evaluation loss final. Para esse tipo de tarefa, a avaliação qualitativa costuma ser mais esclarecedora do que métricas automáticas genéricas.

## Salvamento do modelo após fine-tuning

Como LoRA foi utilizado, o artefato final é composto por **modelo base + pesos do adapter LoRA**. O adapter pode ser salvo em disco (artefato leve) junto com o tokenizer:

```python
model.save_pretrained(ADAPTER_OUTPUT_DIR)
tokenizer.save_pretrained(ADAPTER_OUTPUT_DIR)
```

O `ADAPTER_OUTPUT_DIR` passa a conter o adapter (tipicamente poucos MB) e arquivos do tokenizer. Para usar o modelo depois, o procedimento padrão é carregar o `Qwen/Qwen2.5-1.5B-Instruct` e aplicar o adapter com PEFT.

Opcionalmente, os pesos do LoRA podem ser mesclados no modelo base para gerar um checkpoint único (por exemplo com `PeftModel.merge_and_unload()`). Isso produz um artefato do tamanho total do modelo, aumentando custo de armazenamento; manter o adapter separado costuma ser a escolha mais prática.

## Inferência com o modelo após fine-tuning

Para testar o modelo após o fine-tuning, o modelo base é carregado em 4-bit e o adapter é aplicado:

```python
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model = PeftModel.from_pretrained(model, ADAPTER_OUTPUT_DIR)
model.eval()
```

Uma função de chat pode ser definida para gerar respostas:

```python
def chat(query):
    messages = [
        {"role": "system", "content": "You are a helpful medical assistant."},
        {"role": "user", "content": query}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response
```

A função cria o prompt com mensagens *system* e *user*, chama `model.generate` e decodifica apenas os tokens gerados (ignorando o prompt).

Exemplo:

```python
query = "A 67-year-old patient with atrial fibrillation is on warfarin and starts trimethoprim-sulfamethoxazole. What complication is most likely, and why?"
print(chat(query))
```

Esse cenário clínico corresponde a uma interação conhecida: warfarin (anticoagulante) com TMP-SMX (antibiótico), elevando risco de sangramento.

**Resposta do modelo após fine-tuning (Modelo F):**

*“Trimethoprim-sulfamethoxazole can enhance the effect of warfarin, leading to an increased risk of bleeding (over-anticoagulation). This happens because TMP-SMX interferes with warfarin’s metabolism, causing warfarin levels to rise and the blood to become too thin, so the patient is more likely to bleed.”*

A resposta identifica corretamente sangramento como complicação provável e justifica pelo mecanismo (interferência no metabolismo do warfarin).

## Resultados: modelo base vs. modelo com fine-tuning (Modelo B vs. Modelo F)

Para mensurar o efeito do fine-tuning, é realizada a comparação entre o modelo base (antes do fine-tuning) e o modelo especializado. O Qwen2.5-1.5B Instruct, sem especialização em medicina (**Modelo B**), pode produzir respostas convincentes, porém incorretas ou irrelevantes em perguntas médicas especializadas. Já o modelo com fine-tuning (**Modelo F**) tende a produzir respostas mais alinhadas ao conhecimento médico e às respostas de referência do dataset.

No exemplo da interação warfarin + TMP-SMX, a comparação pode ser resumida:

- **Pergunta:** *A 67-year-old patient with atrial fibrillation is on warfarin and starts trimethoprim-sulfamethoxazole. What complication is most likely, and why?*

- **Resposta do modelo base (Modelo B):** *“Such a patient could most likely develop **blood clots** because the antibiotic might reduce warfarin’s effectiveness. Trimethoprim-sulfamethoxazole can induce liver enzymes and cause warfarin levels to drop, leading to insufficient anticoagulation and thus clot formation.”*

- **Resposta do modelo com fine-tuning (Modelo F):** *“Trimethoprim-sulfamethoxazole can enhance the effect of warfarin, leading to an increased risk of bleeding (over-anticoagulation). This happens because TMP-SMX interferes with warfarin’s metabolism, causing warfarin levels to rise and the blood to become too thin, so the patient is more likely to bleed.”*

A diferença é clara. A resposta do modelo base é **confiante e totalmente incorreta**: afirma o efeito oposto (trombose por redução do efeito do warfarin), um erro de alto impacto em um cenário real. O Modelo B não captura a interação específica e “inventa” um mecanismo de indução enzimática. Em contraste, o Modelo F, treinado com dados médicos, identifica corretamente o aumento de risco de sangramento e apresenta uma explicação válida. Trata-se de um exemplo claro de **“high-confidence, high-impact errors”** no modelo base, corrigidos por fine-tuning de domínio.

Melhorias semelhantes aparecem em outras perguntas, por exemplo:

- **Pergunta:** *After 10 days of clindamycin, a patient develops watery diarrhea and cramping. What is the likely diagnosis and first-line treatment?*  
  **Modelo B:** Diagnóstico correto (CDI), porém descreve tratamento incorreto ou enganoso (uso de vancomicina IV, mecanismo errado, esquemas e condutas não recomendadas).  
  **Modelo F:** *“The likely diagnosis is Clostridioides difficile infection (CDI); first-line treatment is oral vancomycin or fidaxomicin.”* — alinhado às diretrizes clínicas.

- **Pergunta:** *A patient with chronic kidney disease has high phosphate and low calcium. What happens to PTH over time, and what bone changes result?*  
  **Modelo B:** Perde o nexo fisiopatológico central e contém erros conceituais (origem do PTH, efeitos renais do hormônio), resultando em explicação difusa.  
  **Modelo F:** Responde de forma causal e correta: DRC → hiperfosfatemia/hipocalcemia → **hiperparatireoidismo secundário** → **osteodistrofia renal** (especialmente osteíte fibrosa).

Em cada caso, o Modelo F se mantém mais próximo do conhecimento médico esperado, enquanto o Modelo B frequentemente falha em detalhe e precisão. O fine-tuning no conjunto de flashcards Medical Meadow funciona como uma especialização direcionada para Q&A médico, aumentando a confiabilidade nesse domínio.

## Conclusão

O projeto demonstra como realizar fine-tuning de um modelo open-source de 1.5B parâmetros (Qwen2.5) em um dataset de domínio usando QLoRA. O processo inclui preparação dos dados em chat prompt format, quantization em 4-bit para acomodar o modelo em uma única GPU e treinamento de uma fração mínima dos parâmetros via LoRA adapters. O resultado é um modelo de Q&A médico especializado, que supera o modelo base em perguntas relevantes, **corrigindo erros de alta confiança** e gerando explicações mais consistentes e precisas.

**Principais pontos:**

- Fine-tuning com **LoRA/QLoRA** é efetivo para adaptação de domínio, atingindo resultados fortes com uma epoch e recursos computacionais modestos, devido à atualização de <1% dos parâmetros e ao uso de compressão em 4-bit.
- O modelo com fine-tuning (Modelo F) se torna mais confiável em perguntas médicas, reduzindo erros formulados com alta confiança e melhorando a consistência das explicações.
- O uso de **chat-formatted prompt** e de mensagem *system* ajuda a alinhar as saídas ao estilo esperado (respostas médicas úteis e factuais).
- O mesmo fluxo pode ser aplicado a outros domínios (direito, finanças, etc.), utilizando QLoRA para criar modelos especialistas sem infraestrutura pesada.

Como conclusão, o QLoRA amplia o acesso ao fine-tuning de LLMs ao reduzir requisitos de hardware. Com preparação adequada e um dataset apropriado, um modelo relativamente pequeno como o Qwen2.5-1.5B pode se tornar especialista em um domínio específico. O procedimento descrito fornece um template para projetos semelhantes, demonstrando como um dataset direcionado e um método eficiente de fine-tuning podem elevar a qualidade do modelo em tarefas especializadas em poucas horas de execução.
