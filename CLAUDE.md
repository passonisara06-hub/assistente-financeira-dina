# Coach Digital para Metas Financeiras

Este é um assistente financeiro conversacional desenvolvido em Python que ajuda usuários a definir metas financeiras (reserva de emergência, compra de bens, quitação de dívidas) através de simulações educativas e planos passo a passo.

## 🎯 Propósito

Criar um "Coach Digital" que conversa com o usuário, oferece simulações financeiras educativas e orienta na definição de metas financeiras de forma didática e acessível.

## 🏗️ Arquitetura

### Estrutura de Pastas

```
meu_assistente_financeiro/
├── app.py                # Interface Streamlit (ponto de entrada)
├── modules/
│   ├── faq.py            # FAQ inteligente com busca e IA
│   ├── simulacoes.py     # Cálculos financeiros (juros, reserva, etc)
│   ├── contexto.py       # Gerenciamento de sessão e persistência
│   └── ia_helper.py      # Integração com OpenAI/GPT
├── data/
│   └── conhecimento.json # Base de conhecimento para FAQ
├── .env                  # Variáveis de ambiente (API_KEY)
├── requirements.txt      # Dependências Python
└── README.md            # Documentação do projeto
```

### Tecnologias Principais

- **Python 3.12+**: Linguagem principal
- **Streamlit**: Interface web interativa
- **OpenAI API**: IA generativa para respostas personalizadas (GPT-3.5-turbo ou GPT-4o-mini)
- **NumPy/Pandas**: Cálculos matemáticos e manipulação de dados
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 📋 Funcionalidades do MVP

1. **FAQ Inteligente (NLP)**
   - Banco de conhecimento local sobre finanças
   - Busca por similaridade (palavras-chave ou embeddings)
   - Fallback para IA generativa com personalização

2. **Simulador Financeiro**
   - Cálculo de juros compostos
   - Simulação de reserva de emergência
   - Planos de poupança personalizados
   - Explicações didáticas do raciocínio

3. **Persistência de Contexto**
   - Memória de conversa (renda, gastos, objetivos)
   - Retoma de onde parou
   - Histórico de interações

## 🎨 Princípios de UX

- **Clareza**: Pedir uma informação por vez, frases curtas
- **Consistência**: Tom educativo e simpático em todas as respostas
- **Linguagem Simples**: Explicar termos técnicos (ex: "juros sobre juros como uma bola de neve")
- **Acessibilidade**: Fontes legíveis, bom contraste, evitar cores como único indicador
- **Segurança**: Sempre incluir avisos educativos ("Isso é apenas uma simulação, não recomendação financeira")

## 🔐 Segurança e Restrições

**NUNCA faça:**
- Recomendar investimentos específicos ("compre ação X", "invista em CDB do banco Y")
- Prometer retornos garantidos
- Dar conseils personalizados sem contexto completo

**SEMPRE faça:**
- Incluir avisos educativos em cada simulação
- Usar linguagem condicional ("poderia", "pode ser útil")
- Sugerir consulta a profissionais para decisões importantes

## 💻 Convenções de Código

### Python
- Seguir PEP 8
- Type hints em funções públicas
- Docstrings explicando o propósito e parâmetros
- Validação de entradas (números negativos, strings vazias)

### Nomenclatura
- Arquivos: `snake_case.py`
- Funções: `snake_case`
- Classes: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`

### Exemplo de Função

```python
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
    if gastos_fixos <= 0:
        return {"erro": "Gastos fixos devem ser maiores que zero."}

    # ... implementação
```

## 🚀 Desenvolvimento

### Configuração Ambiente

1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar API Key:
```bash
# Criar arquivo .env com:
OPENAI_API_KEY=sk-...
```

### Executar Aplicação

```bash
streamlit run app.py
```

## 📦 Pilares do Projeto

### IA Generativa
- Personalização de respostas baseada no contexto do usuário
- Reformulação de explicações quando usuário pede clareza
- Tom educativo e acessível

### Python
- Funções puras para cálculos financeiros
- Organização modular (faq, simulacoes, contexto, ia_helper)
- Validação robusta de entradas

### Dados
- Estrutura JSON para base de conhecimento
- Sanitização de inputs do usuário
- Precisão matemática com numpy/math

### UX
- Jornada clara: boas-vindas → escolha objetivo → coleta dados → simulação → explicação → próximos passos
- Mensagens amigáveis e botões de ação
- Feedback construtivo em caso de erro

## 📝 Notas Importantes

- O projeto usa `streamlit.session_state` para persistência de contexto durante a sessão
- Para persistência longa-termo, considerar implementar salvamento em JSON
- O FAQ pode ser evoluido para usar embeddings com `sentence-transformers`
- Sempre validar inputs antes de passar para cálculos ou IA

## 🧪 Testes

Testar cenários:
- Validação de inputs negativos/zero
- Cálculos de edge cases (renda = gastos)
- Fallback do FAQ para IA
- Persistência de contexto entre páginas

## 📚 Recursos Adicionais

- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [PEP 8 Style Guide](https://pep8.org/)
