"""
Módulo de gerenciamento de perfil financeiro
Responsável por salvar, carregar e calcular métricas do perfil financeiro
"""

import streamlit as st
import json
import os
from typing import Dict, Optional


def inicializar_perfil():
    """
    Inicializa o perfil financeiro na session_state se não existir.
    """
    if "perfil_financeiro" not in st.session_state:
        st.session_state.perfil_financeiro = {
            "renda_mensal": None,
            "gastos_fixos": None,
            "gastos_variaveis": None,
            "sobra_mensal": None,
            "idade": None,
            "objetivo": None
        }


def atualizar_perfil(campo: str, valor):
    """
    Atualiza um campo específico do perfil.

    Args:
        campo: Nome do campo
        valor: Novo valor
    """
    inicializar_perfil()
    st.session_state.perfil_financeiro[campo] = valor

    # Recalcula sobra se dados relevantes mudaram
    if campo in ["renda_mensal", "gastos_fixos", "gastos_variaveis"]:
        calcular_sobra_mensal()


def calcular_sobra_mensal():
    """
    Calcula a sobra mensal baseada na renda e gastos.
    """
    import streamlit as st
    perfil = st.session_state.perfil_financeiro

    renda = perfil.get("renda_mensal") or 0
    gastos_fixos = perfil.get("gastos_fixos") or 0
    gastos_variaveis = perfil.get("gastos_variaveis") or 0

    sobra = renda - gastos_fixos - gastos_variaveis
    perfil["sobra_mensal"] = max(0, sobra)  # Não permite sobra negativa


def obter_perfil() -> Dict:
    """
    Retorna o perfil financeiro atual.

    Returns:
        Dict com o perfil completo
    """
    inicializar_perfil()
    return st.session_state.perfil_financeiro


def salvar_perfil_json():
    """
    Salva o perfil atual em um arquivo JSON local.
    """
    perfil = obter_perfil()

    caminho_arquivo = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "perfil_usuario.json"
    )

    # Cria diretório se não existir
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(perfil, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar perfil: {e}")
        return False


def carregar_perfil_json() -> Optional[Dict]:
    """
    Carrega o perfil de um arquivo JSON local.

    Returns:
        Dict com o perfil ou None se não existir
    """
    caminho_arquivo = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "perfil_usuario.json"
    )

    try:
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                perfil = json.load(f)
                st.session_state.perfil_financeiro = perfil
                return perfil
    except Exception as e:
        st.warning(f"Não foi possível carregar o perfil salvo: {e}")

    return None


def gerar_dica_perfil() -> str:
    """
    Gera uma dica personalizada baseada no perfil do usuário.

    Returns:
        String com a dica
    """
    perfil = obter_perfil()
    sobra = perfil.get("sobra_mensal", 0)

    if sobra <= 0:
        return "💡 **Dica:** Seus gastos estão iguais ou maiores que sua renda. Revise seus gastos fixos e variáveis para criar uma sobra mensal."

    elif sobra < 500:
        return f"💡 **Dica:** Você tem uma sobra de R$ {sobra:,.2f}. Que tal começar guardando 50% disso para emergências?"

    elif sobra < 2000:
        return f"💡 **Dica:** Ótima sobra de R$ {sobra:,.2f}! Tente guardar pelo menos R$ {sobra * 0.5:,.2f} por mês para construir sua reserva de emergência."

    else:
        return f"💡 **Dica:** Excelente! Com R$ {sobra:,.2f} de sobra, você pode investir em emergências (6 meses de gastos) e começar a investir para o longo prazo."


def formatar_resumo_perfil() -> str:
    """
    Formata um resumo do perfil para exibição.

    Returns:
        String formatada com o resumo
    """
    perfil = obter_perfil()

    partes = []

    if perfil.get("renda_mensal"):
        partes.append(f"💰 **Renda Mensal:** R$ {perfil['renda_mensal']:,.2f}")

    if perfil.get("gastos_fixos"):
        partes.append(f"📉 **Gastos Fixos:** R$ {perfil['gastos_fixos']:,.2f}")

    if perfil.get("gastos_variaveis"):
        partes.append(f"🛒 **Gastos Variáveis:** R$ {perfil['gastos_variaveis']:,.2f}")

    if perfil.get("sobra_mensal") is not None and perfil['sobra_mensal'] > 0:
        partes.append(f"✅ **Sobra Mensal:** R$ {perfil['sobra_mensal']:,.2f}")
    elif perfil.get("renda_mensal") and perfil.get("gastos_fixos"):
        partes.append("⚠️ **Sobra Mensal:** R$ 0,00 (sem sobra)")

    if not partes:
        return "Perfil ainda não preenchido. Preencha seus dados financeiros abaixo!"

    return "\n\n".join(partes)


def limpar_perfil():
    """
    Limpa todos os dados do perfil financeiro.
    """
    if "perfil_financeiro" in st.session_state:
        st.session_state.perfil_financeiro = {
            "renda_mensal": None,
            "gastos_fixos": None,
            "gastos_variaveis": None,
            "sobra_mensal": None,
            "idade": None,
            "objetivo": None
        }
