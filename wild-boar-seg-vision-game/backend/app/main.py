"""
Javali Hunter - Sistema de Detecção de Javalis
Aplicação Principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from .config import settings
from .api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    # Startup
    print(f"🐗 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Servidor iniciando em http://{settings.HOST}:{settings.PORT}")
    
    # Cria diretório de modelos se necessário
    settings.ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Verifica se dataset existe
    if settings.GAME_IMAGES_DIR.exists():
        test_count = len(list(settings.GAME_IMAGES_DIR.iterdir()))
        print(f"📦 Dataset Agriculture carregado: {test_count} imagens de teste")
    else:
        print(f"⚠️ Dataset não encontrado: {settings.GAME_IMAGES_DIR}")
    
    yield
    
    # Shutdown
    print("👋 Encerrando servidor...")


# Cria aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## Sistema de Detecção de Javalis via Visão Computacional
    
    Este sistema detecta javalis (Sus scrofa) e híbridos em imagens usando
    modelos de deep learning (YOLOv8).
    
    ### Funcionalidades:
    - 🎯 Detecção de javalis em imagens
    - 🎮 Jogo competitivo: Humano vs IA
    - 🧠 IA adaptativa que aprende com o jogador
    - 📊 Sistema de pontuação com penalidades
    
    ### Regras do Jogo:
    - ✅ Acertar javali: +100 pontos
    - ❌ Acertar outro animal: -30 pontos
    - ⚠️ Acertar humano: -200 pontos (penalidade severa)
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configuração CORS para permitir frontend
cors_origins = [
    origin.strip() 
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]
# Adiciona origens padrão se não especificadas
if not cors_origins:
    cors_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(router, prefix="/api/v1", tags=["API"])


@app.get("/")
async def root():
    """Rota raiz - informações da API"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

