"""
Rotas da API REST
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional, Dict, Set
from pathlib import Path
import base64
import random

from ..models.schemas import (
    ImageAnalysisRequest, ImageAnalysisResponse,
    GameSession, GameRound, GameResult,
    ClickEvent, ClickResult, Detection,
    LeaderboardEntry
)
from ..services.detection_service import detection_service
from ..services.game_service import game_service
from ..services.ai_learning_service import ai_learning_service
from ..config import settings
from ..constants import BOAR_IMAGE_PROBABILITY, BOAR_CLASS_INDICES

router = APIRouter()


# ===========================================
# Cache de Índice de Imagens por Categoria
# ===========================================
# Armazena quais imagens contêm javalis vs outras
_image_index_cache: Dict[str, Dict[str, List[Path]]] = {}


def _get_labels_dir(images_dir: Path) -> Path:
    """Retorna o diretório de labels correspondente ao diretório de imagens."""
    return images_dir.parent / "labels"


def _image_has_boar(image_path: Path, labels_dir: Path) -> bool:
    """
    Verifica se uma imagem contém javali baseado no arquivo de label YOLO.
    
    O formato YOLO segmentação é: class_id x1 y1 x2 y2 ... (polígono)
    Verificamos se alguma linha começa com classe 0 ou 1 (boar/wild-boar).
    """
    # Nome do label é o mesmo da imagem, mas com .txt
    label_name = image_path.stem + ".txt"
    label_path = labels_dir / label_name
    
    if not label_path.exists():
        return False
    
    try:
        with open(label_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Primeiro número é a classe
                parts = line.split()
                if parts:
                    class_id = int(parts[0])
                    if class_id in BOAR_CLASS_INDICES:
                        return True
    except Exception:
        return False
    
    return False


def _build_image_index(split: str) -> Dict[str, List[Path]]:
    """
    Constrói índice de imagens separando por categoria (com_javali vs outras).
    
    Retorna dict com:
    - 'boar': lista de imagens que contêm javali
    - 'other': lista de imagens sem javali
    """
    split_dirs = {
        "test": settings.GAME_IMAGES_DIR,
        "valid": settings.VALID_IMAGES_DIR,
        "train": settings.TRAIN_IMAGES_DIR,
    }
    
    images_dir = split_dirs.get(split, settings.GAME_IMAGES_DIR)
    labels_dir = _get_labels_dir(images_dir)
    
    extensions = ['.jpg', '.jpeg', '.png', '.webp']
    images = [p for p in images_dir.iterdir() if p.suffix.lower() in extensions]
    
    boar_images = []
    other_images = []
    
    for image_path in images:
        if _image_has_boar(image_path, labels_dir):
            boar_images.append(image_path)
        else:
            other_images.append(image_path)
    
    return {
        'boar': boar_images,
        'other': other_images
    }


def _get_image_index(split: str) -> Dict[str, List[Path]]:
    """Retorna índice de imagens, construindo se necessário (lazy loading)."""
    if split not in _image_index_cache:
        _image_index_cache[split] = _build_image_index(split)
    return _image_index_cache[split]


def _select_random_image_with_bias(split: str) -> Path:
    """
    Seleciona uma imagem aleatória com viés para mostrar mais javalis.
    
    Usa BOAR_IMAGE_PROBABILITY para determinar a chance de mostrar 
    uma imagem com javali vs uma imagem com outros animais.
    """
    index = _get_image_index(split)
    
    boar_images = index.get('boar', [])
    other_images = index.get('other', [])
    
    # Se não há imagens de alguma categoria, retorna da outra
    if not boar_images and not other_images:
        raise HTTPException(status_code=404, detail="Nenhuma imagem encontrada")
    
    if not boar_images:
        return random.choice(other_images)
    
    if not other_images:
        return random.choice(boar_images)
    
    # Decide baseado na probabilidade configurada
    if random.random() < BOAR_IMAGE_PROBABILITY:
        return random.choice(boar_images)
    else:
        return random.choice(other_images)


# ============== Rotas de Detecção ==============

@router.post("/detect", response_model=ImageAnalysisResponse)
async def detect_animals(request: ImageAnalysisRequest):
    """
    Analisa uma imagem e retorna detecções de animais
    
    - Detecta javalis (alvo principal)
    - Detecta outros animais (penalidade)
    - Detecta humanos (penalidade severa)
    """
    try:
        result = detection_service.analyze_image(request.image_base64, return_masks=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na detecção: {str(e)}")


@router.post("/detect/upload", response_model=ImageAnalysisResponse)
async def detect_from_upload(file: UploadFile = File(...)):
    """Analisa uma imagem enviada como arquivo"""
    try:
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode()
        result = detection_service.analyze_image(image_base64, return_masks=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na detecção: {str(e)}")


# ============== Rotas do Jogo ==============

@router.post("/game/start", response_model=GameSession)
async def start_game(player_name: Optional[str] = None):
    """Inicia uma nova sessão de jogo"""
    try:
        session = game_service.create_session(player_name)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar jogo: {str(e)}")


@router.get("/game/{session_id}", response_model=GameSession)
async def get_game_session(session_id: str):
    """Obtém informações de uma sessão de jogo"""
    session = game_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return session


@router.post("/game/{session_id}/round/start")
async def start_round(session_id: str, request: ImageAnalysisRequest):
    """
    Inicia uma nova rodada com uma imagem
    
    Retorna as detecções para o frontend poder mostrar os alvos
    """
    try:
        game_round, detections = game_service.start_round(
            session_id, 
            request.image_base64
        )
        return {
            "round": game_round.model_dump(),
            "detections": [d.model_dump() for d in detections],
            "difficulty": ai_learning_service.calculate_difficulty(detections)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar rodada: {str(e)}")


@router.post("/game/{session_id}/click", response_model=ClickResult)
async def process_click(session_id: str, click: ClickEvent):
    """
    Processa um clique do jogador
    
    - Verifica se acertou algum animal
    - Calcula pontos ou penalidades
    - Registra para aprendizado da IA
    """
    try:
        # Processa o clique
        result = game_service.process_player_click(session_id, click)
        
        # Obtém detecções para aprendizado
        detections = game_service.detection_cache.get(click.image_id, [])
        
        # Encontra detecção acertada (se houver)
        hit, detection = detection_service.check_click_hit(
            click.x, click.y, detections
        )
        
        # Registra para aprendizado
        ai_learning_service.record_human_click(
            session_id, click, hit, detection, detections
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar clique: {str(e)}")


@router.post("/game/{session_id}/ai-turn")
async def ai_turn(session_id: str, image_id: str):
    """
    Executa a vez da IA para uma imagem
    
    A IA analisa as detecções e "clica" baseada em seu aprendizado
    """
    try:
        detections = game_service.detection_cache.get(image_id, [])
        
        # Obtém recomendações baseadas no aprendizado
        recommendations = ai_learning_service.get_ai_recommendations(detections)
        
        # Simula cliques da IA
        results = await game_service.simulate_ai_turn(session_id, detections)
        
        return {
            "results": [r.model_dump() for r in results],
            "recommendations_used": len([r for r in recommendations if r["should_click"]])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na vez da IA: {str(e)}")


@router.post("/game/{session_id}/round/end", response_model=GameRound)
async def end_round(session_id: str):
    """Finaliza a rodada atual"""
    try:
        game_round = game_service.end_round(session_id)
        
        # Atualiza aprendizado da IA
        session = game_service.get_session(session_id)
        if session and session.current_round:
            player_score = session.current_round.player_score
            ai_score = session.current_round.ai_score
            
            player_total = player_score.correct_hits + player_score.wrong_hits
            ai_total = ai_score.correct_hits + ai_score.wrong_hits
            
            player_acc = (player_score.correct_hits / player_total * 100) if player_total > 0 else 0
            ai_acc = (ai_score.correct_hits / ai_total * 100) if ai_total > 0 else 0
            
            ai_learning_service.update_ai_confidence(session_id, player_acc, ai_acc)
        
        return game_round
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao finalizar rodada: {str(e)}")


@router.post("/game/{session_id}/end", response_model=GameResult)
async def end_game(session_id: str):
    """Finaliza o jogo e retorna resultado"""
    try:
        result = game_service.end_game(session_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao finalizar jogo: {str(e)}")


# ============== Rotas de Aprendizado ==============

@router.get("/learning/summary")
async def get_learning_summary():
    """Retorna resumo do aprendizado da IA"""
    return ai_learning_service.get_learning_summary()


@router.post("/learning/reset")
async def reset_learning():
    """Reseta o aprendizado da IA"""
    ai_learning_service.reset_learning()
    return {"message": "Aprendizado resetado com sucesso"}


# ============== Rotas de Leaderboard ==============

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 10):
    """Retorna o placar de líderes"""
    # Por enquanto retorna dados de exemplo
    # Em produção, buscar do banco de dados
    return [
        LeaderboardEntry(
            rank=i+1,
            player_name=f"Jogador{i+1}",
            score=1000 - i*100,
            accuracy=95 - i*5,
            games_played=10 - i,
            best_streak=5 - i//2
        )
        for i in range(min(limit, 10))
    ]


# ============== Rotas de Health Check ==============

@router.get("/health")
async def health_check():
    """Verifica saúde do serviço"""
    return {
        "status": "healthy",
        "model_loaded": detection_service.model is not None,
        "segmentation_enabled": detection_service.use_segmentation,
        "active_sessions": len(game_service.active_sessions),
        "images_available": len(game_service.sample_images)
    }


# ============== Rotas de Imagens (Dataset Agriculture) ==============

@router.get("/images/stats")
async def get_image_stats(split: str = "test"):
    """
    Retorna estatísticas das imagens por categoria (javali vs outras).
    
    Útil para verificar a distribuição das imagens no dataset.
    """
    index = _get_image_index(split)
    
    boar_count = len(index.get('boar', []))
    other_count = len(index.get('other', []))
    total = boar_count + other_count
    
    return {
        "split": split,
        "total_images": total,
        "boar_images": boar_count,
        "other_images": other_count,
        "boar_percentage": round(boar_count / total * 100, 1) if total > 0 else 0,
        "configured_bias": round(BOAR_IMAGE_PROBABILITY * 100, 1)
    }


@router.get("/images/list")
async def list_game_images(split: str = "test", limit: int = 50):
    """
    Lista imagens disponíveis do dataset Agriculture
    
    Args:
        split: 'test', 'valid' ou 'train'
        limit: número máximo de imagens
    """
    split_dirs = {
        "test": settings.GAME_IMAGES_DIR,
        "valid": settings.VALID_IMAGES_DIR,
        "train": settings.TRAIN_IMAGES_DIR,
    }
    
    images_dir = split_dirs.get(split, settings.GAME_IMAGES_DIR)
    
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail=f"Diretório {split} não encontrado")
    
    extensions = ['.jpg', '.jpeg', '.png', '.webp']
    images = [
        p.name for p in images_dir.iterdir()
        if p.suffix.lower() in extensions
    ][:limit]
    
    return {
        "split": split,
        "count": len(images),
        "images": images
    }


@router.get("/images/random")
async def get_random_image(split: str = "test", use_bias: bool = True):
    """
    Retorna uma imagem aleatória do dataset Agriculture
    
    Args:
        split: 'test', 'valid' ou 'train'
        use_bias: Se True, usa viés para mostrar mais imagens com javali
                  (padrão: True, ~70% javalis)
    """
    try:
        if use_bias:
            # Usa seleção com viés para javalis
            image_path = _select_random_image_with_bias(split)
        else:
            # Seleção puramente aleatória
            split_dirs = {
                "test": settings.GAME_IMAGES_DIR,
                "valid": settings.VALID_IMAGES_DIR,
                "train": settings.TRAIN_IMAGES_DIR,
            }
            
            images_dir = split_dirs.get(split, settings.GAME_IMAGES_DIR)
            
            if not images_dir.exists():
                raise HTTPException(status_code=404, detail=f"Diretório {split} não encontrado")
            
            extensions = ['.jpg', '.jpeg', '.png', '.webp']
            images = [p for p in images_dir.iterdir() if p.suffix.lower() in extensions]
            
            if not images:
                raise HTTPException(status_code=404, detail="Nenhuma imagem encontrada")
            
            image_path = random.choice(images)
        
        # Lê e converte para base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        return {
            "filename": image_path.name,
            "split": split,
            "image_base64": image_base64
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter imagem: {str(e)}")


@router.get("/images/file/{split}/{filename}")
async def get_image_file(split: str, filename: str):
    """
    Serve um arquivo de imagem diretamente
    
    Args:
        split: 'test', 'valid' ou 'train'
        filename: nome do arquivo
    """
    split_dirs = {
        "test": settings.GAME_IMAGES_DIR,
        "valid": settings.VALID_IMAGES_DIR,
        "train": settings.TRAIN_IMAGES_DIR,
    }
    
    images_dir = split_dirs.get(split, settings.GAME_IMAGES_DIR)
    image_path = images_dir / filename
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
    return FileResponse(image_path)


@router.get("/images/random/analyzed")
async def get_random_analyzed_image(split: str = "test"):
    """
    Retorna uma imagem aleatória já analisada pelo modelo
    
    Útil para o jogo: retorna imagem + detecções de uma vez
    """
    # Obtém imagem aleatória
    image_data = await get_random_image(split)
    
    # Analisa com o modelo
    analysis = detection_service.analyze_image(image_data["image_base64"], return_masks=True)
    
    return {
        "filename": image_data["filename"],
        "split": split,
        "image_base64": image_data["image_base64"],
        "analysis": analysis.model_dump()
    }

