"""
Configurações do aplicativo

Este arquivo lida com configurações que podem ser sobrescritas via
variáveis de ambiente (.env). Para constantes fixas, veja constants.py
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

from . import constants


class Settings(BaseSettings):
    """
    Configurações do sistema carregadas do ambiente.
    
    Valores sensíveis (API keys, secrets) devem estar no .env
    Valores de configuração do jogo estão em constants.py
    """
    
    # ===========================================
    # Informações do App
    # ===========================================
    APP_NAME: str = "Javali Hunter - IA vs Humano"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = constants.DEBUG_MODE
    
    # ===========================================
    # Servidor (pode ser sobrescrito via .env)
    # ===========================================
    HOST: str = constants.DEFAULT_HOST
    PORT: int = constants.DEFAULT_PORT
    
    # ===========================================
    # Paths (calculados automaticamente)
    # ===========================================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR: Path = Path(__file__).resolve().parent.parent
    ML_MODELS_DIR: Path = BACKEND_DIR  # Modelos estão na pasta backend/
    
    # Dataset Agriculture (HTW) - único dataset usado
    AGRICULTURE_DATASET_DIR: Path = BASE_DIR / "ml" / "data" / "data" / "agriculture-jwqz1"
    GAME_IMAGES_DIR: Path = AGRICULTURE_DATASET_DIR / "test" / "images"
    TRAIN_IMAGES_DIR: Path = AGRICULTURE_DATASET_DIR / "train" / "images"
    VALID_IMAGES_DIR: Path = AGRICULTURE_DATASET_DIR / "valid" / "images"
    
    # ===========================================
    # Banco de Dados
    # ===========================================
    DATABASE_URL: str = "sqlite+aiosqlite:///./javali_hunter.db"
    
    # ===========================================
    # Configurações do Jogo (do constants.py)
    # ===========================================
    ROUND_TIME_SECONDS: int = constants.ROUND_TIME_SECONDS
    IMAGES_PER_ROUND: int = constants.IMAGES_PER_ROUND
    
    # Pontuação
    CORRECT_BOAR_POINTS: int = constants.CORRECT_BOAR_POINTS
    WRONG_ANIMAL_PENALTY: int = constants.WRONG_ANIMAL_PENALTY
    HUMAN_HIT_PENALTY: int = constants.HUMAN_HIT_PENALTY
    SPEED_BONUS_MULTIPLIER: float = constants.SPEED_BONUS_MULTIPLIER
    
    # IA
    AI_BASE_CONFIDENCE: float = constants.AI_BASE_CONFIDENCE
    AI_LEARNING_RATE: float = constants.AI_LEARNING_RATE
    
    # Modelo ML
    MODEL_CONFIDENCE_THRESHOLD: float = constants.MODEL_CONFIDENCE_THRESHOLD
    
    # ===========================================
    # API Keys (SENSÍVEIS - do .env)
    # ===========================================
    ROBOFLOW_API_KEY: Optional[str] = None
    
    # ===========================================
    # Segurança (SENSÍVEIS - do .env)
    # ===========================================
    SECRET_KEY: str = "change-this-in-production-use-random-key"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # ===========================================
    # Logging
    # ===========================================
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

