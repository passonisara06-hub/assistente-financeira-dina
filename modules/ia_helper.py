"""
Módulo de integração com IA (DeepSeek)
Responsável por gerar respostas seguras e personalizadas
"""

import os
from openai import OpenAI
from typing import List, Dict


def inicializar_cliente() -> OpenAI:
    """
    Inicializa o cliente DeepSeek com a API key do ambiente.

    Returns:
        Instância do cliente OpenAI configurado para DeepSeek ou None se não configurado
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key or api_key == "sk-sua-chave-aqui":
        return None

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )


def gerar_resposta_segura(
    pergunta: str,
    contexto_usuario: dict,
    historico_conversa: List[Dict] = None
) -> str:
    """
    Gera uma resposta segura usando IA DeepSeek, com restrições de segurança financeira.

    Args:
        pergunta: Pergunta do usuário
        contexto_usuario: Dict com dados do contexto (renda, gastos, etc)
        historico_conversa: Lista de mensagens anteriores (opcional)

    Returns:
        String com a resposta gerada
    """
    client = inicializar_cliente()

    if not client:
        return """
⚠️ **Chat com IA não configurado**

Para usar esta funcionalidade, você precisa configurar sua API Key da DeepSeek:

1. Copie o arquivo `.env.example` para `.env`
2. Adicione sua chave: `DEEPSEEK_API_KEY=sk-sua-chave-aqui`
3. Obtenha sua chave em: https://platform.deepseek.com/
4. Reinicie a aplicação

Enquanto isso, use a aba **FAQ Inteligente** para tirar dúvidas!
        """

    # Formata contexto do usuário
    contexto_str = ""
    if contexto_usuario.get("renda_mensal"):
        contexto_str += f"Renda mensal: R$ {contexto_usuario['renda_mensal']:,.2f}. "

    if contexto_usuario.get("gastos_fixos"):
        contexto_str += f"Gastos fixos: R$ {contexto_usuario['gastos_fixos']:,.2f}. "

    if contexto_usuario.get("gastos_variaveis"):
        contexto_str += f"Gastos variáveis: R$ {contexto_usuario['gastos_variaveis']:,.2f}. "

    if contexto_usuario.get("objetivo"):
        contexto_str += f"Objetivo: {contexto_usuario['objetivo']}."

    # Histórico de conversa
    messages = []

    if historico_conversa:
        # Adiciona últimas 5 mensagens do histórico
        for msg in historico_conversa[-5:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Prompt do sistema
    system_prompt = f"""
Você é um **Coach Financeiro Digital** especializado em educação financeira.

SEU PAPEL:
- Ajudar usuários a entender conceitos financeiros
- Oferecer simulações educativas
- Explicar de forma didática e acessível
- Usar linguagem simples e exemplos do cotidiano

CONTEXTO DO USUÁRIO:
{contexto_str if contexto_str else "Usuário ainda não compartilhou informações financeiras."}

REGRAS DE SEGURANÇA (OBRIGATÓRIO):
1. **NUNCA** recomendar investimentos específicos (ex: "compre ação X", "invista em CDB do banco Y")
2. **NUNCA** prometer retornos garantidos
3. **NUNCA** dar aconselhamento financeiro personalizado sem conhecer o perfil completo
4. **SEMPRE** incluir aviso: "ℹ️ *Isso é apenas educativo, não uma recomendação financeira personalizada.*"

TOM E ESTILO:
- Educativo, simpático e acessível
- Explicar termos técnicos (ex: "juros sobre juros como uma bola de neve")
- Usar formatação markdown para facilitar leitura
- Máximo 3-4 parágrafos por resposta

Se a pergunta for sobre recomendação de investimento, responda que seu papel é educativo
e sugira consultar um profissional ou aprender mais sobre os conceitos.
"""

    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": pergunta})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Erro ao gerar resposta: {str(e)}"


def personalizar_resposta(
    resposta_base: str,
    contexto_usuario: dict,
    tonalidade: str = "simpatico"
) -> str:
    """
    Personaliza uma resposta base com dados do contexto do usuário.

    Args:
        resposta_base: Resposta base a ser personalizada
        contexto_usuario: Dict com dados do contexto
        tonalidade: Tipo de tom ("simpatico", "formal", "motivacional")

    Returns:
        String personalizada
    """
    client = inicializar_cliente()

    if not client:
        return resposta_base

    # Formata contexto
    contexto_str = ""
    if contexto_usuario.get("renda_mensal"):
        contexto_str += f"Considerando sua renda de R$ {contexto_usuario['renda_mensal']:,.2f}, "
    if contexto_usuario.get("objetivo"):
        contexto_str += f"e seu objetivo de {contexto_usuario['objetivo']}, "

    prompt = f"""
Personalize a resposta abaixo para um usuário com o seguinte contexto: {contexto_str}

Resposta base: {resposta_base}

Use tom {tonalidade} e mantenha o conteúdo educativo.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        return resposta_base


def reformular_explicacao(
    explicacao: str,
    nivel_complexidade: str = "simples"
) -> str:
    """
    Reformula uma explicação para um nível diferente de complexidade.

    Args:
        explicacao: Explicação original
        nivel_complexidade: "simples", "medio", "detalhado"

    Returns:
        Explicação reformulada
    """
    client = inicializar_cliente()

    if not client:
        return explicacao

    prompt = f"""
Reformule a explicação abaixo para um nível de complexidade {nivel_complexidade}:

{explicacao}

Mantenha o conteúdo preciso mas ajuste a linguagem e o nível de detalhe.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        return explicacao


def responder_pergunta_chat(
    pergunta: str,
    contexto_usuario: dict,
    historico_conversa: List[Dict] = None
) -> str:
    """
    Função otimizada para chat com contexto e histórico.

    Args:
        pergunta: Pergunta do usuário
        contexto_usuario: Dict com contexto do usuário
        historico_conversa: Lista de mensagens anteriores

    Returns:
        String com resposta personalizada
    """
    client = inicializar_cliente()

    if not client:
        return """
⚠️ **IA não configurada**

Configure sua API Key da DeepSeek no arquivo `.env` para usar o chat.

Obtenha sua chave em: https://platform.deepseek.com/
        """

    # Formata contexto completo
    contexto_str = formatar_contexto_para_chat(contexto_usuario)

    # Constrói messages
    messages = []

    # Adiciona histórico (últimas 5 trocas)
    if historico_conversa:
        for msg in historico_conversa[-5:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # System prompt
    system_prompt = f"""
Você é a **Nat**, uma assistente de finanças especializada em educação financeira.

🎭 **PERSONA:**
- Nome: Nat
- Tom: Amigável, didático, seguro e acessível
- Especialidade: Educação financeira personalizada
- Abordagem: Prática e contextualizada

📊 **CONTEXTO DO USUÁRIO:**
{contexto_str}

🎯 **DIRETRIZES:**
- Sempre se apresente como "Nat" quando apropriado
- Responda de forma educativa, jamais recomende investimentos específicos
- Use o contexto do usuário (renda, gastos, idade) para personalizar respostas
- Linguagem simples e acessível
- Máximo 3-4 parágrafos por resposta
- Use emojis moderadamente para tornar a conversa mais amigável

⚠️ **OBRIGATÓRIO:** Sempre finalize com: "ℹ️ *Isso é apenas educativo, não recomendação financeira.*"

💡 **EXEMPLO DE ABORDAGEM:**
"Com sua renda de R$ X e sobra de R$ Y, você poderia..."
"Considerando sua idade de Z anos, é um ótimo momento para..."
"""

    messages.insert(0, {"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": pergunta})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Erro: {str(e)}"


def formatar_contexto_para_chat(contexto_usuario: dict) -> str:
    """
    Formata o contexto do usuário para exibição no chat.

    Args:
        contexto_usuario: Dict com dados do contexto

    Returns:
        String formatada com o contexto
    """
    partes = []

    if contexto_usuario.get("renda_mensal"):
        partes.append(f"💰 Renda: R$ {contexto_usuario['renda_mensal']:,.2f}")

    if contexto_usuario.get("gastos_fixos"):
        partes.append(f"📉 Gastos Fixos: R$ {contexto_usuario['gastos_fixos']:,.2f}")

    if contexto_usuario.get("gastos_variaveis"):
        partes.append(f"🛒 Gastos Variáveis: R$ {contexto_usuario['gastos_variaveis']:,.2f}")

    if contexto_usuario.get("sobra_mensal"):
        partes.append(f"✅ Sobra Mensal: R$ {contexto_usuario['sobra_mensal']:,.2f}")

    if contexto_usuario.get("objetivo"):
        partes.append(f"🎯 Objetivo: {contexto_usuario['objetivo']}")

    if not partes:
        return "Perfil ainda não preenchido"

    return "\n".join(partes)
