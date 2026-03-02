"""
Serviço de Detecção e SEGMENTAÇÃO de Javalis usando YOLOv8-seg

Este serviço usa o modelo treinado no dataset Agriculture (HTW) para
detectar e segmentar javalis, macacos, cachorros e pessoas.
"""
import io
import base64
import time
import uuid
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import numpy as np
from PIL import Image, ImageDraw

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

from ..models.schemas import Detection, BoundingBox, AnimalClass, ImageAnalysisResponse, SegmentationPoint
from ..config import settings
from .. import constants


class DetectionService:
    """Serviço para detecção e SEGMENTAÇÃO usando modelo Agriculture (HTW)"""
    
    # Classes do modelo Agriculture (HTW) mapeadas para AnimalClass
    CUSTOM_CLASSES = {
        0: AnimalClass.BOAR,    # boar - Javali (ALVO)
        1: AnimalClass.BOAR,    # wild-boar - Javali selvagem (ALVO)
        2: AnimalClass.OTHER,   # dog - Cachorro (distrator)
        3: AnimalClass.OTHER,   # monkey - Macaco (distrator)
        4: AnimalClass.HUMAN,   # person - Humano (PENALIDADE)
    }
    
    # Nomes das classes para logging
    CLASS_NAMES = constants.MODEL_CLASSES
    
    def __init__(self):
        """Inicializa o serviço de detecção/segmentação"""
        self.model = None
        self.segmentation_model = None
        self.use_segmentation = constants.SEGMENTATION_ENABLED
        self._load_models()
        
        # Confidence adjustments baseados em aprendizado
        self.confidence_adjustments = {}
        
    def _load_models(self):
        """Carrega o modelo de segmentação Agriculture"""
        if not YOLO_AVAILABLE:
            print("⚠️ YOLO não disponível. Instale: pip install ultralytics")
            return
            
        try:
            # Carrega modelo de SEGMENTAÇÃO treinado no Agriculture dataset
            seg_model_path = settings.ML_MODELS_DIR / "javali_seg.pt"
            if seg_model_path.exists():
                self.segmentation_model = YOLO(str(seg_model_path))
                self.use_segmentation = True
                print(f"✅ Modelo Agriculture carregado: javali_seg.pt")
                print(f"   Classes: {list(constants.MODEL_CLASSES.values())}")
            else:
                print(f"❌ Modelo javali_seg.pt não encontrado em: {seg_model_path}")
                print("   Execute o treinamento com: python ml/training/train_segmentation.py")
                
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            self.segmentation_model = None
    
    def decode_image(self, image_base64: str) -> Image.Image:
        """Decodifica imagem de base64 para PIL Image"""
        # Remove header se presente
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
            
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        return image.convert("RGB")
    
    def encode_image(self, image: Image.Image) -> str:
        """Codifica PIL Image para base64"""
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()
    
    def analyze_image(
        self, 
        image_base64: str,
        confidence_threshold: Optional[float] = None,
        return_masks: bool = False
    ) -> ImageAnalysisResponse:
        """
        Analisa uma imagem e retorna detecções/segmentações
        
        Args:
            image_base64: Imagem codificada em base64
            confidence_threshold: Limiar de confiança (opcional)
            return_masks: Se True, inclui máscaras de segmentação nos resultados
            
        Returns:
            ImageAnalysisResponse com as detecções encontradas
        """
        start_time = time.time()
        image_id = str(uuid.uuid4())[:8]
        
        threshold = confidence_threshold or settings.MODEL_CONFIDENCE_THRESHOLD
        
        # Decodifica imagem
        image = self.decode_image(image_base64)
        img_width, img_height = image.size
        
        detections = []
        
        # Usa apenas modelo de segmentação Agriculture
        if self.use_segmentation and self.segmentation_model is not None:
            detections = self._analyze_with_segmentation(
                image, img_width, img_height, threshold, return_masks
            )
        else:
            # Modelo não disponível - retorna vazio
            print("⚠️ Modelo de segmentação não carregado. Nenhuma detecção disponível.")
        
        processing_time = (time.time() - start_time) * 1000
        
        # Conta javalis
        boar_count = sum(1 for d in detections if d.is_target)
        
        return ImageAnalysisResponse(
            image_id=image_id,
            detections=detections,
            processing_time_ms=processing_time,
            has_boar=boar_count > 0,
            boar_count=boar_count
        )
    
    def _analyze_with_segmentation(
        self, 
        image: Image.Image, 
        img_width: int, 
        img_height: int, 
        threshold: float,
        return_masks: bool = False
    ) -> List[Detection]:
        """
        Analisa imagem usando SEGMENTAÇÃO (máscaras de instância)
        
        A segmentação fornece contornos precisos dos animais, não apenas
        bounding boxes. Isso permite uma identificação mais precisa.
        """
        detections = []
        
        # Executa segmentação
        results = self.segmentation_model(image, verbose=False)
        
        for result in results:
            boxes = result.boxes
            masks = result.masks
            
            if boxes is not None:
                for i, box in enumerate(boxes):
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Usa nome da classe do modelo
                    cls_name = result.names[cls_id]
                    
                    # Para modelo customizado, mapeia diretamente
                    if cls_id in self.CUSTOM_CLASSES:
                        animal_class = self.CUSTOM_CLASSES[cls_id]
                    else:
                        animal_class = self._map_class(cls_name)
                    
                    # Aplica ajustes de confiança
                    adjusted_conf = self._apply_confidence_adjustment(cls_name, conf)
                    
                    if adjusted_conf >= threshold:
                        # Converte coordenadas
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # Normaliza para 0-1
                        bbox = BoundingBox(
                            x=(x1 + x2) / 2 / img_width,
                            y=(y1 + y2) / 2 / img_height,
                            width=(x2 - x1) / img_width,
                            height=(y2 - y1) / img_height
                        )
                        
                        # Verifica se é javali
                        is_target = animal_class == AnimalClass.BOAR
                        
                        # Extrai máscara de segmentação se disponível
                        mask_polygon = None
                        if return_masks and masks is not None and i < len(masks):
                            mask = masks[i]
                            if mask.xy is not None and len(mask.xy) > 0:
                                # Normaliza pontos do polígono para SegmentationPoint
                                mask_polygon = [
                                    SegmentationPoint(
                                        x=float(p[0]) / img_width, 
                                        y=float(p[1]) / img_height
                                    )
                                    for p in mask.xy[0]
                                ]
                        
                        detection = Detection(
                            class_name=animal_class,
                            confidence=adjusted_conf,
                            bbox=bbox,
                            is_target=is_target,
                            segmentation=mask_polygon  # Contorno da segmentação
                        )
                        detections.append(detection)
        
        return detections

    def _apply_confidence_adjustment(self, cls_name: str, confidence: float) -> float:
        """Aplica ajustes de confiança baseados no aprendizado"""
        adjustment = self.confidence_adjustments.get(cls_name, 0.0)
        return max(0.0, min(1.0, confidence + adjustment))
    
    def update_confidence_adjustment(self, cls_name: str, adjustment: float):
        """Atualiza ajuste de confiança para uma classe"""
        current = self.confidence_adjustments.get(cls_name, 0.0)
        self.confidence_adjustments[cls_name] = current + adjustment
    
    def check_click_hit(
        self, 
        click_x: float, 
        click_y: float, 
        detections: List[Detection],
        tolerance: float = 0.05
    ) -> Tuple[bool, Optional[Detection]]:
        """
        Verifica se um clique acertou alguma detecção
        
        Args:
            click_x: Posição X do clique (0-1)
            click_y: Posição Y do clique (0-1)
            detections: Lista de detecções na imagem
            tolerance: Tolerância para considerar um acerto
            
        Returns:
            Tupla (acertou, detecção_acertada)
        """
        for detection in detections:
            bbox = detection.bbox
            
            # Calcula limites da caixa com tolerância
            left = bbox.x - bbox.width/2 - tolerance
            right = bbox.x + bbox.width/2 + tolerance
            top = bbox.y - bbox.height/2 - tolerance
            bottom = bbox.y + bbox.height/2 + tolerance
            
            # Verifica se clique está dentro
            if left <= click_x <= right and top <= click_y <= bottom:
                return True, detection
        
        return False, None


# Instância global do serviço
detection_service = DetectionService()

