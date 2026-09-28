import os
import torch
import clip
from PIL import Image, ImageFile
import json
from tqdm import tqdm
import numpy as np
from sklearn.metrics import f1_score, accuracy_score

ImageFile.LOAD_TRUNCATED_IMAGES = True

SEMANTIC_PROMPTS = {
    'armas': [
        "a forensic photo of a physical metallic firearm",
        "a real 3D handgun or pistol on a surface",
        "police evidence photo of a seized metallic revolver",
        "close-up of a metallic gun trigger and magazine",
        "assault rifles or pistols stored in evidence bags",
        "a firearm with distinct metallic textures and mass",
        "seized weapon with mechanical parts and barrels",
        "real physical guns recovered in a crime scene",
    ],
    'drogas': [
        "a forensic photo of illegal narcotics or drugs",
        "pressed bricks of cocaine or marijuana in plastic",
        "bags with suspicious white powder or colorful pills",
        "narcotics displayed as police evidence samples",
        "a person smoking a joint or a handmade drug cigarette",
        "cannabis hand-rolled cigarette or joint held by a person",
        "illegal drug consumption or paraphernalia like pipes/needles",
        "crack cocaine, heroin or cannabis being used in a photo",
    ],
    'dinheiro': [
        "a forensic photo of real physical paper currency",
        "stacks of real bank bills used in law enforcement",
        "Brazilian reais banknotes bundled together in cash",
        "macro photo of cotton-paper security features of money",
        "physical paper bills spread out for counting by police",
        "authentic banknotes seized during a criminal investigation",
        "stashed paper currency in bags or legal containers",
        "genuine paper money with watermarks and paper fiber",
    ],
    'outros': [
        "a tattoo of a weapon or gun on human skin",
        "body art and drawing of weapons on person's face",
        "cartoon illustration of coins in a mobile game app",
        "gambling, casino or bingo interface with digital coins",
        "digital currency, fake coins and colorful game assets",
        "a common photo with no forensic or police interest",
        "everyday household objects and non-forensic items",
        "a webpage screenshot, icon or digital design asset",
    ],
}

def extract_features(data_dir, model, preprocess, device):
    classes = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    features_dict = {cls: [] for cls in classes}
    
    with torch.no_grad():
        for cls in classes:
            cls_dir = os.path.join(data_dir, cls)
            imgs = [os.path.join(cls_dir, f) for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            for img_path in tqdm(imgs, desc=f"Extr. {os.path.basename(data_dir)} - {cls}"):
                try:
                    img = preprocess(Image.open(img_path).convert("RGB")).unsqueeze(0).to(device)
                    feat = model.encode_image(img)
                    feat /= feat.norm(dim=-1, keepdim=True)
                    features_dict[cls].append(feat.cpu())
                except Exception:
                    pass
    return features_dict, classes

def run_ablation():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model, preprocess = clip.load("ViT-B/32", device=device)
    
    base_dir = "/home/italo/Downloads/tcc/Imagens_para_TCC"
    train_dir = os.path.join(base_dir, "dataset_split", "train")
    test_dir = os.path.join(base_dir, "dataset_split", "test")
    
    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
        print(f"Erro: diretórios de treino ou teste não encontrados em {base_dir}/dataset_split")
        return

    # Extract train features
    train_feats_dict, classes = extract_features(train_dir, model, preprocess, device)
    
    # Extract test features
    test_feats_dict, _ = extract_features(test_dir, model, preprocess, device)
    
    # Flatten test features for evaluation
    test_features = []
    test_labels = []
    class_to_idx = {cls: i for i, cls in enumerate(classes)}
    
    for cls in classes:
        for feat in test_feats_dict[cls]:
            test_features.append(feat)
            test_labels.append(class_to_idx[cls])
            
    if len(test_features) == 0:
        print("Nenhuma imagem de teste processada com sucesso.")
        return
        
    test_features = torch.cat(test_features).to(device) # [N_test, dim]
    test_labels = np.array(test_labels)
    
    # Flatten train features for k-NN
    train_all_feats = []
    train_all_labels = []
    visual_centroids = {}
    
    for cls in classes:
        cls_feats = torch.cat(train_feats_dict[cls]) # [N_train_cls, dim]
        
        # Média Visual (Visual Centroid)
        v_centroid = cls_feats.mean(dim=0, keepdim=True)
        v_centroid /= v_centroid.norm(dim=-1, keepdim=True)
        visual_centroids[cls] = v_centroid.to(device)
        
        for feat in train_feats_dict[cls]:
            train_all_feats.append(feat)
            train_all_labels.append(class_to_idx[cls])
            
    train_all_feats = torch.cat(train_all_feats).to(device) # [N_train, dim]
    train_all_labels = np.array(train_all_labels)
    
    # Compute Text Centroids
    text_centroids = {}
    with torch.no_grad():
        for cls in classes:
            prompts = SEMANTIC_PROMPTS.get(cls, [f"a photo of {cls}"]).copy()
            # Read custom prompts if available
            custom_path = os.path.join(base_dir, "custom_prompts.json")
            if os.path.exists(custom_path):
                with open(custom_path, "r") as f:
                    custom_dict = json.load(f)
                    prompts.extend(custom_dict.get(cls, []))
            
            text_tokens = clip.tokenize(prompts).to(device)
            t_feats = model.encode_text(text_tokens)
            t_feats /= t_feats.norm(dim=-1, keepdim=True)
            t_centroid = t_feats.mean(dim=0, keepdim=True)
            t_centroid /= t_centroid.norm(dim=-1, keepdim=True)
            text_centroids[cls] = t_centroid.to(device)
            
    # Compute Hybrid Centroids
    hybrid_centroids = {}
    for cls in classes:
        h_centroid = 0.5 * text_centroids[cls] + 0.5 * visual_centroids[cls]
        h_centroid /= h_centroid.norm(dim=-1, keepdim=True)
        hybrid_centroids[cls] = h_centroid.to(device)
        
    def evaluate_centroids(centroids_dict, name):
        weights = torch.cat([centroids_dict[cls] for cls in classes]).to(device) # [num_classes, dim]
        # test_features @ weights.T -> [N_test, num_classes]
        sims = test_features @ weights.T
        preds = sims.argmax(dim=-1).cpu().numpy()
        
        acc = accuracy_score(test_labels, preds)
        f1 = f1_score(test_labels, preds, average='weighted')
        print(f"--- {name} ---")
        print(f"Accuracy: {acc*100:.2f}%")
        print(f"F1-Score: {f1:.4f}\n")
        return acc, f1

    def evaluate_knn():
        # train_all_feats: [N_train, dim], test_features: [N_test, dim]
        # sims: [N_test, N_train]
        sims = test_features @ train_all_feats.T
        best_match_idx = sims.argmax(dim=-1).cpu().numpy()
        preds = train_all_labels[best_match_idx]
        
        acc = accuracy_score(test_labels, preds)
        f1 = f1_score(test_labels, preds, average='weighted')
        print(f"--- 1-NN Visual (Nearest Neighbor) ---")
        print(f"Accuracy: {acc*100:.2f}%")
        print(f"F1-Score: {f1:.4f}\n")
        return acc, f1
        
    print("\n================ STARTING EVALUATION ================\n")
    results = {}
    acc, f1 = evaluate_centroids(text_centroids, "Text-Only Centroids (alpha=0)")
    results["text_only"] = {"acc": acc, "f1": f1}
    
    acc, f1 = evaluate_centroids(visual_centroids, "Visual-Only Centroids (alpha=1)")
    results["visual_only"] = {"acc": acc, "f1": f1}
    
    acc, f1 = evaluate_centroids(hybrid_centroids, "Hybrid Centroids (alpha=0.5)")
    results["hybrid"] = {"acc": acc, "f1": f1}
    
    acc, f1 = evaluate_knn()
    results["knn_visual"] = {"acc": acc, "f1": f1}
    
    # Save results
    out_dir = os.path.join(base_dir, "CR-bracis")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "ablation_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {out_file}")

if __name__ == "__main__":
    run_ablation()
