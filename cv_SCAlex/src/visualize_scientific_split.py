import os
import torch
import clip
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

# 1. Configurações Estéticas Finais
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "legend.fontsize": 10.5,
    "figure.dpi": 300
})

BASE_DIR = "/home/italo/Downloads/tcc/Imagens_para_TCC"
DATASET_DIR = os.path.join(BASE_DIR, "dataset_split")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CLASSES = ['armas', 'drogas', 'dinheiro', 'outros']
NAME_MAP = {'armas': 'Weapons', 'drogas': 'Drugs', 'dinheiro': 'Currency', 'outros': 'Others'}
COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#7f7f7f'] # Blue, Red, Green, Gray

def extract_features(directory, model, preprocess):
    """Extrai 100% das imagens do diretório para máxima precisão científica."""
    features, labels = [], []
    for idx, cls in enumerate(CLASSES):
        cls_dir = os.path.join(directory, cls)
        if not os.path.exists(cls_dir): continue
        images = [os.path.join(cls_dir, f) for f in os.listdir(cls_dir) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        print(f"  Extracting ALL {len(images)} images for {cls} ({directory.split('/')[-1]})...")
        with torch.no_grad():
            for img_path in tqdm(images, leave=False):
                try:
                    img = preprocess(Image.open(img_path).convert("RGB")).unsqueeze(0).to(DEVICE)
                    feat = model.encode_image(img)
                    feat /= feat.norm(dim=-1, keepdim=True)
                    features.append(feat.cpu().numpy().flatten())
                    labels.append(idx)
                except: continue
    return np.array(features), np.array(labels)

def get_text_centroids(model):
    text_centroids = []
    prompts_dict = {
        'armas': [
            "a forensic photo of a physical metallic firearm", 
            "a real 3D handgun or pistol on a surface", 
            "police evidence photo of a seized metallic revolver", 
            "a firearm with distinct metallic textures and mass", 
            "assault rifles or pistols stored in evidence bags"
        ],
        'drogas': [
            "a forensic photo of illegal narcotics or drugs", 
            "pressed bricks of cocaine or marijuana in plastic", 
            "bags with suspicious white powder or colorful pills", 
            "narcotics displayed as police evidence samples", 
            "a person smoking a joint or a handmade drug cigarette"
        ],
        'dinheiro': [
            "a forensic photo of real physical paper currency", 
            "stacks of real bank bills used in law enforcement", 
            "Brazilian reais banknotes bundled together in cash", 
            "macro photo of cotton-paper security features of money", 
            "authentic banknotes seized during a criminal investigation"
        ],
        'outros': [
            "medicine pills, capsules, blister pack",
            "medical syringe, hospital needle",
            "smartphone, cell phone, mobile",
            "laptop computer, tablet",
            "food, fruit, vegetable",
            "chair, table, sofa, bed",
            "shirt, pants, shoe, hat",
            "wrench, screwdriver, hammer",
            "toy, plastic figure, doll",
            "plant, flower, tree, grass"
        ]
    }
    with torch.no_grad():
        for cls in CLASSES:
            tokens = clip.tokenize(prompts_dict[cls]).to(DEVICE)
            feats = model.encode_text(tokens)
            feats /= feats.norm(dim=-1, keepdim=True)
            text_centroids.append(feats.mean(dim=0, keepdim=True).cpu().numpy().flatten())
    return np.array(text_centroids)

def run_scientific_pca_viz():
    print(f"Gerando Gráfico Final (Full Dataset Integration) com CLIP/{DEVICE}...")
    model, preprocess = clip.load("ViT-B/32", device=DEVICE)
    
    # 1. Dados de Treino -> Centroides (Agora usando TODAS as imagens de treino)
    train_feat, train_labels = extract_features(os.path.join(DATASET_DIR, "train"), model, preprocess)
    text_feat = get_text_centroids(model)
    
    hybrid_centroids = []
    for i in range(4):
        v_mean = train_feat[train_labels == i].mean(axis=0)
        h = 0.5 * text_feat[i] + 0.5 * v_mean
        h /= np.linalg.norm(h)
        hybrid_centroids.append(h)
    hybrid_centroids = np.array(hybrid_centroids)
    
    # 2. Dados de Teste (Agora usando TODAS as imagens de teste)
    test_feat, test_labels = extract_features(os.path.join(DATASET_DIR, "test"), model, preprocess)
    
    # 3. PCA FIT
    pca = PCA(n_components=2, random_state=42)
    pca.fit(np.vstack([train_feat, hybrid_centroids]))
    
    C_2d = pca.transform(hybrid_centroids)
    Test_2d = pca.transform(test_feat)
    
    # 4. ZOOM E MALHA
    all_points = np.vstack([Test_2d, C_2d])
    x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
    y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()
    
    x_margin = (x_max - x_min) * 0.1
    y_margin = (y_max - y_min) * 0.1
    x_lim_min, x_lim_max = x_min - x_margin, x_max + x_margin
    y_lim_min, y_lim_max = y_min - y_margin, y_max + y_margin

    h_mesh = .005
    xx, yy = np.meshgrid(np.arange(x_lim_min, x_lim_max + h_mesh, h_mesh), 
                         np.arange(y_lim_min, y_lim_max + h_mesh, h_mesh))
    
    clf = KNeighborsClassifier(n_neighbors=1)
    clf.fit(C_2d, range(4))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # 5. Plotagem Final
    fig, ax = plt.subplots(figsize=(11, 7))
    
    # Regiões de Decisão
    ax.contourf(xx, yy, Z, alpha=0.22, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], colors=COLORS, antialiased=True)
    ax.contour(xx, yy, Z, colors='black', levels=[0.5, 1.5, 2.5], linewidths=0.6, alpha=0.3)
    
    # Amostras de Teste (Pontos - Todos os ~350 por classe)
    for i in range(4):
        mask = test_labels == i
        if any(mask):
            coords = Test_2d[mask]
            ax.scatter(coords[:, 0], coords[:, 1], c=COLORS[i], 
                       label=f'{NAME_MAP[CLASSES[i]]} (Sample)', alpha=0.45, s=20, edgecolors='none')
    
    # Centroides (Estrelas)
    for i in range(4):
        ax.scatter(C_2d[i, 0], C_2d[i, 1], c=COLORS[i], marker='*', s=500, 
                   edgecolors='black', linewidth=1.5, label=f'{NAME_MAP[CLASSES[i]]} (Centroid)', zorder=25)
    
    # 6. Títulos, Eixos e Legenda
    ax.set_title("SCA-Lex Latent Space: Decision Regions and Sample Distribution", fontweight='bold', pad=15)
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    
    ax.set_xlim(x_lim_min, x_lim_max)
    ax.set_ylim(y_lim_min, y_lim_max)
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=True, 
               labelspacing=0.8, handletextpad=0.8, borderpad=0.6, framealpha=1, edgecolor='silver', 
               title="SCA-Lex Latent Distribution")
    
    plt.grid(True, linestyle='--', alpha=0.1)
    plt.tight_layout()
    
    save_path = os.path.join(BASE_DIR, "tarefas/bracis-Springer_Lecture_Notes_in_Computer_Science/img/fig_latent_space_scientific.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    run_scientific_pca_viz()
