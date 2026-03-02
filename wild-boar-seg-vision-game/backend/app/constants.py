"""
Constantes do sistema Javali Hunter

Este arquivo contém todas as constantes de configuração do jogo,
pontuação e IA. Valores que não são sensíveis e podem ser
versionados no repositório.
"""

# ===========================================
# Configurações do Servidor
# ===========================================
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEBUG_MODE = True

# ===========================================
# Configurações do Jogo
# ===========================================
ROUND_TIME_SECONDS = 5  # Tempo por rodada em segundos
IMAGES_PER_ROUND = 10    # Número de imagens por partida

# ===========================================
# Sistema de Pontuação
# ===========================================
CORRECT_BOAR_POINTS = 100       # Pontos por acertar javali
WRONG_ANIMAL_PENALTY = -30      # Penalidade por acertar animal errado
HUMAN_HIT_PENALTY = -200        # Penalidade severa por acertar humano
SPEED_BONUS_MULTIPLIER = 1.5    # Multiplicador de bônus por velocidade

# Pontuação detalhada por classe
POINTS_BY_CLASS = {
    "boar": 100,        # Javali - alvo principal
    "wild-boar": 100,   # Javali selvagem - também alvo
    "monkey": -30,      # Macaco - penalidade
    "dog": -30,         # Cachorro - penalidade
    "person": -200,     # Humano - penalidade severa
    "other": -10,       # Outros - penalidade leve
}

# ===========================================
# Configurações da IA
# ===========================================
AI_BASE_CONFIDENCE = 0.7    # Confiança base da IA (0.0 - 1.0)
AI_LEARNING_RATE = 0.05     # Taxa de aprendizado da IA
AI_REACTION_TIME_BASE = 1.5  # Tempo base de reação da IA em segundos
AI_REACTION_TIME_VARIANCE = 0.5  # Variância no tempo de reação

# ===========================================
# Configurações do Modelo ML
# ===========================================
MODEL_CONFIDENCE_THRESHOLD = 0.5  # Threshold mínimo de confiança para detecção
SEGMENTATION_ENABLED = True       # Habilitar segmentação de instância

# Classes do modelo Agriculture (HTW)
# Mapeamento: índice do modelo -> nome da classe
MODEL_CLASSES = {
    0: "boar",       # Javali - ALVO
    1: "wild-boar",  # Javali selvagem - ALVO
    2: "dog",        # Cachorro - distrator
    3: "monkey",     # Macaco - distrator
    4: "person",     # Pessoa - PENALIDADE
}

# Classes que são alvos válidos (dão pontos positivos)
TARGET_CLASSES = {"boar", "wild-boar"}

# Classes que geram penalidade
PENALTY_CLASSES = {"person"}

# ===========================================
# Dataset Agriculture (HTW)
# ===========================================
DATASET_NAME = "agriculture-jwqz1"
DATASET_SOURCE = "https://universe.roboflow.com/htw-8xh8b/agriculture-jwqz1"
DATASET_SPLITS = ["train", "valid", "test"]

# Distribuição das imagens
DATASET_IMAGES = {
    "train": 1011,
    "valid": 288,
    "test": 144,
    "total": 1443,
}

# ===========================================
# Configurações de UI/UX
# ===========================================
COUNTDOWN_SECONDS = 3        # Contagem regressiva antes da rodada
HIT_MARKER_DURATION = 1.0    # Duração do marcador de acerto em segundos
DETECTION_BOX_COLOR_TARGET = "#22c55e"   # Verde para alvos
DETECTION_BOX_COLOR_PENALTY = "#ef4444"  # Vermelho para penalidades
DETECTION_BOX_COLOR_OTHER = "#f59e0b"    # Amarelo para outros

# ===========================================
# Balanceamento de Imagens
# ===========================================
# Probabilidade de mostrar imagem com javali (0.0 - 1.0)
# Valores recomendados: 0.6 a 0.75 para boa experiência de jogo
BOAR_IMAGE_PROBABILITY = 0.70  # 70% de chance de mostrar imagem com javali

# Classes que indicam "javali" nos labels YOLO (índices 0 e 1)
BOAR_CLASS_INDICES = {0, 1}  # boar, wild-boar
