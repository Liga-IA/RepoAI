# Dataset de Segmentação de Javalis

## Estrutura
```
data/
├── images/
│   ├── train/    # Imagens de treino (~70%)
│   ├── val/      # Imagens de validação (~20%)
│   └── test/     # Imagens de teste (~10%)
├── labels/
│   ├── train/    # Labels de treino
│   ├── val/      # Labels de validação
│   └── test/     # Labels de teste
└── dataset.yaml  # Configuração
```

## Formato das Labels (YOLO-seg)

Cada arquivo .txt deve ter o mesmo nome da imagem correspondente.
Cada linha representa um polígono de segmentação:

```
class_id x1 y1 x2 y2 x3 y3 ... xn yn
```

Onde:
- class_id: ID da classe (0-4)
- x, y: Coordenadas normalizadas (0-1) dos vértices do polígono

### Classes:
- 0: boar (javali) - ALVO PRINCIPAL
- 1: pig (porco doméstico)
- 2: deer (veado)
- 3: human (humano) - PENALIDADE
- 4: other (outros animais)

## Ferramentas de Anotação

1. **CVAT** - https://cvat.ai (recomendado, gratuito)
2. **Roboflow** - https://roboflow.com (fácil de usar)
3. **LabelMe** - pip install labelme (local)
4. **Segment Anything (SAM)** - para auto-segmentação

## Treinamento

```bash
python train_segmentation.py --train --data ./dataset.yaml --epochs 100
```
