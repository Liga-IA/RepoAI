"""
Serviço de Aprendizado Adaptativo da IA
"""
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import numpy as np

from ..models.schemas import (
    ClickEvent, Detection, AnimalClass, AILearningData
)
from ..config import settings
from .detection_service import detection_service


class AILearningService:
    """
    Serviço para aprendizado adaptativo da IA
    
    A IA aprende com os padrões de acertos e erros do humano para:
    1. Melhorar sua própria precisão
    2. Ajustar tempo de reação
    3. Identificar padrões de dificuldade em imagens
    """
    
    def __init__(self):
        """Inicializa o serviço de aprendizado"""
        # Histórico de cliques por imagem
        self.click_history: Dict[str, List[ClickEvent]] = defaultdict(list)
        
        # Padrões aprendidos por classe de animal
        self.class_patterns: Dict[str, dict] = {}
        
        # Ajustes de confiança aprendidos
        self.confidence_adjustments: Dict[str, float] = {}
        
        # Histórico de performance humana
        self.human_performance: Dict[str, dict] = {}
        
        # Taxa de aprendizado
        self.learning_rate = settings.AI_LEARNING_RATE
        
        # Métricas globais
        self.global_metrics = {
            "total_rounds": 0,
            "human_correct": 0,
            "human_wrong": 0,
            "ai_correct": 0,
            "ai_wrong": 0,
            "avg_reaction_time": 0.0
        }
    
    def record_human_click(
        self,
        session_id: str,
        click: ClickEvent,
        hit: bool,
        detection: Optional[Detection],
        detections: List[Detection]
    ):
        """
        Registra um clique do humano para aprendizado
        
        Args:
            session_id: ID da sessão
            click: Evento de clique
            hit: Se acertou algo
            detection: Detecção acertada (se houver)
            detections: Todas as detecções na imagem
        """
        # Registra no histórico
        self.click_history[click.image_id].append(click)
        
        # Atualiza métricas globais
        if hit and detection:
            if detection.is_target:
                self.global_metrics["human_correct"] += 1
            else:
                self.global_metrics["human_wrong"] += 1
        
        # Aprende padrões de clique
        self._learn_from_click(click, hit, detection, detections)
    
    def _learn_from_click(
        self,
        click: ClickEvent,
        hit: bool,
        detection: Optional[Detection],
        detections: List[Detection]
    ):
        """Extrai aprendizado de um clique"""
        if not hit or not detection:
            return
        
        class_name = detection.class_name.value
        
        # Inicializa padrões da classe se necessário
        if class_name not in self.class_patterns:
            self.class_patterns[class_name] = {
                "hit_count": 0,
                "miss_count": 0,
                "avg_confidence_when_hit": 0.0,
                "position_bias": {"x": 0.0, "y": 0.0},
                "size_preference": {"width": 0.0, "height": 0.0}
            }
        
        pattern = self.class_patterns[class_name]
        
        if detection.is_target:
            pattern["hit_count"] += 1
            
            # Atualiza média de confiança
            old_avg = pattern["avg_confidence_when_hit"]
            n = pattern["hit_count"]
            pattern["avg_confidence_when_hit"] = old_avg + (detection.confidence - old_avg) / n
            
            # Aprende preferência de posição (onde humanos tendem a clicar mais rápido)
            alpha = self.learning_rate
            pattern["position_bias"]["x"] += alpha * (click.x - pattern["position_bias"]["x"])
            pattern["position_bias"]["y"] += alpha * (click.y - pattern["position_bias"]["y"])
            
            # Aprende preferência de tamanho
            pattern["size_preference"]["width"] += alpha * (detection.bbox.width - pattern["size_preference"]["width"])
            pattern["size_preference"]["height"] += alpha * (detection.bbox.height - pattern["size_preference"]["height"])
        else:
            pattern["miss_count"] += 1
    
    def update_ai_confidence(
        self,
        session_id: str,
        player_accuracy: float,
        ai_accuracy: float
    ):
        """
        Atualiza confiança da IA baseado na performance comparativa
        
        Args:
            session_id: ID da sessão
            player_accuracy: Precisão do jogador na rodada
            ai_accuracy: Precisão da IA na rodada
        """
        # Se jogador está muito melhor, IA aumenta agressividade
        accuracy_diff = player_accuracy - ai_accuracy
        
        adjustment = self.learning_rate * accuracy_diff / 100
        
        # Aplica ajuste às classes mais erradas
        for class_name, pattern in self.class_patterns.items():
            total = pattern["hit_count"] + pattern["miss_count"]
            if total > 0:
                error_rate = pattern["miss_count"] / total
                
                # Ajusta confiança inversamente ao erro
                class_adjustment = adjustment * (1 - error_rate)
                
                current = self.confidence_adjustments.get(class_name, 0.0)
                self.confidence_adjustments[class_name] = max(-0.3, min(0.3, current + class_adjustment))
                
                # Propaga para o serviço de detecção
                detection_service.update_confidence_adjustment(class_name, class_adjustment)
    
    def get_ai_recommendations(
        self,
        detections: List[Detection]
    ) -> List[Dict]:
        """
        Obtém recomendações da IA sobre quais detecções priorizar
        
        Args:
            detections: Lista de detecções na imagem
            
        Returns:
            Lista de recomendações ordenada por prioridade
        """
        recommendations = []
        
        for detection in detections:
            class_name = detection.class_name.value
            pattern = self.class_patterns.get(class_name, {})
            
            # Calcula score de prioridade
            priority = detection.confidence
            
            # Boost para alvos
            if detection.is_target:
                priority *= 1.5
            
            # Penalidade para classes com alto erro humano
            if pattern:
                total = pattern.get("hit_count", 0) + pattern.get("miss_count", 0)
                if total > 0:
                    success_rate = pattern.get("hit_count", 0) / total
                    priority *= (0.5 + 0.5 * success_rate)
            
            # Penalidade severa para humanos
            if detection.class_name == AnimalClass.HUMAN:
                priority *= 0.1
            
            recommendations.append({
                "detection": detection,
                "priority": priority,
                "should_click": priority > 0.5 and detection.class_name != AnimalClass.HUMAN
            })
        
        # Ordena por prioridade
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        
        return recommendations
    
    def calculate_difficulty(self, detections: List[Detection]) -> float:
        """
        Calcula dificuldade de uma imagem baseado nas detecções
        
        Returns:
            Score de dificuldade (0-1)
        """
        if not detections:
            return 0.5
        
        # Fatores de dificuldade
        num_detections = len(detections)
        num_targets = sum(1 for d in detections if d.is_target)
        num_humans = sum(1 for d in detections if d.class_name == AnimalClass.HUMAN)
        avg_confidence = np.mean([d.confidence for d in detections])
        
        # Mais detecções = mais difícil
        detection_factor = min(1.0, num_detections / 10)
        
        # Menos alvos = mais difícil
        target_factor = 1.0 - (num_targets / max(1, num_detections))
        
        # Humanos presentes = mais perigoso
        human_factor = min(1.0, num_humans * 0.3)
        
        # Baixa confiança = mais incerto
        confidence_factor = 1.0 - avg_confidence
        
        # Combina fatores
        difficulty = (
            0.25 * detection_factor +
            0.3 * target_factor +
            0.25 * human_factor +
            0.2 * confidence_factor
        )
        
        return min(1.0, max(0.0, difficulty))
    
    def get_learning_summary(self) -> Dict:
        """Retorna resumo do aprendizado da IA"""
        return {
            "global_metrics": self.global_metrics,
            "class_patterns": {
                k: {
                    "hits": v.get("hit_count", 0),
                    "misses": v.get("miss_count", 0),
                    "avg_confidence": v.get("avg_confidence_when_hit", 0)
                }
                for k, v in self.class_patterns.items()
            },
            "confidence_adjustments": self.confidence_adjustments,
            "total_images_analyzed": len(self.click_history)
        }
    
    def reset_learning(self):
        """Reseta todo o aprendizado"""
        self.click_history.clear()
        self.class_patterns.clear()
        self.confidence_adjustments.clear()
        self.human_performance.clear()
        self.global_metrics = {
            "total_rounds": 0,
            "human_correct": 0,
            "human_wrong": 0,
            "ai_correct": 0,
            "ai_wrong": 0,
            "avg_reaction_time": 0.0
        }


# Instância global
ai_learning_service = AILearningService()

