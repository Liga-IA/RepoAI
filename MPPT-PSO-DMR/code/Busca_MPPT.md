# Tutorial – Implementação do PSO-MPPT com DMR no PLECS

<p align="center">
  <img src="../content/PSO_block.png" width=75%>
</p>  

Este documento explica como realizar um teste com o algoritmo **PSO-MPPT com Dynamic Monitoring Reset (DMR)** no **PLECS**.

Você terá um exemplo de simulação mostrando o **reset dinâmico** e a convergência do PSO para o **GMPP**.

---

## Conteúdo

* [Abrindo o Arquivo do Projeto](#abrindo-o-arquivo-do-projeto)
* [Configuração dos Parâmetros do PSO](#configuração-dos-parâmetros-do-pso)
* [Rodando o Exemplo de Reset Dinâmico](#rodando-o-exemplo-de-reset-dinâmico)
* [Resultados Esperados](#resultados-esperados)

---

## Abrindo o Arquivo do Projeto

No repositório, abra o arquivo principal:

```text
code/Busca_MPPT.plecs
```

<p align="center">
  <img src="../content/PLECS_open_MPPT.png" width=75%>
</p>  

---

## Configuração dos Parâmetros do PSO

No início do código (`Busca_MPPT.c`), você pode ajustar os parâmetros:

```c
#define W   0.15   // Inércia
#define C1  0.6    // Peso cognitivo
#define C2  0.6    // Peso social
#define Np  10     // Número de partículas
#define RESET_TOL 0.01 // Tolerância do DMR (1%)
```

📌 Esses parâmetros podem ser alterados para testar diferentes condições de convergência.

---

## Rodando o Exemplo de Reset Dinâmico

O arquivo `Busca_MPPT.plecs` já contém um **cenário com sombreamento parcial dinâmico**.

1. Dê **Run** na simulação.
2. Observe no **Scope**:

   * A potência do painel (Ppv)
   * O duty cycle (D)
   * É possível observar o evento de **reset do DMR**

<p align="center">
  <img src="../content/PLECS_run_MPPT.png" width=80%>
</p>  

---

## Resultados Esperados

O comportamento típico do **PSO-DMR** é:

1. Inicialmente, o PSO converge para um máximo global (**GMPP**).
2. Quando ocorre uma mudança de irradiância, a potência cai fora da zona de tolerância.
3. O **DMR dispara um reset**, reiniciando a população de partículas.
4. O PSO converge para o **GMPP** corretamente.

<p align="center">
  <img src="../content/PSO_reset_example.png" width=85%>
</p>  

> \[!TIP]
> Esse reset dinâmico garante que o sistema **não fique preso em picos locais**, aumentando a eficiência em condições de sombreamento parcial.

---

## Estrutura Relacionada

```text
RepoAI/
└── PSO_MPPT_DMR/
    ├── code/
    │   ├── Busca_MPPT.md          ← este arquivo
    │   ├── Busca_MPPT.c           ← código do PSO com DMR
    │   └── Busca_MPPT.plecs       ← circuito de simulação
    └── content/
        ├── PLECS_open_MPPT.png
        ├── PLECS_Cscript.png
        ├── PLECS_IO_config.png
        ├── PLECS_run_MPPT.png
        ├── PSO_reset_example.png
        └── PSO_block.png
```
