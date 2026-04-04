"""
Módulo de FAQ Inteligente
Responsável por buscar e responder perguntas frequentes sobre finanças
"""

import json
import os
from modules.ia_helper import inicializar_cliente


def carregar_base_conhecimento() -> list:
    """
    Carrega a base de conhecimento do arquivo JSON.

    Returns:
        Lista de dicts com perguntas e respostas
    """
    caminho_arquivo = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "conhecimento.json"
    )

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def buscar_resposta_base(pergunta_usuario: str) -> dict:
    """
    Busca uma resposta base na base de conhecimento usando palavras-chave.

    Args:
        pergunta_usuario: Pergunta feita pelo usuário

    Returns:
        Dict com a resposta encontrada ou dict vazio se não encontrar
    """
    base = carregar_base_conhecimento()

    if not base:
        return {}

    pergunta_lower = pergunta_usuario.lower()

    for item in base:
        # Busca por palavra-chave principal
        if item["pergunta"] in pergunta_lower:
            return item

        # Busca por palavras-chave secundárias
        for palavra in item.get("palavras_chave", []):
            if palavra in pergunta_lower:
                return item

    return {}


def enriquecer_resposta_com_ia(resposta_base: dict, contexto_usuario: dict = None) -> str:
    """
    Enriquece a resposta base usando IA para personalização e melhor didática.

    Args:
        resposta_base: Dict com resposta da base de conhecimento
        contexto_usuario: Dict opcional com contexto do usuário

    Returns:
        String com resposta enriquecida
    """
    client = inicializar_cliente()

    if not client:
        # Se não tem IA, retorna resposta base
        return f"""
**{resposta_base.get('resposta_base', 'Não encontrado')}**

ℹ️ *Para respostas mais personalizadas, configure sua API Key da OpenAI.*
        """

    from openai import OpenAI

    # Prepara contexto
    contexto_str = ""
    if contexto_usuario:
        if contexto_usuario.get("renda_mensal"):
            contexto_str += f"Contexto: Renda de R$ {contexto_usuario['renda_mensal']:,.2f}. "
        if contexto_usuario.get("objetivo"):
            contexto_str += f"Objetivo: {contexto_usuario['objetivo']}."

    prompt = f"""
Você é um assistente de educação financeira. Sua resposta deve ser clara, didática e amigável.

{contexto_str}

Resposta base para você usar e melhorar: {resposta_base.get('resposta_base', '')}

Regras:
1. Mantenha a informação precisa
2. Use linguagem simples e acessível
3. Adicione exemplos práticos se apropriado
4. Use formatação markdown para melhor leitura
5. No final, adicione: "ℹ️ *Isso é apenas uma explicação educativa, não uma recomendação financeira personalizada.*"
6. Responda em até 3 parágrafos
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        # Em caso de erro, retorna resposta base
        return resposta_base.get('resposta_base', 'Erro ao processar resposta')


def responder_pergunta(pergunta: str, contexto_usuario: dict = None) -> str:
    """
    Função principal para responder perguntas do usuário.

    Args:
        pergunta: Pergunta do usuário
        contexto_usuario: Dict opcional com contexto do usuário

    Returns:
        String com a resposta (base ou enriquecida com IA)
    """
    # Tenta buscar na base primeiro
    resposta_base = buscar_resposta_base(pergunta)

    if resposta_base:
        # Enriquece com IA se disponível
        return enriquecer_resposta_com_ia(resposta_base, contexto_usuario)
    else:
        # Se não encontrou na base, usa IA pura (se disponível)
        from modules.ia_helper import gerar_resposta_segura

        resposta_ia = gerar_resposta_segura(
            pergunta,
            contexto_usuario or {},
            []
        )

        # Adiciona aviso de que não encontrou na base
        if "não configurado" not in resposta_ia.lower():
            return f"{resposta_ia}\n\n💡 **Nota:** Esta resposta foi gerada com base em seu contexto, mas não está em nossa base de conhecimento."
        else:
            return resposta_ia


def obter_sugestoes_perguntas(n: int = 5) -> list:
    """
    Retorna sugestões de perguntas que o usuário pode fazer.

    Args:
        n: Número de sugestões

    Returns:
        Lista de strings com sugestões
    """
    base = carregar_base_conhecimento()

    if not base:
        return [
            "Como funciona a reserva de emergência?",
            "O que são juros compostos?",
            "Qual a diferença entre CDB e Tesouro Direto?",
            "Como funciona a inflação?",
            "O que é diversificação de investimentos?"
        ]

    # Extrai perguntas da base
    sugestoes = []
    for item in base[:n]:
        pergunta_base = item["pergunta"]

        # Transforma em pergunta completa
        if pergunta_base == "cdb":
            sugestoes.append("O que é CDB?")
        elif pergunta_base == "selic":
            sugestoes.append("O que é a taxa Selic?")
        elif pergunta_base == "juros compostos":
            sugestoes.append("Como funcionam os juros compostos?")
        elif pergunta_base == "reserva emergencia":
            sugestoes.append("Como criar uma reserva de emergência?")
        elif pergunta_base == "inflacao":
            sugestoes.append("O que é inflação e como ela me afeta?")
        else:
            sugestoes.append(f"Como funciona {pergunta_base}?")

    return sugestoes[:n]
