"""
Módulos do Coach Financeiro Digital
"""

from .contexto import (
    inicializar_contexto,
    atualizar_contexto,
    obter_contexto,
    limpar_contexto,
    adicionar_historico,
    obter_historico,
    formatar_contexto_para_ia
)

from .simulacoes import (
    calcular_reserva_emergencia,
    calcular_juros_compostos,
    calcular_amortizacao_sac
)

from .ia_helper import (
    inicializar_cliente,
    gerar_resposta_segura,
    personalizar_resposta,
    reformular_explicacao,
    responder_pergunta_chat,
    formatar_contexto_para_chat
)

from .faq import (
    carregar_base_conhecimento,
    buscar_resposta_base,
    responder_pergunta,
    obter_sugestoes_perguntas
)

from .perfil import (
    inicializar_perfil,
    atualizar_perfil,
    obter_perfil,
    salvar_perfil_json,
    carregar_perfil_json,
    gerar_dica_perfil,
    formatar_resumo_perfil,
    limpar_perfil
)

__all__ = [
    # Contexto
    'inicializar_contexto',
    'atualizar_contexto',
    'obter_contexto',
    'limpar_contexto',
    'adicionar_historico',
    'obter_historico',
    'formatar_contexto_para_ia',

    # Simulações
    'calcular_reserva_emergencia',
    'calcular_juros_compostos',
    'calcular_amortizacao_sac',

    # IA Helper
    'inicializar_cliente',
    'gerar_resposta_segura',
    'personalizar_resposta',
    'reformular_explicacao',
    'responder_pergunta_chat',
    'formatar_contexto_para_chat',

    # FAQ
    'carregar_base_conhecimento',
    'buscar_resposta_base',
    'responder_pergunta',
    'obter_sugestoes_perguntas',

    # Perfil
    'inicializar_perfil',
    'atualizar_perfil',
    'obter_perfil',
    'salvar_perfil_json',
    'carregar_perfil_json',
    'gerar_dica_perfil',
    'formatar_resumo_perfil',
    'limpar_perfil'
]
