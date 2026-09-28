import os
import torch
import clip
from PIL import Image, ImageFile
import torchvision.models as models
from torchvision import transforms
from ultralytics import YOLO
import json
import time
import numpy as np
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix

# Configurações
ImageFile.LOAD_TRUNCATED_IMAGES = True
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TEST_DIR = "dataset_split/test"
CLASSES = ["armas", "dinheiro", "drogas", "outros"]# Modelos CNN
CNN_MODELS = {
    "ResNet-18": "benchmark_resnet18.pth",
    "ResNet-50": "benchmark_resnet50.pth",
    "MobileNetV3": "benchmark_mobilenet_v3.pth",
    "ViT-B/16": "benchmark_vit_b16.pth",
    "YOLOv8-cls": "runs/classify/train/weights/best.pt",
}

TRANSFORM = transforms.Compose([
    transforms.Resize(256), transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_cnn(name, path):
    if name == "ResNet-18": m = models.resnet18(); m.fc = torch.nn.Linear(m.fc.in_features, 4)
    elif name == "ResNet-50": m = models.resnet50(); m.fc = torch.nn.Linear(m.fc.in_features, 4)
    elif name == "MobileNetV3": m = models.mobilenet_v3_large(); m.classifier[3] = torch.nn.Linear(m.classifier[3].in_features, 4)
    elif name == "ViT-B/16": m = models.vit_b_16(); m.heads[0] = torch.nn.Linear(m.heads[0].in_features, 4)
    else: return YOLO(path)
    
    if os.path.exists(path):
        m.load_state_dict(torch.load(path, map_location=DEVICE))
    m.to(DEVICE).eval()
    return m

def get_clip_prediction(img_path, model, preprocess, centroids):
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        features = model.encode_image(image)
        features /= features.norm(dim=-1, keepdim=True)
        
        sims = {c: torch.cosine_similarity(features, centroids[c]).max().item() for c in CLASSES}
        winner = max(sims, key=sims.get)
        return winner, sims

def evaluate():
    print(f"--- 🔬 EVALUATING FORENSIC ENSEMBLE (v27.4) ON {DEVICE} ---")
    
    # 1. Carrega CLIP e Centróides
    model_clip, preprocess = clip.load("ViT-B/32", device=DEVICE)
    with open("centroids_final.pkl", "rb") as f:
        import pickle
        centroids = pickle.load(f)
        for c in centroids: centroids[c] = torch.tensor(centroids[c]).to(DEVICE)

    # 2. Carrega CNNs e YOLO
    nets = {name: load_cnn(name, path) for name, path in CNN_MODELS.items()}
    
    y_true = []
    y_pred_ensemble = []
    y_pred_clip = []
    y_pred_resnet = []

    for label in CLASSES:
        class_path = os.path.join(TEST_DIR, label)
        if not os.path.exists(class_path): continue
        
        imgs = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Processando {label}: {len(imgs)} imagens...")
        
        for img_name in imgs:
            path = os.path.join(class_path, img_name)
            try:
                # 1. CLIP Prediction (Standalone Baseline)
                current_clip_win, _ = get_clip_prediction(path, model_clip, preprocess, centroids)
                
                # 2. CNNs and YOLO (Ensemble - 5 Specialist Models)
                img_pil = Image.open(path).convert("RGB")
                img_t = TRANSFORM(img_pil).unsqueeze(0).to(DEVICE)
                
                council = [] # v27.4: CLIP isolado da votação (Duelo Final)
                current_resnet_win = None

                with torch.no_grad():
                    for name, net in nets.items():
                        if name == "YOLOv8-cls":
                            res = net(path, verbose=False)[0]
                            c_idx = res.probs.top1
                            winner = CLASSES[c_idx] if c_idx < 4 else "outros"
                        else:
                            out = net(img_t)
                            winner = CLASSES[torch.argmax(out).item()]
                        
                        council.append(winner)
                        if name == "ResNet-50": current_resnet_win = winner

                # 3. Ensemble Logic (5 Models: Majority 3/5)
                counts = Counter(council)
                win_cat, win_count = counts.most_common(1)[0]
                
                # Voto Majoritário Absoluto entre os 5 especialistas
                final_ensemble_win = win_cat
                
                # --- ALL COMPLETED SUCCESSFULLY: Append to results (v27.4) ---
                y_true.append(label)
                y_pred_clip.append(current_clip_win)
                y_pred_resnet.append(current_resnet_win)
                y_pred_ensemble.append(final_ensemble_win)

            except Exception as e:
                print(f"Pulando imagem corrompida {path}: {e}")
                continue

    # 3. Gerar Relatórios
    print("\n--- 📊 RESULTS: SINGLE CLIP (BASELINE) ---")
    print(classification_report(y_true, y_pred_clip))
    
    print("\n--- 📊 RESULTS: ENSEMBLE (5 SPECIALISTS COUNCIL) ---")
    report = classification_report(y_true, y_pred_ensemble, output_dict=True)
    print(classification_report(y_true, y_pred_ensemble))
    
    # Salva métricas para o LaTeX
    results = {
        "clip": classification_report(y_true, y_pred_clip, output_dict=True),
        "ensemble": report,
        "resnet": classification_report(y_true, y_pred_resnet, output_dict=True),
    }
    with open("forensic_ensemble_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n✅ Métricas salvas em forensic_ensemble_results.json")

if __name__ == "__main__":
    evaluate()
