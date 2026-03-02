# 🔒 Segurança - Javali Hunter

Este documento descreve as práticas de segurança implementadas no projeto.

## 📋 Variáveis de Ambiente

**NUNCA** commite arquivos `.env` com chaves reais no repositório!

### Configuração Inicial

1. **Backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Edite .env e adicione suas chaves
   ```

2. **Frontend:**
   ```bash
   cd frontend
   cp .env.example .env.local
   # Edite .env.local e adicione suas configurações
   ```

### Variáveis Sensíveis

#### Backend (`backend/.env`)

- `ROBOFLOW_API_KEY`: Chave da API do Roboflow (opcional)
- `SECRET_KEY`: Chave secreta para JWT/sessões (gere uma aleatória)
- `DATABASE_URL`: URL do banco de dados (pode conter credenciais)

#### Frontend (`frontend/.env.local`)

- `NEXT_PUBLIC_API_URL`: URL da API backend
- `NEXT_PUBLIC_UNSPLASH_ACCESS_KEY`: Chave do Unsplash (opcional)

⚠️ **ATENÇÃO**: Variáveis que começam com `NEXT_PUBLIC_` são expostas ao cliente!

## 🔑 Gerando Chaves Seguras

### Secret Key (Backend)

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32
```

### Roboflow API Key

1. Acesse https://roboflow.com
2. Crie uma conta gratuita
3. Vá em **Settings > API Key**
4. Copie a chave e adicione em `backend/.env`:
   ```
   ROBOFLOW_API_KEY=sua_chave_aqui
   ```

## 🛡️ Boas Práticas

### ✅ FAZER

- ✅ Usar `.env.example` como template
- ✅ Adicionar `.env` ao `.gitignore`
- ✅ Gerar chaves aleatórias para produção
- ✅ Rotacionar chaves periodicamente
- ✅ Usar variáveis de ambiente em produção
- ✅ Validar variáveis obrigatórias na inicialização

### ❌ NÃO FAZER

- ❌ Commitar arquivos `.env` com chaves reais
- ❌ Hardcodar chaves no código
- ❌ Compartilhar chaves por email/chat
- ❌ Usar a mesma chave em dev e produção
- ❌ Expor chaves em logs ou mensagens de erro

## 🔍 Verificação de Segurança

### Checklist antes de fazer commit:

```bash
# Verificar se não há .env no git
git status | grep .env

# Verificar se .env está no .gitignore
grep "^\.env$" .gitignore

# Verificar se há chaves hardcoded
grep -r "ROBOFLOW_API_KEY\|SECRET_KEY" --exclude-dir=node_modules --exclude-dir=venv .
```

## 🚨 Em caso de vazamento de chave

1. **Revogue a chave imediatamente** no serviço correspondente
2. **Gere uma nova chave**
3. **Atualize todos os ambientes** (dev, staging, produção)
4. **Revise logs** para detectar uso não autorizado
5. **Notifique a equipe** se necessário

## 📚 Recursos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [12 Factor App - Config](https://12factor.net/config)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

## 📞 Contato

Em caso de dúvidas sobre segurança, entre em contato com a equipe de desenvolvimento.

---

**Última atualização**: Dezembro 2024

