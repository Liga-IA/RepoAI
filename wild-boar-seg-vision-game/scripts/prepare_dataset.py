#!/usr/bin/env python3
"""
Script para preparar o dataset de treinamento do modelo de detecção de javalis.

Este script:
1. Copia as imagens do frontend para a estrutura de ML
2. Cria estrutura de pastas para YOLO (train/val/test)
3. Gera arquivo YAML do dataset
4. Cria anotações placeholder para iniciar o treinamento supervisionado

IMPORTANTE: 
- Para um modelo robusto, você precisará anotar as imagens manualmente.
- Use ferramentas como LabelImg, CVAT, ou Roboflow para anotação.
- Este script cria labels placeholder que precisam ser verificados.
"""

import os
import sys
import shutil
import random
import json
from pathlib import Path
import argparse

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


def create_directory_structure(data_dir: Path):
    """Cria estrutura de diretórios para o dataset YOLO"""
    
    subdirs = [
        "train/images",
        "train/labels", 
        "val/images",
        "val/labels",
        "test/images",
        "test/labels",
    ]
    
    for subdir in subdirs:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)
        
    print(f"✅ Estrutura de diretórios criada em: {data_dir}")


def copy_images_from_frontend(data_dir: Path, split_ratios: dict = None):
    """
    Copia imagens do frontend para o dataset de ML
    
    Args:
        data_dir: Diretório de destino para os dados
        split_ratios: Proporções de divisão (train, val, test)
    """
    if split_ratios is None:
        split_ratios = {"train": 0.7, "val": 0.2, "test": 0.1}
    
    frontend_images_dir = BASE_DIR / "frontend" / "public" / "images"
    
    # Coleta todas as imagens
    image_files = []
    
    # Imagens sample_XX.jpg
    for img_file in frontend_images_dir.glob("sample_*.jpg"):
        image_files.append(img_file)
    
    # Imagens da pasta Sus_scrofa (iNaturalist)
    sus_scrofa_dir = frontend_images_dir / "Sus_scrofa"
    if sus_scrofa_dir.exists():
        for img_file in sus_scrofa_dir.glob("*.jpg"):
            image_files.append(img_file)
    
    print(f"📸 Encontradas {len(image_files)} imagens")
    
    if not image_files:
        print("⚠️ Nenhuma imagem encontrada!")
        return
    
    # Embaralha e divide
    random.shuffle(image_files)
    
    n_total = len(image_files)
    n_train = int(n_total * split_ratios["train"])
    n_val = int(n_total * split_ratios["val"])
    
    splits = {
        "train": image_files[:n_train],
        "val": image_files[n_train:n_train + n_val],
        "test": image_files[n_train + n_val:],
    }
    
    for split_name, files in splits.items():
        dest_dir = data_dir / split_name / "images"
        for src_file in files:
            dst_file = dest_dir / src_file.name
            shutil.copy2(src_file, dst_file)
        print(f"  {split_name}: {len(files)} imagens copiadas")
    
    print(f"✅ Imagens copiadas para {data_dir}")


def create_placeholder_labels(data_dir: Path):
    """
    Cria labels placeholder para as imagens.
    
    ATENÇÃO: Estes são labels genéricos que assumem um javali centralizado.
    Para treinamento real, as labels devem ser criadas manualmente usando
    ferramentas de anotação como LabelImg, CVAT, ou Roboflow.
    
    Formato YOLO:
        class_id x_center y_center width height
        (valores normalizados 0-1)
    """
    print("\n📝 Criando labels placeholder...")
    print("⚠️ ATENÇÃO: Estes são labels genéricos! Para um modelo robusto,")
    print("   anote as imagens manualmente usando LabelImg, CVAT ou Roboflow.")
    
    for split in ["train", "val", "test"]:
        images_dir = data_dir / split / "images"
        labels_dir = data_dir / split / "labels"
        
        for img_file in images_dir.glob("*.jpg"):
            label_file = labels_dir / f"{img_file.stem}.txt"
            
            # Label placeholder: classe 0 (boar), centralizado, tamanho médio
            # Formato: class_id x_center y_center width height
            with open(label_file, 'w') as f:
                # Posição aleatória realista para simular variação
                x_center = 0.3 + random.random() * 0.4  # 0.3 a 0.7
                y_center = 0.4 + random.random() * 0.3  # 0.4 a 0.7
                width = 0.15 + random.random() * 0.2    # 0.15 a 0.35
                height = 0.1 + random.random() * 0.15   # 0.1 a 0.25
                
                f.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    print("✅ Labels placeholder criados")


def create_dataset_yaml(data_dir: Path):
    """Cria arquivo YAML de configuração do dataset"""
    
    yaml_content = f"""# Javali Hunter Dataset
# Configuração para treinamento YOLOv8

path: {data_dir.absolute()}
train: train/images
val: val/images
test: test/images

# Classes de detecção
# 0: boar     - Javali (Sus scrofa) - ALVO PRINCIPAL
# 1: pig      - Porco doméstico
# 2: deer     - Veado/Cervo
# 3: human    - Humano (EVITAR!)
# 4: other    - Outros animais

names:
  0: boar
  1: pig
  2: deer
  3: human
  4: other

nc: 5  # Número de classes

# Notas:
# - Classe 0 (boar) é o alvo principal do jogo
# - Classe 3 (human) deve ter penalidade severa
# - Para um modelo robusto, baixe imagens adicionais de cada classe
"""
    
    yaml_path = data_dir / "dataset.yaml"
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"✅ Arquivo YAML criado: {yaml_path}")
    return yaml_path


def create_training_readme(data_dir: Path):
    """Cria README com instruções de treinamento"""
    
    readme_content = """# Dataset de Javalis para Treinamento

## 📊 Estrutura do Dataset

```
data/
├── train/
│   ├── images/     # Imagens de treino
│   └── labels/     # Anotações YOLO (.txt)
├── val/
│   ├── images/     # Imagens de validação
│   └── labels/     # Anotações de validação
├── test/
│   ├── images/     # Imagens de teste
│   └── labels/     # Anotações de teste
└── dataset.yaml    # Configuração do dataset
```

## 🏷️ Classes

| ID | Classe | Descrição | Pontuação no Jogo |
|----|--------|-----------|-------------------|
| 0  | boar   | Javali    | +100 pts (ALVO)   |
| 1  | pig    | Porco     | -15 pts           |
| 2  | deer   | Veado     | -30 pts           |
| 3  | human  | Humano    | -200 pts          |
| 4  | other  | Outros    | -30 pts           |

## 📝 Formato das Anotações (YOLO)

Cada arquivo `.txt` na pasta `labels/` deve ter o mesmo nome da imagem correspondente.
Cada linha representa um objeto:

```
class_id x_center y_center width height
```

Exemplo:
```
0 0.5 0.5 0.3 0.2
```
Significa: javali (0) centralizado, ocupando 30% da largura e 20% da altura.

## ⚠️ IMPORTANTE: Anotação Manual

Os labels gerados automaticamente são **PLACEHOLDERS**!
Para um modelo robusto, você deve:

1. **Usar ferramentas de anotação**:
   - [LabelImg](https://github.com/tzutalin/labelImg) - Simples, offline
   - [CVAT](https://cvat.ai/) - Web, colaborativo
   - [Roboflow](https://roboflow.com/) - Web, com augmentation

2. **Verificar e corrigir cada label**

3. **Adicionar mais imagens** (veja seção abaixo)

## 📥 Fontes de Dados Recomendadas

Para equilibrar o dataset, baixe imagens de:

### 1. Javalis (classe 0) - PRIORIDADE
- [iNaturalist - Sus scrofa](https://www.inaturalist.org/observations?taxon_id=42134)
- [LILA BC Camera Traps](https://lila.science/datasets/)
- [Roboflow Universe - Wild Boar](https://universe.roboflow.com/search?q=wild%20boar)

### 2. Porcos Domésticos (classe 1)
- [iNaturalist - Sus domesticus](https://www.inaturalist.org/taxa/42131)
- Pesquise "pig detection dataset" no Kaggle

### 3. Veados (classe 2)
- [LILA BC - Deer datasets](https://lila.science/datasets/)
- [Roboflow - Deer detection](https://universe.roboflow.com/search?q=deer)

### 4. Humanos (classe 3)
- [COCO Dataset - Person class](https://cocodataset.org/)
- Imagens de trilhas/câmeras de monitoramento

### 5. Outros Animais (classe 4)
- Qualquer animal de fauna silvestre
- Câmeras trap datasets

## 🚀 Treinamento

```bash
# Navegue para o diretório ml/training
cd ml/training

# Execute o treinamento
python train_detector.py --train --data-yaml ../data/dataset.yaml --epochs 100

# Para continuar treinamento
python train_detector.py --train --data-yaml ../data/dataset.yaml --resume
```

## 📈 Métricas Esperadas

Para um modelo utilizável:
- mAP50: > 0.7
- mAP50-95: > 0.5
- Precisão: > 0.8
- Recall: > 0.7

## 💡 Dicas

1. **Mínimo recomendado**: 200 imagens por classe
2. **Ideal**: 500+ imagens por classe
3. **Inclua variações**: 
   - Dia/noite (infravermelho)
   - Diferentes ângulos
   - Diferentes distâncias
   - Oclusão parcial
4. **Balanceie as classes** para evitar viés
5. **Use augmentation** durante o treinamento
"""
    
    readme_path = data_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ README criado: {readme_path}")


def print_dataset_stats(data_dir: Path):
    """Imprime estatísticas do dataset"""
    
    print("\n📊 Estatísticas do Dataset:")
    print("=" * 50)
    
    for split in ["train", "val", "test"]:
        images_dir = data_dir / split / "images"
        labels_dir = data_dir / split / "labels"
        
        n_images = len(list(images_dir.glob("*.jpg")))
        n_labels = len(list(labels_dir.glob("*.txt")))
        
        print(f"  {split:6s}: {n_images:4d} imagens, {n_labels:4d} labels")
    
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Prepara dataset para treinamento do detector de javalis"
    )
    parser.add_argument(
        "--output-dir", 
        type=Path, 
        default=BASE_DIR / "ml" / "data",
        help="Diretório de saída para o dataset"
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.7,
        help="Proporção de imagens para treino (default: 0.7)"
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Proporção de imagens para validação (default: 0.2)"
    )
    parser.add_argument(
        "--skip-copy",
        action="store_true",
        help="Pular cópia de imagens (usar se já copiou)"
    )
    
    args = parser.parse_args()
    
    print("🐗 Preparando Dataset do Javali Hunter")
    print("=" * 50)
    
    # Cria estrutura de diretórios
    create_directory_structure(args.output_dir)
    
    # Copia imagens
    if not args.skip_copy:
        test_ratio = 1.0 - args.train_ratio - args.val_ratio
        split_ratios = {
            "train": args.train_ratio,
            "val": args.val_ratio,
            "test": test_ratio,
        }
        copy_images_from_frontend(args.output_dir, split_ratios)
    
    # Cria labels placeholder
    create_placeholder_labels(args.output_dir)
    
    # Cria arquivo YAML
    create_dataset_yaml(args.output_dir)
    
    # Cria README
    create_training_readme(args.output_dir)
    
    # Estatísticas
    print_dataset_stats(args.output_dir)
    
    print("\n✅ Dataset preparado com sucesso!")
    print("\n⚠️ PRÓXIMOS PASSOS:")
    print("1. Verifique e corrija as anotações manualmente")
    print("2. Baixe mais imagens para equilibrar as classes")
    print("3. Execute o treinamento:")
    print("   cd ml/training")
    print("   python train_detector.py --train --data-yaml ../data/dataset.yaml")


if __name__ == "__main__":
    main()
