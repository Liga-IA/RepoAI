#!/usr/bin/env python3
"""
Script de Treinamento de SEGMENTAÇÃO de Javalis
Usa YOLOv8-seg para segmentação de instâncias

Este script treina um modelo para SEGMENTAR (não apenas detectar) javalis
e outros animais em imagens. A segmentação fornece máscaras precisas dos
animais, permitindo uma identificação mais precisa no jogo.

Uso:
    python train_segmentation.py --train --data ../data/dataset.yaml --epochs 100
    python train_segmentation.py --validate --model runs/segment/best.pt
    python train_segmentation.py --predict --model runs/segment/best.pt --source image.jpg
"""

import os
import argparse
from pathlib import Path
import shutil

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    print("⚠️ Ultralytics não instalado. Execute: pip install ultralytics")
    YOLO_AVAILABLE = False


# Configurações padrão para segmentação
DEFAULT_CONFIG = {
    "model": "yolov8n-seg.pt",  # Modelo de SEGMENTAÇÃO (nano)
    "epochs": 100,
    "batch": 16,
    "imgsz": 640,
    "patience": 20,
    "device": "0",  # GPU 0, ou "cpu" para CPU
    "workers": 8,
    "project": "runs/segment",
    "name": "javali_seg",
}

# Modelos de segmentação disponíveis (do menor para o maior)
AVAILABLE_MODELS = {
    "nano": "yolov8n-seg.pt",    # ~3.4M params - mais rápido
    "small": "yolov8s-seg.pt",   # ~11.8M params
    "medium": "yolov8m-seg.pt",  # ~27.3M params
    "large": "yolov8l-seg.pt",   # ~46.0M params
    "xlarge": "yolov8x-seg.pt",  # ~71.8M params - mais preciso
}


def create_segmentation_dataset_yaml(data_dir: Path, output_path: Path):
    """
    Cria arquivo YAML de configuração do dataset para segmentação
    
    Estrutura esperada do dataset:
    data_dir/
        images/
            train/
            val/
            test/
        labels/
            train/
            val/
            test/
    
    Labels para segmentação (formato YOLO-seg):
    class_id x1 y1 x2 y2 x3 y3 ... xn yn
    """
    import yaml
    
    dataset_config = {
        "path": str(data_dir.absolute()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test" if (data_dir / "images" / "test").exists() else "images/val",
        
        # Classes para segmentação
        "names": {
            0: "boar",      # Javali (Sus scrofa) - ALVO PRINCIPAL
            1: "pig",       # Porco doméstico
            2: "deer",      # Veado/Cervo  
            3: "human",     # Humano (penalidade no jogo)
            4: "other",     # Outros animais
        },
        
        "nc": 5  # Número de classes
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(dataset_config, f, default_flow_style=False)
    
    print(f"✅ Dataset YAML de segmentação criado: {output_path}")
    return output_path


def train_segmentation(
    data_yaml: Path,
    model_name: str = DEFAULT_CONFIG["model"],
    epochs: int = DEFAULT_CONFIG["epochs"],
    batch: int = DEFAULT_CONFIG["batch"],
    imgsz: int = DEFAULT_CONFIG["imgsz"],
    device: str = DEFAULT_CONFIG["device"],
    project: str = DEFAULT_CONFIG["project"],
    name: str = DEFAULT_CONFIG["name"],
    resume: bool = False
):
    """
    Treina modelo YOLOv8-seg para segmentação de javalis
    """
    if not YOLO_AVAILABLE:
        print("❌ Ultralytics não disponível. Instale com: pip install ultralytics")
        return None
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐗 TREINAMENTO DE SEGMENTAÇÃO DE JAVALIS                    ║
╠══════════════════════════════════════════════════════════════╣
║  📊 Dataset: {str(data_yaml):<44} ║
║  🔧 Modelo Base: {model_name:<40} ║
║  📈 Épocas: {epochs:<46} ║
║  📦 Batch Size: {batch:<42} ║
║  🖼️  Tamanho Imagem: {imgsz:<38} ║
║  💻 Device: {device:<46} ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Carrega modelo de SEGMENTAÇÃO
    model = YOLO(model_name)
    
    # Treina com configurações otimizadas para segmentação
    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        device=device,
        project=project,
        name=name,
        patience=DEFAULT_CONFIG["patience"],
        workers=DEFAULT_CONFIG["workers"],
        resume=resume,
        
        # Augmentações importantes para segmentação
        hsv_h=0.015,      # Variação de matiz
        hsv_s=0.7,        # Variação de saturação
        hsv_v=0.4,        # Variação de brilho
        degrees=15,       # Rotação (um pouco mais para segmentação)
        translate=0.1,
        scale=0.5,
        shear=5,          # Shear para variedade
        perspective=0.0005,
        flipud=0.0,       # Não inverter verticalmente (animais têm orientação)
        fliplr=0.5,       # Inverter horizontalmente
        
        # Augmentações específicas para segmentação
        mosaic=1.0,       # Mosaic - muito bom para segmentação
        mixup=0.1,        # Mixup - ajuda com generalização
        copy_paste=0.3,   # Copy-paste - CRUCIAL para segmentação
        
        # Configurações de loss
        box=7.5,          # Box loss gain
        cls=0.5,          # Class loss gain
        dfl=1.5,          # DFL loss gain
        
        # Salvar checkpoints
        save=True,
        save_period=10,   # Salva a cada 10 épocas
        plots=True,       # Gera gráficos de métricas
    )
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ TREINAMENTO CONCLUÍDO!                                   ║
╠══════════════════════════════════════════════════════════════╣
║  📁 Resultados: {project}/{name:<38}  ║
║  🏆 Melhor modelo: {project}/{name}/weights/best.pt         ║
║  📊 Último modelo: {project}/{name}/weights/last.pt         ║
╚══════════════════════════════════════════════════════════════╝

Próximos passos:
1. Valide o modelo: python train_segmentation.py --validate --model {project}/{name}/weights/best.pt
2. Teste em imagens: python train_segmentation.py --predict --model {project}/{name}/weights/best.pt --source imagem.jpg
3. Copie o modelo para o backend: cp {project}/{name}/weights/best.pt ../../backend/models/javali_seg.pt
    """)
    
    return results


def validate_segmentation(model_path: Path, data_yaml: Path):
    """
    Valida modelo de segmentação
    """
    if not YOLO_AVAILABLE:
        return None
    
    print(f"🔍 Validando modelo: {model_path}")
    
    model = YOLO(str(model_path))
    results = model.val(data=str(data_yaml))
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  📊 RESULTADOS DA VALIDAÇÃO DE SEGMENTAÇÃO                   ║
╠══════════════════════════════════════════════════════════════╣
║  Box mAP50:     {results.box.map50:.4f}                                      ║
║  Box mAP50-95:  {results.box.map:.4f}                                      ║
║  Mask mAP50:    {results.seg.map50:.4f}                                      ║
║  Mask mAP50-95: {results.seg.map:.4f}                                      ║
║  Box Precisão:  {results.box.mp:.4f}                                      ║
║  Box Recall:    {results.box.mr:.4f}                                      ║
║  Mask Precisão: {results.seg.mp:.4f}                                      ║
║  Mask Recall:   {results.seg.mr:.4f}                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    return results


def predict_segmentation(
    model_path: Path, 
    source: str, 
    save: bool = True,
    show: bool = False,
    conf: float = 0.5
):
    """
    Faz predição de segmentação em imagem(ns)
    """
    if not YOLO_AVAILABLE:
        return None
    
    print(f"🔮 Fazendo predição com: {model_path}")
    print(f"   Fonte: {source}")
    
    model = YOLO(str(model_path))
    
    results = model.predict(
        source=source,
        save=save,
        show=show,
        conf=conf,
        retina_masks=True,  # Máscaras de alta qualidade
        boxes=True,         # Mostrar bounding boxes também
    )
    
    # Mostra resultados
    for result in results:
        if result.masks is not None:
            print(f"\n📸 {result.path}")
            for i, (box, mask) in enumerate(zip(result.boxes, result.masks)):
                cls_id = int(box.cls)
                cls_name = result.names[cls_id]
                conf = float(box.conf)
                print(f"   [{i}] {cls_name}: {conf:.2%}")
        else:
            print(f"   Nenhuma detecção encontrada")
    
    if save:
        print(f"\n✅ Resultados salvos em: runs/segment/predict/")
    
    return results


def export_segmentation_model(model_path: Path, format: str = "onnx"):
    """
    Exporta modelo de segmentação para diferentes formatos
    """
    if not YOLO_AVAILABLE:
        return None
    
    print(f"📦 Exportando modelo para formato: {format}")
    
    model = YOLO(str(model_path))
    export_path = model.export(format=format)
    
    print(f"✅ Modelo exportado: {export_path}")
    return export_path


def prepare_dataset(data_dir: Path):
    """
    Prepara estrutura do dataset para segmentação
    """
    print(f"📁 Preparando estrutura do dataset em: {data_dir}")
    
    # Cria estrutura de pastas
    for split in ["train", "val", "test"]:
        (data_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (data_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
    
    # Cria dataset.yaml
    create_segmentation_dataset_yaml(data_dir, data_dir / "dataset.yaml")
    
    # Cria README
    readme = """# Dataset de Segmentação de Javalis

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
"""
    
    with open(data_dir / "README.md", 'w') as f:
        f.write(readme)
    
    print(f"""
✅ Dataset preparado!

Próximos passos:
1. Adicione imagens em images/train/, images/val/, images/test/
2. Anote as segmentações com CVAT ou Roboflow
3. Exporte labels no formato YOLO para labels/train/, etc.
4. Execute: python train_segmentation.py --train --data {data_dir}/dataset.yaml
    """)


def main():
    parser = argparse.ArgumentParser(
        description="Treinamento de Segmentação de Javalis com YOLOv8-seg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
=========

# Preparar estrutura do dataset
python train_segmentation.py --prepare --data-dir ../data

# Treinar modelo de segmentação
python train_segmentation.py --train --data ../data/dataset.yaml --epochs 100

# Treinar com modelo maior (mais preciso, mais lento)
python train_segmentation.py --train --data ../data/dataset.yaml --model-size large

# Validar modelo treinado
python train_segmentation.py --validate --model runs/segment/javali_seg/weights/best.pt --data ../data/dataset.yaml

# Fazer predição em imagem
python train_segmentation.py --predict --model runs/segment/javali_seg/weights/best.pt --source imagem.jpg

# Exportar modelo para ONNX
python train_segmentation.py --export --model runs/segment/javali_seg/weights/best.pt --format onnx

Modelos disponíveis (--model-size):
- nano: Mais rápido, menos preciso (~3.4M params)
- small: Bom equilíbrio (~11.8M params)
- medium: Mais preciso (~27.3M params)  
- large: Alta precisão (~46.0M params)
- xlarge: Máxima precisão (~71.8M params)
        """
    )
    
    # Comandos
    parser.add_argument("--prepare", action="store_true", help="Prepara estrutura do dataset")
    parser.add_argument("--train", action="store_true", help="Treina o modelo de segmentação")
    parser.add_argument("--validate", action="store_true", help="Valida o modelo")
    parser.add_argument("--predict", action="store_true", help="Faz predição em imagem(ns)")
    parser.add_argument("--export", action="store_true", help="Exporta o modelo")
    
    # Parâmetros
    parser.add_argument("--data-dir", type=Path, default=Path("../data"), help="Diretório do dataset")
    parser.add_argument("--data", type=Path, help="Arquivo YAML do dataset")
    parser.add_argument("--model", type=Path, help="Caminho do modelo treinado")
    parser.add_argument("--model-size", type=str, default="nano", 
                       choices=list(AVAILABLE_MODELS.keys()),
                       help="Tamanho do modelo base")
    parser.add_argument("--epochs", type=int, default=100, help="Número de épocas")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamanho da imagem")
    parser.add_argument("--device", type=str, default="0", help="Device (0 para GPU, cpu para CPU)")
    parser.add_argument("--source", type=str, help="Imagem ou pasta para predição")
    parser.add_argument("--format", type=str, default="onnx", help="Formato de exportação")
    parser.add_argument("--resume", action="store_true", help="Continuar treinamento anterior")
    parser.add_argument("--conf", type=float, default=0.5, help="Threshold de confiança para predição")
    
    args = parser.parse_args()
    
    if args.prepare:
        prepare_dataset(args.data_dir)
    
    elif args.train:
        data_yaml = args.data or args.data_dir / "dataset.yaml"
        
        if not data_yaml.exists():
            print(f"❌ Dataset YAML não encontrado: {data_yaml}")
            print("   Execute primeiro: python train_segmentation.py --prepare")
            return
        
        model_name = AVAILABLE_MODELS[args.model_size]
        
        train_segmentation(
            data_yaml=data_yaml,
            model_name=model_name,
            epochs=args.epochs,
            batch=args.batch,
            imgsz=args.imgsz,
            device=args.device,
            resume=args.resume
        )
    
    elif args.validate:
        if not args.model or not args.data:
            print("❌ Especifique --model e --data para validação")
            return
        validate_segmentation(args.model, args.data)
    
    elif args.predict:
        if not args.model or not args.source:
            print("❌ Especifique --model e --source para predição")
            return
        predict_segmentation(args.model, args.source, conf=args.conf)
    
    elif args.export:
        if not args.model:
            print("❌ Especifique --model para exportação")
            return
        export_segmentation_model(args.model, args.format)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
