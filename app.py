"""
Dina - Assistente Financeira Estratégica
Interface principal usando Streamlit
Atualizado com DeepSeek, Perfil Financeiro e Chat Interativo
"""

import streamlit as st
from modules.simulacoes import calcular_reserva_emergencia
from modules.perfil import (
    inicializar_perfil,
    atualizar_perfil,
    obter_perfil,
    salvar_perfil_json,
    carregar_perfil_json,
    gerar_dica_perfil,
    formatar_resumo_perfil,
    limpar_perfil
)
from modules.ia_helper import responder_pergunta_chat, formatar_contexto_para_chat
from modules.faq import responder_pergunta, obter_sugestoes_perguntas
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Dina - Sua Estrategista Financeira",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado com cores acessíveis
st.markdown("""
<style>
    /* Estilo do header principal */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
    }

    /* Caixas informativas */
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    .warning-box {
        background-color: #fff4e5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }

    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }

    /* Mensagens do chat */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }

    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }

    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #ff5722;
    }

    /* Valores monetários em azul (acessível para daltônicos) */
    .valor-monetario {
        color: #1E88E5 !important;
        font-weight: bold;
    }

    /* Métricas em azul em vez de verde */
    [data-testid="stMetricValue"] {
        color: #1E88E5 !important;
        font-weight: bold;
    }

    /* Valores positivos em azul */
    [data-testid="stMetricDelta"] svg {
        fill: #1E88E5 !important;
    }

    /* Títulos e headers */
    h1 {
        color: #1E88E5;
    }

    /* Rodapé da Dina */
    .dina-footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Função principal da aplicação"""

    # Inicializa perfil
    inicializar_perfil()

    # Header da Dina
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Dina - Sua Estrategista Financeira</h1>
        <p>Sua aliada estratégica para conquistar seus objetivos financeiros | Powered by DeepSeek</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar com informações do perfil
    with st.sidebar:
        st.header("📊 Seu Planejamento")

        perfil = obter_perfil()

        # Exibe resumo do perfil
        if perfil.get("renda_mensal") or perfil.get("gastos_fixos"):
            st.markdown(formatar_resumo_perfil())

            if perfil.get("sobra_mensal", 0) > 0:
                st.success(f"✅ Sobra: R$ {perfil['sobra_mensal']:,.2f}/mês")
            elif perfil.get("renda_mensal"):
                st.warning("⚠️ Sem sobra mensal")

        st.divider()

        # Botão para carregar perfil salvo
        if st.button("📂 Carregar Planejamento Salvo", use_container_width=True):
            if carregar_perfil_json():
                st.success("Planejamento carregado com sucesso!")
                st.rerun()
            else:
                st.info("Nenhum planejamento salvo encontrado.")

        # Botão para limpar perfil
        if st.button("🗑️ Limpar Planejamento", use_container_width=True):
            limpar_perfil()
            st.success("Planejamento limpo!")
            st.rerun()

        # Rodapé da Dina na sidebar
        st.divider()
        st.markdown("---")
        st.markdown("### 🎯 **Dina**")
        st.caption("Estratégia e disciplina para suas finanças")

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Meu Planejamento Financeiro",
        "🎯 Simuladores Estratégicos",
        "💬 Converse com a Dina",
        "❓ FAQ Inteligente"
    ])

    with tab1:
        perfil_financeiro()

    with tab2:
        simuladores_financeiros()

    with tab3:
        chat_com_dina()

    with tab4:
        faq_inteligente()

    # Rodapé
    st.markdown("""
    <div class="dina-footer">
        <p>🎯 <strong>Dina</strong> - Sua Estrategista Financeira | Disciplina e resiliência para sua vitória financeira</p>
        <p><em>Lembre-se: As informações fornecidas são apenas educativas. Consulte um profissional para decisões financeiras importantes.</em></p>
    </div>
    """, unsafe_allow_html=True)


def perfil_financeiro():
    """Aba de gerenciamento do perfil financeiro"""
    st.header("👤 Meu Planejamento Financeiro")

    st.markdown("""
    **Estratégia começa com clareza.** Preencha seus dados financeiros para que eu possa traçar
    o melhor plano de ação para você. Essas informações ficam salvas durante a sessão e ajudam
    a personalizar as orientações estratégicas.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("💰 Renda")

        renda = st.number_input(
            "Renda Mensal Líquida",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            value=obter_perfil().get("renda_mensal", 0.0),
            help="Valor total que você recebe por mês (salário, rendas extras, etc.)"
        )

        if renda is not None and renda > 0:
            atualizar_perfil("renda_mensal", renda)

    with col2:
        st.subheader("📉 Gastos Fixos")

        gastos_fixos = st.number_input(
            "Gastos Fixos Mensais",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            value=obter_perfil().get("gastos_fixos", 0.0),
            help="Aluguel, contas, alimentação básica, transporte, etc."
        )

        if gastos_fixos is not None and gastos_fixos > 0:
            atualizar_perfil("gastos_fixos", gastos_fixos)

    with col3:
        st.subheader("🛒 Gastos Variáveis")

        gastos_variaveis = st.number_input(
            "Gastos Variáveis Mensais",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            value=obter_perfil().get("gastos_variaveis", 0.0),
            help="Lazer, compras extras, restaurantes, etc."
        )

        if gastos_variaveis is not None and gastos_variaveis > 0:
            atualizar_perfil("gastos_variaveis", gastos_variaveis)

    with col4:
        st.subheader("🎂 Idade")

        idade = st.number_input(
            "Sua Idade",
            min_value=0,
            max_value=120,
            step=1,
            value=obter_perfil().get("idade", 0),
            help="Sua idade atual é crucial para o planejamento estratégico de longo prazo"
        )

        if idade is not None and idade > 0:
            atualizar_perfil("idade", idade)

    # Botão para salvar
    col_a, col_b, col_c = st.columns([1, 1, 2])

    with col_a:
        if st.button("💾 Salvar Planejamento", type="primary", use_container_width=True):
            if salvar_perfil_json():
                st.success("Planejamento salvo com sucesso!")
            else:
                st.error("Erro ao salvar planejamento.")

    with col_b:
        if st.button("🔄 Recalcular Estratégia", use_container_width=True):
            st.rerun()

    # Exibe resultados
    st.divider()

    perfil = obter_perfil()

    if perfil.get("renda_mensal") is not None and perfil.get("gastos_fixos") is not None:
        renda = perfil["renda_mensal"]
        gastos_fixos = perfil.get("gastos_fixos", 0)
        gastos_variaveis = perfil.get("gastos_variaveis", 0)
        total_gastos = gastos_fixos + gastos_variaveis
        sobra = renda - total_gastos

        st.subheader("📊 Análise Estratégica")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Renda Mensal", f"R$ {renda:,.2f}")

        with col2:
            st.metric("Total Gastos", f"R$ {total_gastos:,.2f}")

        with col3:
            st.metric(
                "Sobra Estratégica",
                f"R$ {max(0, sobra):,.2f}",
                delta=f"{'Positivo' if sobra > 0 else 'Negativo'}"
            )

        with col4:
            percentual = (sobra / renda * 100) if renda > 0 else 0
            st.metric("% Poupar", f"{max(0, percentual):.1f}%")

        # Dica personalizada
        st.markdown("---")
        dica = gerar_dica_perfil()
        st.markdown(f"**🎯 Estratégia da Dina:** {dica}")

        # Informação adicional se idade foi fornecida
        if perfil.get("idade") and sobra is not None and sobra > 0:
            anos_para_aposentadoria = max(0, 65 - perfil["idade"])
            if anos_para_aposentadoria > 0:
                total_poupado = sobra * 12 * anos_para_aposentadoria
                st.info(f"""
                🎯 **Planejamento de Longo Prazo:**

                Com sua sobra estratégica atual de **R$ {sobra:,.2f}/mês**, em **{anos_para_aposentadoria} anos**
                (até os 65 anos), você pode acumular aproximadamente **R$ {total_poupado:,.2f}**
                considerando apenas a poupança, sem investimentos.

                **Estratégia da Dina:** Invista esse valor para fazer seu dinheiro trabalhar para você.
                O tempo é seu maior aliado na batalha pela independência financeira!
                """)

        # Gráfico simples
        if renda > 0:
            import pandas as pd

            df = pd.DataFrame({
                'Categoria': ['Gastos Fixos', 'Gastos Variáveis', 'Sobra Estratégica'],
                'Valor': [gastos_fixos, gastos_variaveis, max(0, sobra)]
            })

            st.bar_chart(df.set_index('Categoria'), use_container_width=True)


def simuladores_financeiros():
    """Aba de simuladores financeiros"""
    st.header("🎯 Simuladores Estratégicos")

    st.info("🎯 **Nota da Dina:** Estou usando os dados do seu planejamento para criar simulações estratégicas personalizadas.")

    simulador = st.selectbox(
        "Escolha um simulador:",
        ["Selecione...", "Reserva de Emergência", "Juros Compostos", "Aposentadoria"]
    )

    if simulador == "Reserva de Emergência":
        st.subheader("🛡️ Estratégia de Reserva de Emergência")

        perfil = obter_perfil()

        # Usa dados do perfil se disponíveis
        renda_padrao = perfil.get("renda_mensal", 0.0)
        gastos_padrao = perfil.get("gastos_fixos", 0.0)

        col1, col2 = st.columns(2)

        with col1:
            renda = st.number_input(
                "Renda Mensal Líquida",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                value=renda_padrao
            )

        with col2:
            gastos = st.number_input(
                "Gastos Fixos Mensais",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                value=gastos_padrao
            )

        if st.button("🎯 Calcular Reserva", type="primary"):
            if renda > 0 and gastos > 0:
                resultado = calcular_reserva_emergencia(renda, gastos)

                if "erro" in resultado:
                    st.error(resultado["erro"])
                else:
                    st.success(f"🛡️ Reserva Estratégica: **R$ {resultado['reserva_recomendada']:,.2f}**")
                    st.markdown(resultado["explicacao"])

                    # Aviso educativo
                    st.markdown("""
                    <div class="warning-box">
                        ⚠️ <strong>Aviso Estratégico:</strong> Esta simulação é apenas educativa e não
                        leva em conta seu perfil completo. Para decisões financeiras importantes,
                        consulte um profissional qualificado.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Preencha todos os campos com valores estratégicos maiores que zero.")

    elif simulador == "Juros Compostos":
        st.subheader("📈 Estratégia de Juros Compostos")

        col1, col2, col3 = st.columns(3)

        with col1:
            principal = st.number_input(
                "Valor Inicial (R$)",
                min_value=0.0,
                step=100.0,
                value=1000.0
            )

        with col2:
            taxa = st.number_input(
                "Taxa Mensal (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                value=1.0,
                help="Ex: 1% ao mês = 0.01"
            )

        with col3:
            meses = st.number_input(
                "Período (meses)",
                min_value=1,
                max_value=360,
                step=1,
                value=12
            )

        aporte = st.number_input(
            "Aporte Mensal (opcional)",
            min_value=0.0,
            step=100.0,
            value=0.0
        )

        if st.button("🚀 Calcular Crescimento", type="primary"):
            from modules.simulacoes import calcular_juros_compostos

            resultado = calcular_juros_compostos(
                principal,
                taxa / 100,  # Converte % para decimal
                meses,
                aporte
            )

            if "erro" in resultado:
                st.error(resultado["erro"])
            else:
                st.success(f"💰 Valor Final Estratégico: **R$ {resultado['valor_final']:,.2f}**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Investido", f"R$ {resultado['total_investido']:,.2f}")

                with col2:
                    st.metric("Total em Juros", f"R$ {resultado['total_juros']:,.2f}")

                with col3:
                    rendimento = (resultado['total_juros'] / resultado['total_investido'] * 100) if resultado['total_investido'] > 0 else 0
                    st.metric("Rendimento", f"{rendimento:.1f}%")

                # Tabela mensal (últimos 6 meses)
                st.markdown("#### 📋 Evolução Mensal")

                import pandas as pd
                df = pd.DataFrame(resultado['tabela'][-6:])
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.markdown("""
                <div class="warning-box">
                    ℹ️ <strong>Estratégia:</strong> Juros compostos são sua arma secreta. Quanto mais tempo
                    deixa investir, maior o crescimento. Isso é apenas uma simulação educativa,
                    não uma recomendação de investimento.
                </div>
                """, unsafe_allow_html=True)

    elif simulador == "Aposentadoria":
        st.subheader("🎯 Estratégia de Aposentadoria")

        perfil = obter_perfil()

        # Usa idade do perfil se disponível
        idade_padrao = perfil.get("idade", 30)
        renda_padrao = perfil.get("renda_mensal", 5000.0)

        col1, col2, col3 = st.columns(3)

        with col1:
            idade_atual = st.number_input(
                "Sua Idade",
                min_value=18,
                max_value=80,
                step=1,
                value=idade_padrao
            )

        with col2:
            idade_aposentadoria = st.number_input(
                "Idade Aposentadoria",
                min_value=idade_atual + 1,
                max_value=90,
                step=1,
                value=65
            )

        with col3:
            renda_desejada = st.number_input(
                "Renda Mensal Desejada (R$)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                value=renda_padrao
            )

        anos_poupar = idade_aposentadoria - idade_atual
        taxa_retorno = st.number_input(
            "Taxa de Retorno Anual (%)",
            min_value=0.0,
            max_value=20.0,
            step=0.1,
            value=8.0,
            help="Retorno médio anual esperado dos investimentos"
        )

        if st.button("🎯 Calcular Estratégia", type="primary"):
            # Regra dos 4%
            patrimonio_necessario = renda_desejada * 12 * 25  # 25 anos = 4% ao ano

            meses_poupar = anos_poupar * 12
            taxa_mensal = (taxa_retorno / 100) / 12

            # Calcula poupança mensal necessária
            if taxa_mensal is not None and taxa_mensal > 0:
                poupanca_mensal = patrimonio_necessario / (((1 + taxa_mensal) ** meses_poupar - 1) / taxa_mensal)
            else:
                poupanca_mensal = patrimonio_necessario / meses_poupar

            st.success(f"🎯 **Patrimônio Estratégico: R$ {patrimonio_necessario:,.2f}**")
            st.info(f"""
            📊 **Plano Estratégico da Dina:**

            Para atingir uma renda de **R$ {renda_desejada:,.2f}/mês** aos {idade_aposentadoria} anos,
            considerando {anos_poupar} anos de disciplina:

            • **Patrimônio alvo:** R$ {patrimonio_necessario:,.2f}
            • **Investimento mensal:** R$ {poupanca_mensal:,.2f}
            • **Total investido:** R$ {poupanca_mensal * meses_poupar:,.2f}
            • **Total em juros:** R$ {patrimonio_necessario - poupanca_mensal * meses_poupar:,.2f}

            🎯 **Estratégia da Dina:** Comece agora! A disciplina é sua maior arma.
            """)

            # Gráfico de crescimento
            import pandas as pd
            import numpy as np

            anos = list(range(1, anos_poupar + 1))
            patrimonio_anual = []
            acumulado = 0

            for ano in anos:
                for _ in range(12):
                    acumulado = acumulado * (1 + taxa_mensal) + poupanca_mensal
                patrimonio_anual.append(acumulado)

            df = pd.DataFrame({
                'Ano': anos,
                'Patrimônio': patrimonio_anual
            })

            st.line_chart(df.set_index('Ano'), use_container_width=True)

            st.markdown("""
            <div class="warning-box">
                ℹ️ <strong>Estratégia:</strong> Este simulador usa a regra dos 4%, uma estratégia comum
                para planejamento de aposentadoria. Assume que você viverá até os 90 anos e que seus
                investimentos renderão a taxa especificada. Consulte um planejador financeiro para um
                plano personalizado.
            </div>
            """, unsafe_allow_html=True)


def chat_com_dina():
    """Aba de chat com IA DeepSeek - Dina"""
    st.header("💬 Converse com a Dina")

    st.info("🎯 **Sobre a Dina:** Sou sua estrategista financeira. Vou ajudar você a traçar o melhor plano para suas finanças com disciplina e resiliência.")

    # Verifica se a API está configurada
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key or api_key == "sk-sua-chave-aqui":
        st.warning("""
        ### ⚠️ Configure a API Key da DeepSeek

        Para conversar com a Dina, você precisa configurar sua API Key:

        1. Acesse: https://platform.deepseek.com/
        2. Crie sua conta e obtenha uma API Key
        3. Edite o arquivo `.env` e adicione: `DEEPSEEK_API_KEY=sua-chave-aqui`
        4. Reinicie a aplicação

        **Enquanto isso, use a aba FAQ Inteligente!**
        """)
        return

    # Inicializa histórico de mensagens
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Exibe contexto do usuário
    perfil = obter_perfil()
    if perfil.get("renda_mensal"):
        with st.expander("📊 Seu Contexto Estratégico"):
            contexto = formatar_contexto_para_chat(perfil)
            if perfil.get("idade"):
                contexto += f"\n🎂 Idade: {perfil['idade']} anos"
            st.markdown(contexto)

    # Saudação inicial da Dina
    if not st.session_state.chat_messages:
        st.info("🎯 **Olá! Sou a Dina,** sua estrategista financeira. Estou aqui para te ajudar a traçar a melhor estratégia para sua vida financeira. **Por onde vamos começar?**")

    # Exibe histórico de mensagens
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input para nova mensagem
    if prompt := st.chat_input("Digite sua pergunta sobre finanças..."):
        # Adiciona mensagem do usuário
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gera resposta da Dina
        with st.chat_message("assistant"):
            with st.spinner("🎯 A Dina está analisando sua estratégia..."):
                resposta = responder_pergunta_chat(
                    prompt,
                    perfil,
                    st.session_state.chat_messages
                )
                st.markdown(resposta)

        # Adiciona resposta ao histórico
        st.session_state.chat_messages.append({"role": "assistant", "content": resposta})

        # Mantém apenas últimas 10 mensagens para não pesar
        if len(st.session_state.chat_messages) > 10:
            st.session_state.chat_messages = st.session_state.chat_messages[-10:]

    # Botão para limpar histórico
    if st.session_state.chat_messages:
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.chat_messages = []
            st.success("Histórico limpo! Vamos traçar uma nova estratégia.")
            st.rerun()


def faq_inteligente():
    """Aba de FAQ inteligente"""
    st.header("📚 Perguntas Frequentes")

    st.info("🎯 A Dina preparou respostas estratégicas para as perguntas mais comuns sobre finanças!")

    # Sugestões de perguntas
    st.markdown("### 🔥 Perguntas Populares")

    sugestoes = obter_sugestoes_perguntas(4)

    col1, col2 = st.columns(2)

    with col1:
        for i, sugestao in enumerate(sugestoes[:2]):
            if st.button(sugestao, key=f"faq_{i}", use_container_width=True):
                st.session_state.pergunta_faq = sugestao

    with col2:
        for i, sugestao in enumerate(sugestoes[2:4]):
            if st.button(sugestao, key=f"faq_{i+2}", use_container_width=True):
                st.session_state.pergunta_faq = sugestao

    st.divider()

    # Campo de pergunta personalizada
    pergunta = st.text_input(
        "💬 Ou digite sua pergunta sobre finanças:",
        value=st.session_state.get("pergunta_faq", ""),
        placeholder="Ex: Como funciona a reserva de emergência?"
    )

    if st.button("🎯 Perguntar", type="primary") or pergunta:
        if pergunta:
            with st.spinner("🎯 A Dina está pesquisando..."):
                perfil = obter_perfil()
                resposta = responder_pergunta(pergunta, perfil)

                st.markdown(f"**❓ Pergunta:** {pergunta}")
                st.markdown("---")
                st.markdown(f"**🎯 Resposta da Dina:**\n\n{resposta}")

                # Limpa a pergunta após responder
                if "pergunta_faq" in st.session_state:
                    del st.session_state.pergunta_faq


if __name__ == "__main__":
    main()
