![banner-inicial](content/RepoAI.png)

# Template - RepoAI (Repositório de Conhecimento em IA)

Esse repositório é um modelo (template) para a criação de repositórios do projeto RepoAI. 
Ao mesmo tempo, ele também é um repositório que demonstra como participar do projeto e produzir outros repositórios :D

## Conteúdo
  - [Estilo Visual do Repositório](#estilo-visual-do-reposit%C3%B3rio)
  - [Repositório em Construção](#reposit%C3%B3rio-em-constru%C3%A7%C3%A3o)
  - [Pré-Requisitos e Instalações Necessárias](#se%C3%A7%C3%A3o-de-pr%C3%A9-requisitos-e-instala%C3%A7%C3%B5es-necess%C3%A1rias)
  - [Licença 📝](#licen%C3%A7a-)

## Estrutura do Repositório

Aqui você deve descrever brevemente a estrutura do repositório

```text
RepoAI/
└── seu_repositorio/
    ├── content/
    │   ├── imagens
    │   └── outros
    ├── code/
    |   ├── dados
    |   └── implementação
    ├── README.md
    └── license
    
```

## Estilo Visual e Estrutura do Repositório
Queremos que todos os repositórios publicados sigam o mesmo estilo visual e estrutura, proporcionando assim uma experiência de sinergia aos visitantes. 
Para isso recomendamos os seguintes elementos visuais: 

- Adicione um banner temático no seu repositório. Use o formato de capa para redes sociais. Por exemplo, recomendamos utilizar os templates disponíveis no [Canva](https://www.canva.com/). Seja criativo!
- Utilize seções e subseções seguindo o mesmo estilo desse template, respeitando fontes e tamanhos.
- Logo ao inicio do arquivo, adicione índices dos conteúdos, e a estrutura de pastas do repositório. 
  Após, apresente uma seção de introdução conceitual sobre a técnica escolhida (use quantas subseções desejar), seja didático usando imagens e diagramas.
  Depois, adicione uma seção para apresentar a implementação realizada (use quantas subseções desejar), abordando de forma didática o código e dominio de aplicação. 
  Adicione trechos de código, videos curtos, imagens e explicações pontuais na construção do documento.
  Por último, mantenha uma seção sobre vocês, e, muito importante, a licença indicada.
- Siga a estrutura de pastas indicadas nesse template.


## Repositório em Construção

Se você está desenvolvendo o repositório em grupos, ou mesmo está aberto a contribuições, você pode abrir uma lista simples de tarefas nas seções iniciais, para organizar as tarefas:

- [x] Tarefa 1
- [x] Tarefa 2
- [x] Tarefa 3
- [ ] Tarefa 4
- [ ] Tarefa 5

## Seção de Pré-Requisitos e Instalações Necessárias

Faça uma seção de pré-requisitos e instalações necessárias para a execução do tutorial apresentado junto ao repositório. Por exemplo:

### Pré-requisitos 💻 
Antes de começar, verifique se você atendeu aos seguintes requisitos:
- Você instalou a versão mais recente de `<linguagem / dependência / requeridos>`
- Você tem uma máquina `<Windows / Linux / Mac>`. Indique qual sistema operacional é compatível / não compatível.
- Você leu `<guia / link / documentação_relacionada_ao_projeto>`.

### Instalação 🚀 

Para instalar o <requisito>, siga estas etapas:

Linux e macOS:

```
<comando_de_instalação>
```

Windows:

```
<comando_de_instalação>
```

## Outras Seções 

### Seções Escondidas
Você pode fazer uso de seções escondidas, por exemplo, para exibir trechos de código básico que você acredita que nem todos os leitores terão a necessidade de ver. 
São elementos perfeitos para esse tipo de conteúdo, ou seja, que é opcional para leitores que já possuem algum background sobre o assunto do repositório. Exemplo:

<details>

<summary>Exemplo de Seção Escondida</summary>

### Ela pode conter títulos

Pode conter texto, imagens, blocos, código (essensialmente qualquer coisa)

```python
   print("Hello World").
```
</details>

### Alertas

Você pode usar alertas para enfatizar algum aspecto em seu tutorial: 

> [!NOTE]
> Instruções importantes que os usuários devem conhecer, mesmo ao ler rapidamente o conteúdo.

> [!TIP]
> Dicas úteis para fazer as coisas de forma melhor ou mais fácil.

> [!IMPORTANT]
> Informações essenciais que os usuários precisam saber para alcançar seu objetivo.

> [!WARNING]
> Informações urgentes que exigem a atenção imediata dos usuários para evitar problemas.

> [!CAUTION]
> Alertas sobre os riscos ou possíveis consequências negativas de certas ações.

### Diagramas
Você pode criar diagramas sem a necessidade de ferramentas externas. 
Por exemplo, abaixo é apresentado o diagrama de fluxo de submissão de projetos do repositório:

```mermaid
flowchart TB
    subgraph Equipe
    a1-->|Aprova e Cria|a2[Sub Repositório]
    a3-->|avalia|a4[Avaliação]
    a4-->|aceita|a5[Publicado!]
    end
    subgraph Você
    b1(Interesse)-->|define|b2(Tema)
    b3-->|fork|b4(Repositório)
    b4-->|cria|b5(Conteúdo)
    b5-->|solicita|a3[Merge]
    end
    b2-->|submete|a1[Proposta]
    a2-->|indica|b3(Pastas)
    a4-->|solicita correções|b4
```
[Nesse link](https://mermaid.js.org/intro/) você encontra a documentação para criação de digramas.

### Vídeos e GIF's

#### Adicionando vídeos e GIF's
No GitHub apenas são permitidos incorporações de GIF's e imagens no markdown. Vídeos são dispiníveis apenas por links redirecionados para sites externos ou download de vídeos salvos no projeto.

#### Adicionando GIF
Para adicionar um GIF, utilize a estrutura abaixo

```markdown
![nome](https://url-para-o-gif)
```
![GIF](content/add_gif.gif)


#### Vídeo incorporado (vscode)
Para incorporar vídeos em plataformas que suportam vídeos incorporados(como o vscode), você pode utilizar a seguinte estrutura:
```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

![video-incorporado](content/add_video_yt.gif)


Ou para inserir vídeo local, pode seguir essa estrutura:

```html
<video width="600" controls>
  <source src="video.mp4" type="video/mp4">
</video>
```

![video-local](content/add_video_local.gif)
#### Referencia por links
link para video local:
[Vídeo](content/video.mp4)
```markdown
[video-local](video.mp4)
```

#### Vídeo online
Link para vídeo online:
[Youtube](https://youtu.be/Lc-FuPJavDk?si=JY3LC6LifQtxZkI3)
```markdown
[nome-youtube](https://www.youtube.com/video)
```
#### Link Por imagem
[![Assista ao vídeo](content/image.png)](https://youtu.be/Lc-FuPJavDk?si=JY3LC6LifQtxZkI3)
```markdown
[![Assista ao vídeo](image.png)](https://www.youtube.com/video)
```

## Contribuidores
 Você pode listar todos os contribuidores do seu projeto. Adicione a si mesmo. 

 | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/49369639?v=4" width=115><br><sub>Matheus Lima</sub>](https://github.com/matheus1103) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/11313404?v=4" width=115><br><sub>Alison R. Panisson</sub>](https://github.com/AlisonPanisson) |
| :---: | :---: |

## Licença 📝
Ao final edite o arquivo de licença, atualizando o ano e seu nome, depois adicione uma breve descrição de que seu projeto está sobre a licença CC-BY, por exemplo:

"Esse projeto está sob licença CC-BY 4.0." 

Veja o arquivo [Licença](LICENSE) para mais detalhes.
