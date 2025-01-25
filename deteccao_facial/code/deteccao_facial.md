# Detecção Facial e visão computacional

![Imagem na pasta Imagens](/content\imagens\baixados.png)

Neste artigo vamos falar sobre detecção facial e visão computacional, e como podemos utilizar essas tecnologias para criar aplicações.
Abordaremos alguns dos principais metodos  de detecção facial, como o Haar Cascade, e os mais modernos, como o Yunet e DeepFace.
Esse repositório deriva do projeto SD2 da Liga Acadêmica de Inteligência Artificial da UFSC.

**Todos os códigos estão disponíveis no Jupyter Notebook `deteccao_facial.ipynb` e as imagens utilizadas estão na pasta `imagens`. E os modelos de detecção facial estão na pasta `models`.**

Os arquivos dos modelos se encontram na pasta `models`

## O que é a visão computacional?

A visão computacional, um campo interdisciplinar que combina técnicas de computação e processamento de imagens com o objetivo de capacitar os computadores a processar interpretar informações visuais de maneira semelhante a um ser humano mas por meio de algoritmos e técnicas computacionais.


## O que é detecção facial?

Sendo uma das principais áreas de pesquisa, a detecção facial é uma técnica de visão computacional que tem como objetivo identificar faces em uma imagem.
Ela se difere da reconhecimento facial, que tem como objetivo identificar a quem pertence a face detectada.


## OpenCV

OpenCV (Open Source Computer Vision Library) é uma biblioteca de visão computacional e aprendizado de máquina de código aberto.
Ela foi projetada para fornecer uma infraestrutura comum para aplicativos de visão computacional e para acelerar o uso da percepção da máquina em produtos comerciais.
Foi inicialmente desenvolvida pela Intel e atualmente é mantida pela OpenCV.org.


# Modelos de detecção facial

## Haar Cascade Viola Jones
O método de Haar Cascade é um algoritmo de detecção de objetos proposto por Paul Viola e Michael Jones em 2001.
Esse é um algoritmo clássico de detecção de objetos, e é muito utilizado para detecção facial. Ele tambem foi muito utilizado comercialmente, pois possui um desempenho e velocidade relativamente bons mesmo em hardware limitados.

Ele consiste no uso de filtros que são aplicados em uma imagem, que são basicamente retângulos brancos e pretos adjacentes, os quais simulam padrões de claridade e escuridão em regiões da imagem, gerando um mapa de características.

A ideia é que estruturas como olhos (escuros) vs testa e bochecas (claras) possam ser identificadas por esses padrões.

 

![Imagem na pasta Imagens](/content\imagens\haar.png)

## Yunet
O Yunet é um modelo de detecção facial mais moderno, que utiliza redes neurais convolucionais para realizar a detecção. Ele é mais preciso que o Haar Cascade e também mais novo, sendo mais utilizado em aplicações modernas.

![Imagem na pasta Imagens](/content\imagens\yunet_vs_haarcascade.png)

## DeepFace
A biblioteca DeepFace do python permite que você faça reconhecimento facial em imagens com poucas linhas de codigo. Ela é uma biblioteca de código aberto que utiliza redes neurais para realizar a detecção facial.
Ela também permite que você faça reconhecimento facial juntamente com uma análise de atributos como idade, gênero, raça, emoções.

Além disso, a biblioteca permite que você utilize outros modelos de detecção facial no backend, como VGG-Face , FaceNet, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace e GhostFaceNet. O modelo padrão é o VGG-Face.

![Imagem na pasta Imagens](/content\imagens\angelina.jpg)
![Imagem na pasta Imagens](/content\imagens\emotions_age.jpg)



Fontes e saiba mais:


https://opencv.org/blog/opencv-face-detection-cascade-classifier-vs-yunet/

https://github.com/serengil/deepface/tree/master

https://python.plainenglish.io/face-mesh-detection-with-python-and-opencv-complete-project-359d81d6a712

https://medium.com/pythons-gurus/what-is-the-best-face-detector-ab650d8c1225

https://qengineering.eu/install-opencv-on-raspberry-pi.html

https://dev.to/tassi/opencv-raspberry-pi-como-configurar-o-ambiente-m3c

https://github.com/ageitgey/face_recognition

## Contribuidores
  

   [<img loading="lazy" src="https://media.licdn.com/dms/image/v2/D4D03AQHbAzOfHiKbCw/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1712951392343?e=1743033600&v=beta&t=puV7t1bOnAHr0Ic1a1SkmV7oLaTT2FZ5OQYwHf87YSI" width=115><br><sub>Vinicius Wolosky</sub>](https://github.com/vini-muchulski) 

## Estrutura do Repositório

Aqui você deve descrever brevemente a estrutura do repositório

```text
RepoAI/
└── deteccao_facial/
    ├── content/
    │   ├── imagens
    │     
   
    │   
    ├── code/
        ├── deteccao_facial.md <- Você está aqui!
        ├── deteccao_facial.ipynb
        └── models/
                ├── haarcascade_frontalface_default.xml
                └── face_detection_yunet_2023mar.onnx
                
```

## Licença 📝

"Este projeto está sob a licença CC-BY 4.0."