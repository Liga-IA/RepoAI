"""
Serviço de Gerenciamento do Jogo
"""
import uuid
import time
import random
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from ..models.schemas import (
    GameSession, GameRound, GameResult, PlayerScore,
    ClickEvent, ClickResult, Detection, AnimalClass
)
from ..config import settings
from .detection_service import detection_service


class GameService:
    """Serviço para gerenciar sessões de jogo"""
    
    def __init__(self):
        """Inicializa o serviço de jogo"""
        # Armazena sessões ativas em memória
        self.active_sessions: Dict[str, GameSession] = {}
        
        # Cache de detecções por imagem
        self.detection_cache: Dict[str, List[Detection]] = {}
        
        # Estado da IA por sessão
        self.ai_state: Dict[str, dict] = {}
        
        # Imagens de exemplo para o jogo
        self.sample_images: List[str] = []
        self._load_sample_images()
    
    def _load_sample_images(self):
        """Carrega imagens do dataset Agriculture (HTW) para o jogo"""
        extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
        # Prioridade: test > valid > train do dataset Agriculture
        image_dirs = [
            settings.GAME_IMAGES_DIR,   # test/images (144 imagens)
            settings.VALID_IMAGES_DIR,  # valid/images (288 imagens)
            settings.TRAIN_IMAGES_DIR,  # train/images (1011 imagens)
        ]
        
        for images_dir in image_dirs:
            if images_dir.exists():
                images = [
                    str(p) for p in images_dir.iterdir()
                    if p.suffix.lower() in extensions
                ]
                if images:
                    self.sample_images.extend(images)
                    print(f"✅ Carregadas {len(images)} imagens de {images_dir.name}")
        
        if self.sample_images:
            print(f"🎮 Total de {len(self.sample_images)} imagens do dataset Agriculture disponíveis")
        else:
            print("⚠️ Nenhuma imagem encontrada no dataset Agriculture")
    
    def create_session(self, player_name: Optional[str] = None) -> GameSession:
        """
        Cria uma nova sessão de jogo
        
        Args:
            player_name: Nome opcional do jogador
            
        Returns:
            Nova GameSession
        """
        session_id = str(uuid.uuid4())
        
        session = GameSession(
            session_id=session_id,
            created_at=datetime.utcnow(),
            rounds_completed=0,
            total_rounds=settings.IMAGES_PER_ROUND,
            player_total_score=0,
            ai_total_score=0,
            status="active"
        )
        
        self.active_sessions[session_id] = session
        
        # Inicializa estado da IA
        self.ai_state[session_id] = {
            "confidence": settings.AI_BASE_CONFIDENCE,
            "reaction_time_base": 1.5,  # segundos
            "accuracy_bonus": 0.0,
            "learned_patterns": []
        }
        
        return session
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Obtém uma sessão existente"""
        return self.active_sessions.get(session_id)
    
    def start_round(self, session_id: str, image_base64: str) -> Tuple[GameRound, List[Detection]]:
        """
        Inicia uma nova rodada
        
        Args:
            session_id: ID da sessão
            image_base64: Imagem da rodada em base64
            
        Returns:
            Tupla (GameRound, detecções da imagem)
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        
        # Analisa a imagem com segmentação habilitada
        analysis = detection_service.analyze_image(image_base64, return_masks=True)
        
        # Armazena detecções no cache
        self.detection_cache[analysis.image_id] = analysis.detections
        
        # Cria a rodada
        round_num = session.rounds_completed + 1
        
        game_round = GameRound(
            round_number=round_num,
            image_id=analysis.image_id,
            image_url="",  # Será preenchido pelo frontend
            time_limit=settings.ROUND_TIME_SECONDS,
            player_score=PlayerScore(),
            ai_score=PlayerScore()
        )
        
        session.current_round = game_round
        
        return game_round, analysis.detections
    
    def process_player_click(
        self, 
        session_id: str, 
        click: ClickEvent
    ) -> ClickResult:
        """
        Processa um clique do jogador
        
        Args:
            session_id: ID da sessão
            click: Evento de clique
            
        Returns:
            Resultado do clique
        """
        session = self.active_sessions.get(session_id)
        if not session or not session.current_round:
            return ClickResult(
                hit=False,
                target_class=None,
                points_earned=0,
                is_penalty=False,
                message="Sessão inválida"
            )
        
        # Obtém detecções da imagem
        detections = self.detection_cache.get(click.image_id, [])
        
        # Verifica acerto
        hit, detection = detection_service.check_click_hit(
            click.x, click.y, detections
        )
        
        if not hit:
            return ClickResult(
                hit=False,
                target_class=None,
                points_earned=0,
                is_penalty=False,
                message="Tiro na água! Nenhum animal atingido."
            )
        
        # Calcula pontos baseado no tipo de acerto
        points, is_penalty, message = self._calculate_points(detection)
        
        # Atualiza pontuação do jogador
        session.player_total_score += points
        player_score = session.current_round.player_score
        
        if detection.is_target:
            player_score.correct_hits += 1
        else:
            player_score.wrong_hits += 1
            if detection.class_name == AnimalClass.HUMAN:
                player_score.human_hits += 1
        
        player_score.total_points += points
        
        return ClickResult(
            hit=True,
            target_class=detection.class_name,
            points_earned=points,
            is_penalty=is_penalty,
            message=message
        )
    
    def _calculate_points(self, detection: Detection) -> Tuple[int, bool, str]:
        """
        Calcula pontos para uma detecção
        
        Returns:
            Tupla (pontos, é_penalidade, mensagem)
        """
        if detection.is_target:
            # Acertou javali!
            bonus = int(detection.confidence * 50)  # Bônus por confiança
            points = settings.CORRECT_BOAR_POINTS + bonus
            return points, False, f"🎯 Javali detectado! +{points} pontos"
        
        if detection.class_name == AnimalClass.HUMAN:
            # Penalidade severa por acertar humano
            return settings.HUMAN_HIT_PENALTY, True, "⚠️ HUMANO ATINGIDO! Penalidade severa aplicada!"
        
        if detection.class_name == AnimalClass.PIG:
            # Penalidade menor por porco doméstico
            return settings.WRONG_ANIMAL_PENALTY // 2, True, "🐷 Porco doméstico! Penalidade leve."
        
        # Outros animais
        return settings.WRONG_ANIMAL_PENALTY, True, f"❌ Animal errado ({detection.class_name.value})! Penalidade aplicada."
    
    async def simulate_ai_turn(
        self, 
        session_id: str, 
        detections: List[Detection]
    ) -> List[ClickResult]:
        """
        Simula a vez da IA com base nas detecções e aprendizado
        
        Args:
            session_id: ID da sessão
            detections: Detecções na imagem atual
            
        Returns:
            Lista de resultados dos "cliques" da IA
        """
        session = self.active_sessions.get(session_id)
        ai_state = self.ai_state.get(session_id, {})
        
        if not session or not session.current_round:
            return []
        
        results = []
        ai_confidence = ai_state.get("confidence", settings.AI_BASE_CONFIDENCE)
        base_reaction = ai_state.get("reaction_time_base", 1.5)
        
        for detection in detections:
            # IA decide se vai "clicar" baseado na confiança
            should_click = random.random() < ai_confidence
            
            # Adiciona ruído realista - IA pode errar
            if detection.is_target:
                # Maior chance de acertar javalis
                should_click = should_click or random.random() < 0.3
            else:
                # Pode evitar não-alvos
                if detection.class_name == AnimalClass.HUMAN:
                    # IA é mais cuidadosa com humanos
                    should_click = should_click and random.random() < 0.1
                elif random.random() < 0.2:
                    # 20% de chance de erro em não-alvos
                    should_click = True
            
            if should_click:
                # Simula tempo de reação
                reaction_time = base_reaction * random.uniform(0.8, 1.2)
                await asyncio.sleep(min(reaction_time, 0.1))  # Cap para não travar
                
                points, is_penalty, message = self._calculate_points(detection)
                
                # Atualiza pontuação da IA
                session.ai_total_score += points
                ai_score = session.current_round.ai_score
                
                if detection.is_target:
                    ai_score.correct_hits += 1
                else:
                    ai_score.wrong_hits += 1
                    if detection.class_name == AnimalClass.HUMAN:
                        ai_score.human_hits += 1
                
                ai_score.total_points += points
                
                results.append(ClickResult(
                    hit=True,
                    target_class=detection.class_name,
                    points_earned=points,
                    is_penalty=is_penalty,
                    message=f"🤖 IA: {message}"
                ))
        
        return results
    
    def end_round(self, session_id: str) -> GameRound:
        """Finaliza a rodada atual"""
        session = self.active_sessions.get(session_id)
        if not session or not session.current_round:
            raise ValueError("Sessão ou rodada inválida")
        
        current_round = session.current_round
        session.rounds_completed += 1
        
        # Limpa cache de detecções
        if current_round.image_id in self.detection_cache:
            del self.detection_cache[current_round.image_id]
        
        return current_round
    
    def end_game(self, session_id: str) -> GameResult:
        """
        Finaliza o jogo e calcula resultado
        
        Returns:
            GameResult com estatísticas finais
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError("Sessão não encontrada")
        
        session.status = "completed"
        
        # Determina vencedor
        if session.player_total_score > session.ai_total_score:
            winner = "player"
        elif session.ai_total_score > session.player_total_score:
            winner = "ai"
        else:
            winner = "tie"
        
        # Calcula estatísticas
        player_stats = PlayerScore(
            total_points=session.player_total_score,
            correct_hits=0,
            wrong_hits=0,
            human_hits=0
        )
        
        ai_stats = PlayerScore(
            total_points=session.ai_total_score,
            correct_hits=0,
            wrong_hits=0,
            human_hits=0
        )
        
        # Calcula precisão (evita divisão por zero)
        player_total_shots = player_stats.correct_hits + player_stats.wrong_hits
        ai_total_shots = ai_stats.correct_hits + ai_stats.wrong_hits
        
        player_accuracy = (
            player_stats.correct_hits / player_total_shots * 100 
            if player_total_shots > 0 else 0
        )
        ai_accuracy = (
            ai_stats.correct_hits / ai_total_shots * 100
            if ai_total_shots > 0 else 0
        )
        
        result = GameResult(
            session_id=session_id,
            winner=winner,
            player_final_score=session.player_total_score,
            ai_final_score=session.ai_total_score,
            player_accuracy=player_accuracy,
            ai_accuracy=ai_accuracy,
            total_boars_found=player_stats.correct_hits + ai_stats.correct_hits,
            player_stats=player_stats,
            ai_stats=ai_stats
        )
        
        # Remove sessão ativa
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.ai_state:
            del self.ai_state[session_id]
        
        return result


# Instância global
game_service = GameService()

