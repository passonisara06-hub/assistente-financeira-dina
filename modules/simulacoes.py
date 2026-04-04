"""
Módulo de simulações financeiras
Contém funções para cálculos financeiros educativos
"""


def calcular_reserva_emergencia(renda_mensal: float, gastos_fixos: float) -> dict:
    """
    Calcula a reserva de emergência recomendada (6 meses de gastos).

    Args:
        renda_mensal: Renda mensal líquida do usuário
        gastos_fixos: Total de gastos fixos mensais

    Returns:
        Dict com 'reserva_recomendada', 'explicacao' e 'meses_necessarios'
        ou {'erro': 'mensagem'} em caso de validação falhar
    """
    # Validação
    if gastos_fixos <= 0:
        return {"erro": "Gastos fixos devem ser maiores que zero."}

    if renda_mensal <= 0:
        return {"erro": "Renda mensal deve ser maior que zero."}

    # Cálculo da reserva (6 meses de gastos)
    reserva_recomendada = gastos_fixos * 6

    # Cálculo de meses para juntar
    poupanca_mensal = renda_mensal - gastos_fixos

    if poupanca_mensal > 0:
        meses_para_juntar = reserva_recomendada / poupanca_mensal
    else:
        meses_para_juntar = float('inf')

    # Explicação didática
    explicacao = f"""
📘 **Como cheguei nesse cálculo?**

Especialistas em finanças pessoais sugerem que uma reserva de emergência ideal seja equivalente a **6 meses de gastos fixos**.

**Seus dados:**
- Gastos fixos mensais: R$ {gastos_fixos:,.2f}
- Reserva ideal recomendada: **R$ {reserva_recomendada:,.2f}**
"""

    if meses_para_juntar != float('inf'):
        explicacao += f"""

**Seu plano de poupança:**
- Renda mensal: R$ {renda_mensal:,.2f}
- Poupança mensal possível: R$ {poupanca_mensal:,.2f}
- ⏱️ Tempo estimado: **{meses_para_juntar:.1f} meses** ({meses_para_juntar/12:.1f} anos)

💡 **Dica:** Considere automatizar sua poupança com transferências automáticas no dia
do recebimento de sua renda. Isso ajuda a manter a constância!
"""
    else:
        explicacao += f"""

⚠️ **Atenção:** Sua renda atual (R$ {renda_mensal:,.2f}) não cobre seus gastos fixos (R$ {gastos_fixos:,.2f}).

**Sugestões:**
1. Revise seus gastos fixos e identifique onde pode reduzir
2. Considere fontes adicionais de renda
3. Procure equilibrar suas finanças antes de formar a reserva
"""

    return {
        "reserva_recomendada": round(reserva_recomendada, 2),
        "explicacao": explicacao,
        "meses_necessarios": round(meses_para_juntar, 1) if meses_para_juntar != float('inf') else None
    }


def calcular_juros_compostos(
    principal: float,
    taxa_mensal: float,
    meses: int,
    aporte_mensal: float = 0
) -> dict:
    """
    Calcula juros compostos com aportes mensais opcionais.

    Args:
        principal: Valor inicial investido
        taxa_mensal: Taxa de juros mensal (em decimal, ex: 0.01 para 1%)
        meses: Período em meses
        aporte_mensal: Valor a depositar mensalmente (opcional)

    Returns:
        Dict com valor final, total investido, total em juros e tabela mensal
    """
    # Validação
    if principal < 0 or taxa_mensal < 0 or meses <= 0 or aporte_mensal < 0:
        return {"erro": "Parâmetros inválidos. Use valores não-negativos e meses > 0."}

    valor_atual = principal
    total_investido = principal
    tabela = []

    for mes in range(1, meses + 1):
        # Aplica juros
        juros_mes = valor_atual * taxa_mensal
        valor_atual += juros_mes

        # Adiciona aporte mensal
        valor_atual += aporte_mensal
        total_investido += aporte_mensal

        tabela.append({
            "mes": mes,
            "valor": round(valor_atual, 2),
            "juros_mes": round(juros_mes, 2)
        })

    total_juros = valor_atual - total_investido

    return {
        "valor_final": round(valor_atual, 2),
        "total_investido": round(total_investido, 2),
        "total_juros": round(total_juros, 2),
        "tabela": tabela
    }


def calcular_amortizacao_sac(
    valor_financiado: float,
    taxa_juros: float,
    meses: int
) -> dict:
    """
    Calcula tabela de amortização usando o sistema SAC (Sistema de Amortização Constante).

    Args:
        valor_financiado: Valor total financiado
        taxa_juros: Taxa de juros mensal (decimal)
        meses: Número de meses para pagamento

    Returns:
        Dict com tabela de amortização e totais
    """
    # Validação
    if valor_financiado <= 0 or taxa_juros < 0 or meses <= 0:
        return {"erro": "Parâmetros inválidos"}

    amortizacao_constante = valor_financiado / meses
    saldo_devedor = valor_financiado
    tabela = []
    total_juros = 0
    total_pago = 0

    for mes in range(1, meses + 1):
        juros_mes = saldo_devedor * taxa_juros
        prestacao = amortizacao_constante + juros_mes

        saldo_devedor -= amortizacao_constante
        total_juros += juros_mes
        total_pago += prestacao

        tabela.append({
            "mes": mes,
            "prestacao": round(prestacao, 2),
            "amortizacao": round(amortizacao_constante, 2),
            "juros": round(juros_mes, 2),
            "saldo_devedor": round(max(0, saldo_devedor), 2)
        })

    return {
        "tabela": tabela,
        "total_pago": round(total_pago, 2),
        "total_juros": round(total_juros, 2),
        "primeira_prestacao": round(tabela[0]["prestacao"], 2) if tabela else 0,
        "ultima_prestacao": round(tabela[-1]["prestacao"], 2) if tabela else 0
    }
