"""
Script de Treinamento do Detector de Javalis
Usa YOLOv8 para fine-tuning em dataset de javalis
"""
import os
import argparse
from pathlib import Path
import yaml
import shutil

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    print("⚠️ Ultralytics não instalado. Execute: pip install ultralytics")
    YOLO_AVAILABLE = False


# Configurações padrão
DEFAULT_CONFIG = {
    "model": "yolov8n.pt",  # Modelo base (nano para velocidade)
    "epochs": 100,
    "batch": 16,
    "imgsz": 640,
    "patience": 20,
    "device": "0",  # GPU 0, ou "cpu" para CPU
    "workers": 8,
    "project": "runs/detect",
    "name": "javali_detector",
}


def create_dataset_yaml(data_dir: Path, output_path: Path):
    """
    Cria arquivo YAML de configuração do dataset
    
    Estrutura esperada do dataset:
    data_dir/
        train/
            images/
            labels/
        val/
            images/
            labels/
        test/  (opcional)
            images/
            labels/
    """
    dataset_config = {
        "path": str(data_dir.absolute()),
        "train": "train/images",
        "val": "val/images",
        "test": "test/images" if (data_dir / "test").exists() else "val/images",
        
        # Classes para detecção
        "names": {
            0: "boar",      # Javali (alvo principal)
            1: "pig",       # Porco doméstico
            2: "deer",      # Veado
            3: "human",     # Humano
            4: "other",     # Outros animais
        },
        
        # Número de classes
        "nc": 5
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(dataset_config, f, default_flow_style=False)
    
    print(f"✅ Dataset YAML criado: {output_path}")
    return output_path


def download_sample_dataset(output_dir: Path):
    """
    Baixa dataset de exemplo do Roboflow (se disponível)
    ou cria estrutura de pastas para dataset manual
    """
    print("📦 Preparando estrutura do dataset...")
    
    # Cria estrutura de pastas
    for split in ["train", "val", "test"]:
        (output_dir / split / "images").mkdir(parents=True, exist_ok=True)
        (output_dir / split / "labels").mkdir(parents=True, exist_ok=True)
    
    # Cria README com instruções
    readme_content = """# Dataset de Javalis para Treinamento

## Estrutura
```
data/
├── train/
│   ├── images/     # Imagens de treino (.jpg, .png)
│   └── labels/     # Anotações YOLO (.txt)
├── val/
│   ├── images/     # Imagens de validação
│   └── labels/     # Anotações de validação
└── test/
    ├── images/     # Imagens de teste
    └── labels/     # Anotações de teste
```

## Formato das Anotações (YOLO)
Cada arquivo .txt deve ter o mesmo nome da imagem correspondente.
Cada linha representa um objeto: `class_id x_center y_center width height`

Classes:
- 0: boar (javali)
- 1: pig (porco doméstico)
- 2: deer (veado)
- 3: human (humano)
- 4: other (outros)

## Fontes de Dados Recomendadas
1. LILA BC Camera Traps: https://lila.science/datasets/
2. Roboflow Universe (Wild Boar): https://universe.roboflow.com/
3. iNaturalist: https://www.inaturalist.org/

## Dicas
- Mínimo recomendado: 500 imagens por classe
- Inclua variações: dia/noite, diferentes ângulos, distâncias
- Balanceie as classes para evitar viés
"""
    
    with open(output_dir / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Estrutura criada em: {output_dir}")
    print("📝 Leia o README.md para instruções de como adicionar dados")


def train_model(
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
    Treina o modelo YOLOv8 para detecção de javalis
    """
    if not YOLO_AVAILABLE:
        print("❌ Ultralytics não disponível. Instale com: pip install ultralytics")
        return None
    
    print(f"""
    🐗 Iniciando Treinamento do Detector de Javalis
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 Dataset: {data_yaml}
    🔧 Modelo Base: {model_name}
    📈 Épocas: {epochs}
    📦 Batch Size: {batch}
    🖼️  Tamanho Imagem: {imgsz}
    💻 Device: {device}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    # Carrega modelo base
    model = YOLO(model_name)
    
    # Treina
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
        
        # Augmentações para robustez
        hsv_h=0.015,  # Variação de matiz
        hsv_s=0.7,    # Variação de saturação
        hsv_v=0.4,    # Variação de brilho
        degrees=10,   # Rotação
        translate=0.1,
        scale=0.5,
        flipud=0.0,   # Não inverter verticalmente
        fliplr=0.5,   # Inverter horizontalmente
        mosaic=1.0,   # Mosaic augmentation
        mixup=0.1,    # Mixup augmentation
    )
    
    print(f"""
    ✅ Treinamento Concluído!
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📁 Resultados salvos em: {project}/{name}
    🏆 Melhor modelo: {project}/{name}/weights/best.pt
    📊 Último modelo: {project}/{name}/weights/last.pt
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    return results


def export_model(model_path: Path, output_dir: Path, format: str = "onnx"):
    """
    Exporta modelo treinado para diferentes formatos
    """
    if not YOLO_AVAILABLE:
        return None
    
    model = YOLO(str(model_path))
    
    # Exporta
    export_path = model.export(format=format)
    
    # Copia para diretório de saída
    output_path = output_dir / f"javali_detector.{format}"
    shutil.copy(export_path, output_path)
    
    print(f"✅ Modelo exportado: {output_path}")
    return output_path


def validate_model(model_path: Path, data_yaml: Path):
    """
    Valida modelo em dataset de teste
    """
    if not YOLO_AVAILABLE:
        return None
    
    model = YOLO(str(model_path))
    
    results = model.val(data=str(data_yaml))
    
    print(f"""
    📊 Resultados da Validação
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    mAP50: {results.box.map50:.4f}
    mAP50-95: {results.box.map:.4f}
    Precisão: {results.box.mp:.4f}
    Recall: {results.box.mr:.4f}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Treinamento do Detector de Javalis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Preparar dataset
  python train_detector.py --prepare-data --data-dir ./data
  
  # Treinar modelo
  python train_detector.py --train --data-yaml ./data.yaml --epochs 100
  
  # Validar modelo
  python train_detector.py --validate --model ./best.pt --data-yaml ./data.yaml
  
  # Exportar modelo
  python train_detector.py --export --model ./best.pt --format onnx
        """
    )
    
    # Comandos
    parser.add_argument("--prepare-data", action="store_true", help="Prepara estrutura do dataset")
    parser.add_argument("--train", action="store_true", help="Treina o modelo")
    parser.add_argument("--validate", action="store_true", help="Valida o modelo")
    parser.add_argument("--export", action="store_true", help="Exporta o modelo")
    
    # Parâmetros
    parser.add_argument("--data-dir", type=Path, default=Path("./data"), help="Diretório do dataset")
    parser.add_argument("--data-yaml", type=Path, help="Arquivo YAML do dataset")
    parser.add_argument("--model", type=Path, help="Caminho do modelo")
    parser.add_argument("--epochs", type=int, default=100, help="Número de épocas")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--device", type=str, default="0", help="Device (0 para GPU, cpu para CPU)")
    parser.add_argument("--format", type=str, default="onnx", help="Formato de exportação")
    parser.add_argument("--resume", action="store_true", help="Continuar treinamento anterior")
    
    args = parser.parse_args()
    
    if args.prepare_data:
        download_sample_dataset(args.data_dir)
        create_dataset_yaml(args.data_dir, args.data_dir / "dataset.yaml")
    
    elif args.train:
        if not args.data_yaml:
            args.data_yaml = args.data_dir / "dataset.yaml"
        
        if not args.data_yaml.exists():
            print(f"❌ Dataset YAML não encontrado: {args.data_yaml}")
            print("   Execute primeiro: python train_detector.py --prepare-data")
            return
        
        train_model(
            data_yaml=args.data_yaml,
            epochs=args.epochs,
            batch=args.batch,
            device=args.device,
            resume=args.resume
        )
    
    elif args.validate:
        if not args.model or not args.data_yaml:
            print("❌ Especifique --model e --data-yaml para validação")
            return
        validate_model(args.model, args.data_yaml)
    
    elif args.export:
        if not args.model:
            print("❌ Especifique --model para exportação")
            return
        export_model(args.model, args.model.parent, args.format)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

