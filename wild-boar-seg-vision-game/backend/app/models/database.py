"""
Modelos do banco de dados SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class GameSessionDB(Base):
    """Tabela de sessões de jogo"""
    __tablename__ = "game_sessions"
    
    id = Column(String, primary_key=True)
    player_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="active")
    
    # Scores
    player_total_score = Column(Integer, default=0)
    ai_total_score = Column(Integer, default=0)
    
    # Stats
    rounds_completed = Column(Integer, default=0)
    total_rounds = Column(Integer, default=10)
    
    # Winner
    winner = Column(String, nullable=True)
    
    # Relationships
    rounds = relationship("GameRoundDB", back_populates="session")
    clicks = relationship("ClickEventDB", back_populates="session")


class GameRoundDB(Base):
    """Tabela de rodadas"""
    __tablename__ = "game_rounds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("game_sessions.id"))
    round_number = Column(Integer)
    image_id = Column(String)
    
    # Scores
    player_points = Column(Integer, default=0)
    ai_points = Column(Integer, default=0)
    
    # Stats
    player_hits = Column(Integer, default=0)
    ai_hits = Column(Integer, default=0)
    player_misses = Column(Integer, default=0)
    ai_misses = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Detections stored as JSON
    detections = Column(JSON, nullable=True)
    
    session = relationship("GameSessionDB", back_populates="rounds")


class ClickEventDB(Base):
    """Tabela de eventos de clique"""
    __tablename__ = "click_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("game_sessions.id"))
    image_id = Column(String)
    
    # Click position
    x = Column(Float)
    y = Column(Float)
    timestamp = Column(Float)
    
    # Result
    hit = Column(Boolean)
    target_class = Column(String, nullable=True)
    points_earned = Column(Integer)
    is_penalty = Column(Boolean, default=False)
    
    session = relationship("GameSessionDB", back_populates="clicks")


class AILearningDB(Base):
    """Tabela de aprendizado da IA"""
    __tablename__ = "ai_learning"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String)
    
    # Learning data
    player_success_rate = Column(Float)
    difficulty_rating = Column(Float)
    
    # Click patterns (JSON)
    click_patterns = Column(JSON)
    
    # Model adjustments
    confidence_adjustment = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeaderboardDB(Base):
    """Tabela de placar de líderes"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String)
    score = Column(Integer)
    accuracy = Column(Float)
    games_played = Column(Integer, default=1)
    best_streak = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

