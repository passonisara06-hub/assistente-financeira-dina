"""
Módulo de gerenciamento de contexto
Responsável por inicializar e gerenciar o estado da sessão
"""

import streamlit as st
from typing import Any


def inicializar_contexto():
    """
    Inicializa o contexto da sessão do usuário se não existir.
    Gerencia informações persistentes durante a sessão.
    """
    if "contexto" not in st.session_state:
        st.session_state.contexto = {
            "renda_mensal": None,
            "gastos_fixos": None,
            "objetivo": None,
            "historico": [],  # Lista de interações anteriores
            "data_inicio": None
        }


def atualizar_contexto(chave: str, valor: Any):
    """
    Atualiza um valor específico no contexto da sessão.

    Args:
        chave: Nome do campo a ser atualizado
        valor: Novo valor
    """
    inicializar_contexto()
    st.session_state.contexto[chave] = valor


def obter_contexto() -> dict:
    """
    Retorna o contexto atual da sessão.

    Returns:
        Dict com o contexto atual
    """
    inicializar_contexto()
    return st.session_state.contexto


def limpar_contexto():
    """
    Limpa todos os dados do contexto, resetando para valores iniciais.
    """
    if "contexto" in st.session_state:
        st.session_state.contexto = {
            "renda_mensal": None,
            "gastos_fixos": None,
            "objetivo": None,
            "historico": [],
            "data_inicio": None
        }


def adicionar_historico(tipo: str, dados: dict):
    """
    Adiciona uma entrada ao histórico de interações.

    Args:
        tipo: Tipo de interação (ex: 'simulacao_reserva', 'faq', etc)
        dados: Dict com dados relevantes da interação
    """
    inicializar_contexto()

    import datetime
    entrada = {
        "tipo": tipo,
        "dados": dados,
        "timestamp": datetime.datetime.now().isoformat()
    }

    st.session_state.contexto["historico"].append(entrada)


def obter_historico(tipo: str = None) -> list:
    """
    Retorna o histórico de interações.

    Args:
        tipo: Filtra por tipo se fornecido, senão retorna tudo

    Returns:
        Lista de entradas do histórico
    """
    inicializar_contexto()
    historico = st.session_state.contexto["historico"]

    if tipo:
        return [h for h in historico if h["tipo"] == tipo]

    return historico


def formatar_contexto_para_ia() -> str:
    """
    Formata o contexto atual em string para ser usado em prompts de IA.

    Returns:
        String formatada com os dados do contexto
    """
    contexto = obter_contexto()
    partes = []

    if contexto["renda_mensal"]:
        partes.append(f"Renda mensal: R$ {contexto['renda_mensal']:,.2f}")

    if contexto["gastos_fixos"]:
        partes.append(f"Gastos fixos: R$ {contexto['gastos_fixos']:,.2f}")

    if contexto["objetivo"]:
        partes.append(f"Objetivo atual: {contexto['objetivo']}")

    if not partes:
        return "Usuário ainda não forneceu informações financeiras específicas."

    return " | ".join(partes)
