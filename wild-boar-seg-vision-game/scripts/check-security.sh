#!/bin/bash

# ===========================================
# Script de Verificação de Segurança
# ===========================================

echo "🔒 Verificando segurança do projeto..."
echo ""

ERRORS=0
WARNINGS=0

# Cores
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Verifica se .env está no gitignore
echo "📋 Verificando .gitignore..."
if grep -q "^\.env$" .gitignore; then
    echo -e "${GREEN}✅ .env está no .gitignore${NC}"
else
    echo -e "${RED}❌ .env NÃO está no .gitignore!${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Verifica se há arquivos .env commitados
echo ""
echo "🔍 Verificando arquivos .env no repositório..."
if git ls-files | grep -q "\.env$"; then
    echo -e "${RED}❌ Arquivos .env encontrados no repositório!${NC}"
    git ls-files | grep "\.env$"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ Nenhum arquivo .env commitado${NC}"
fi

# Verifica se .env.example existe
echo ""
echo "📄 Verificando arquivos .env.example..."
if [ -f "backend/.env.example" ]; then
    echo -e "${GREEN}✅ backend/.env.example existe${NC}"
else
    echo -e "${YELLOW}⚠️ backend/.env.example não encontrado${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -f "frontend/.env.example" ]; then
    echo -e "${GREEN}✅ frontend/.env.example existe${NC}"
else
    echo -e "${YELLOW}⚠️ frontend/.env.example não encontrado${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Verifica se há chaves hardcoded no código (apenas arquivos fonte)
echo ""
echo "🔑 Verificando chaves hardcoded no código..."
SENSITIVE_PATTERNS=(
    "ROBOFLOW_API_KEY.*=.*['\"][^'\"]+['\"]"
    "SECRET_KEY.*=.*['\"][^'\"]+['\"]"
    "api[_-]?key.*=.*['\"][^'\"]+['\"]"
    "password.*=.*['\"][^'\"]+['\"]"
    "token.*=.*['\"][^'\"]+['\"]"
)

FOUND_HARDCODED=false
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    # Busca apenas em arquivos fonte (não compilados)
    results=$(grep -r -E "$pattern" \
        --include="*.py" \
        --include="*.ts" \
        --include="*.tsx" \
        --include="*.js" \
        --include="*.jsx" \
        --exclude-dir=node_modules \
        --exclude-dir=venv \
        --exclude-dir=.git \
        --exclude-dir=.next \
        --exclude-dir=dist \
        --exclude-dir=build \
        --exclude="*.example" \
        --exclude="*.min.js" \
        . 2>/dev/null | \
        grep -v "\.env.example" | \
        grep -v "SECURITY.md" | \
        grep -v "check-security.sh" | \
        grep -v "download_datasets.py" | \
        grep -v "maintain--tab-focus.js" | \
        grep -v "change-this-in-production" | \
        grep -v "your-secret-key-here" | \
        grep -v "localhost" || true)
    
    if [ -n "$results" ]; then
        echo -e "${RED}❌ Possível chave hardcoded encontrada:${NC}"
        echo "$results"
        FOUND_HARDCODED=true
        ERRORS=$((ERRORS + 1))
    fi
done

if [ "$FOUND_HARDCODED" = false ]; then
    echo -e "${GREEN}✅ Nenhuma chave hardcoded encontrada${NC}"
fi

# Verifica se há arquivos .env locais
echo ""
echo "📁 Verificando arquivos .env locais..."
if [ -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️ backend/.env existe localmente (isso é normal)${NC}"
    # Verifica se tem chaves vazias ou padrão
    if grep -q "change-this-in-production" backend/.env 2>/dev/null; then
        echo -e "${YELLOW}⚠️ SECRET_KEY ainda está com valor padrão!${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️ backend/.env não existe (crie a partir de .env.example)${NC}"
fi

if [ -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}⚠️ frontend/.env.local existe localmente (isso é normal)${NC}"
else
    echo -e "${YELLOW}⚠️ frontend/.env.local não existe (crie a partir de .env.example)${NC}"
fi

# Resumo
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Verificação concluída sem problemas!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️ Verificação concluída com $WARNINGS aviso(s)${NC}"
    exit 0
else
    echo -e "${RED}❌ Verificação falhou com $ERRORS erro(s) e $WARNINGS aviso(s)${NC}"
    echo ""
    echo "Corrija os erros antes de fazer commit!"
    exit 1
fi

