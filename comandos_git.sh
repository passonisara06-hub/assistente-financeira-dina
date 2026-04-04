#!/bin/bash
# 🚀 Comandos para postar Nat no GitHub
# Execute este script ou copie os comandos um por um

echo "=== 🧡 Nat - Assistente de Finanças ==="
echo "Preparando para postar no GitHub..."
echo ""

# 1. Inicializar repositório (se ainda não feito)
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    echo "✅ Git inicializado!"
else
    echo "✅ Git já inicializado"
fi

echo ""

# 2. Verificar arquivos que serão commitados
echo "📋 Arquivos que serão commitados:"
git status --short
echo ""

# 3. Adicionar arquivos
echo "➕ Adicionando arquivos..."
git add .
echo "✅ Arquivos adicionados!"
echo ""

# 4. Commit
echo "💾 Criando commit..."
git commit -m "🎉 Initial commit: Nat - Assistente de Finanças

- 🧡 Personalidade única: Nat, assistente de finanças
- 📊 Perfil financeiro com cálculo de sobra
- 📚 Simuladores: Reserva, Juros Compostos, Aposentadoria
- 💬 Chat com IA (DeepSeek)
- ❓ FAQ inteligente com 10+ tópicos
- 🔵 Cores acessíveis para daltônicos
- 🎂 Campo de idade para planejamento de LP

Powered by Streamlit + DeepSeek"

echo "✅ Commit criado!"
echo ""

# 5. Instruções para o usuário
echo "==================================="
echo "📝 PRÓXIMOS PASSOS:"
echo "==================================="
echo ""
echo "1. Crie um repositório no GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Nome do repositório: nat-assistente-financeiro"
echo ""
echo "3. Execute os seguintes comandos (substitua SEU_USUARIO):"
echo ""
echo "   git remote add origin https://github.com/SEU_USUARIO/nat-assistente-financeiro.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "==================================="
echo ""
echo "🧡 Boa sorte com a Nat!"
