"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class AnimalClass(str, Enum):
    """Classes de animais detectáveis"""
    BOAR = "boar"           # Javali - alvo principal
    PIG = "pig"             # Porco doméstico
    DEER = "deer"           # Veado
    HUMAN = "human"         # Humano - penalidade máxima
    OTHER = "other"         # Outros animais


class BoundingBox(BaseModel):
    """Caixa delimitadora de detecção"""
    x: float = Field(..., description="Coordenada X do centro")
    y: float = Field(..., description="Coordenada Y do centro")
    width: float = Field(..., description="Largura da caixa")
    height: float = Field(..., description="Altura da caixa")


class SegmentationPoint(BaseModel):
    """Ponto de um polígono de segmentação"""
    x: float = Field(..., description="Coordenada X normalizada (0-1)")
    y: float = Field(..., description="Coordenada Y normalizada (0-1)")


class Detection(BaseModel):
    """Resultado de uma detecção com segmentação opcional"""
    class_name: AnimalClass
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: BoundingBox
    is_target: bool = Field(default=False, description="Se é o alvo (javali)")
    segmentation: Optional[List[SegmentationPoint]] = Field(
        default=None, 
        description="Pontos do contorno de segmentação (polígono)"
    )


class ImageAnalysisRequest(BaseModel):
    """Requisição de análise de imagem"""
    image_base64: str = Field(..., description="Imagem em base64")
    game_session_id: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    """Resposta da análise de imagem"""
    image_id: str
    detections: List[Detection]
    processing_time_ms: float
    has_boar: bool
    boar_count: int


class ClickEvent(BaseModel):
    """Evento de clique do usuário"""
    x: float
    y: float
    timestamp: float
    image_id: str
    game_session_id: str


class ClickResult(BaseModel):
    """Resultado de um clique"""
    hit: bool
    target_class: Optional[AnimalClass]
    points_earned: int
    is_penalty: bool
    message: str


class PlayerScore(BaseModel):
    """Pontuação de um jogador"""
    total_points: int = 0
    correct_hits: int = 0
    wrong_hits: int = 0
    human_hits: int = 0
    reaction_time_avg: float = 0.0


class GameRound(BaseModel):
    """Uma rodada do jogo"""
    round_number: int
    image_id: str
    image_url: str
    time_limit: float
    player_score: PlayerScore
    ai_score: PlayerScore


class GameSession(BaseModel):
    """Sessão de jogo"""
    session_id: str
    created_at: datetime
    rounds_completed: int = 0
    total_rounds: int = 10
    player_total_score: int = 0
    ai_total_score: int = 0
    current_round: Optional[GameRound] = None
    status: str = "active"  # active, completed, abandoned


class GameResult(BaseModel):
    """Resultado final do jogo"""
    session_id: str
    winner: str  # "player", "ai", "tie"
    player_final_score: int
    ai_final_score: int
    player_accuracy: float
    ai_accuracy: float
    total_boars_found: int
    player_stats: PlayerScore
    ai_stats: PlayerScore


class AILearningData(BaseModel):
    """Dados para aprendizado da IA"""
    image_id: str
    player_clicks: List[ClickEvent]
    correct_detections: List[Detection]
    player_success_rate: float
    difficulty_rating: float


class LeaderboardEntry(BaseModel):
    """Entrada do placar de líderes"""
    rank: int
    player_name: str
    score: int
    accuracy: float
    games_played: int
    best_streak: int

