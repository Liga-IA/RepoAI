#!/bin/bash

# ===========================================
# Script de Inicialização - Javali Hunter
# ===========================================

echo "🐗 Javali Hunter - Inicializando ambiente de desenvolvimento..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 não encontrado. Por favor, instale Python 3.10+${NC}"
    exit 1
fi

# Verificar Node.js
if ! command_exists node; then
    echo -e "${RED}❌ Node.js não encontrado. Por favor, instale Node.js 18+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python e Node.js encontrados${NC}"
echo ""

# ===== BACKEND =====
echo -e "${YELLOW}📦 Configurando Backend...${NC}"

cd "$BASE_DIR/backend"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências Python..."
pip install -r requirements.txt --quiet

# Criar diretórios necessários
mkdir -p ../ml/models ../ml/data/images

echo -e "${GREEN}✅ Backend configurado${NC}"
echo ""

# ===== FRONTEND =====
echo -e "${YELLOW}📦 Configurando Frontend...${NC}"

cd "$BASE_DIR/frontend"

# Instalar dependências npm
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências Node.js..."
    npm install --silent
fi

echo -e "${GREEN}✅ Frontend configurado${NC}"
echo ""

# ===== INICIAR SERVIÇOS =====
echo -e "${YELLOW}🚀 Iniciando serviços...${NC}"
echo ""

# Iniciar backend em background
cd "$BASE_DIR/backend"
source venv/bin/activate
echo "Iniciando Backend (porta 8000)..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Aguardar backend iniciar
sleep 3

# Iniciar frontend
cd "$BASE_DIR/frontend"
echo "Iniciando Frontend (porta 3000)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🐗 Javali Hunter está rodando!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "API Docs: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo -e "Pressione ${RED}Ctrl+C${NC} para encerrar todos os serviços"
echo ""

# Função para limpar ao sair
cleanup() {
    echo ""
    echo -e "${YELLOW}Encerrando serviços...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Serviços encerrados${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Manter script rodando
wait

