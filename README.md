# 🎯 Dina - Sua Estrategista Financeira

[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Sua estrategista financeira para conquistar seus objetivos através de disciplina, resiliência e planejamento estratégico.**

Dina é uma assistente financeira conversacional desenvolvida em Python com Streamlit e IA generativa (DeepSeek), que ajuda usuários a planejar suas finanças através de simulações estratégicas e orientações personalizadas.

---

## 🌟 Funcionalidades

### 👤 Planejamento Financeiro Personalizado
- Cadastro de renda, gastos fixos e variáveis
- Campo de idade para planejamento estratégico de longo prazo
- Cálculo automático de sobra estratégica
- Orientações personalizadas baseadas no perfil
- Visualizações gráficas do seu panorama financeiro

### 🎯 Simuladores Estratégicos
- **Reserva de Emergência:** Sua linha de defesa financeira
- **Juros Compostos:** Veja seu dinheiro crescer com o tempo
- **Aposentadoria:** Planeje sua independência financeira

### 💬 Chat com a Dina
- Assistente conversacional com IA (DeepSeek)
- Respostas estratégicas contextualizadas com seu perfil
- Histórico de conversa mantido durante a sessão
- Perguntas sobre qualquer tema financeiro

### ❓ FAQ Inteligente
- 10+ tópicos financeiros essenciais
- Respostas educativas e estratégicas
- Busca rápida por palavras-chave

---

## 🚀 Como Usar

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/dina-estrategista-financeira.git
cd dina-estrategista-financeira
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure a API Key da DeepSeek:**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua chave:
# DEEPSEEK_API_KEY=sk-sua-chave-aqui
```

> 💡 **Obtenha sua chave gratuita em:** https://platform.deepseek.com/

### Execução

```bash
streamlit run app.py
```
---

## 📁 Estrutura do Projeto

```
dina-estrategista-financeira/
├── app.py                    # Interface principal (Streamlit)
├── modules/
│   ├── __init__.py          # Inicialização do pacote
│   ├── perfil.py            # Gerenciamento de perfil financeiro
│   ├── simulacoes.py        # Cálculos financeiros estratégicos
│   ├── ia_helper.py         # Integração com DeepSeek
│   ├── faq.py              # FAQ inteligente
│   └── contexto.py         # Gerenciamento de contexto
├── data/
│   └── conhecimento.json    # Base de conhecimento financeiro
├── requirements.txt         # Dependências Python
├── .env.example            # Template de configuração
├── .gitignore              # Arquivos ignorados pelo Git
├── CLAUDE.md               # Documentação técnica
└── README.md               # Este arquivo
```

---

## 🎯 Principais Características

### 🎯 Personalidade Única
- **Nome:** Dina (inspirada em guerreira estratégica)
- **Tom:** Direto, claro, confiante e acolhedor
- **Abordagem:** Estratégica, focada em disciplina e resiliência
- **Metodologia:** Planejamento tático para objetivos financeiros

### 🔵 Acessibilidade
- Cores em azul (#1E88E5) adequadas para daltônicos
- Contraste adequado em todos os elementos
- Ícones + cores para melhor diferenciação
- Linguagem clara e inclusiva

### 🔒 Segurança
- Avisos educativos em todas as respostas
- Sem recomendações de investimento específicas
- Foco em educação financeira estratégica
- Dados salvos localmente (no navegador)

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+** - Linguagem principal
- **Streamlit 1.56+** - Interface web interativa
- **DeepSeek API** - IA generativa para respostas estratégicas
- **Pandas & NumPy** - Cálculos matemáticos e manipulação de dados
- **python-dotenv** - Gerenciamento de variáveis de ambiente

---

## 📖 Exemplos de Uso

### 1. Planejamento de Reserva de Emergência

```
Usuário: "Quero criar uma reserva de emergência."

Dina: "Com sua renda de R$ 5.000,00 e gastos de R$ 3.500,00,
você tem uma sobra estratégica de R$ 1.500,00. Minha recomendação:
guarde 50% disso (R$ 750,00) por mês. Em 20 meses, você terá sua
reserva de R$ 15.000,00 (6 meses de gastos). Disciplina é a chave!"
```

### 2. Estratégia de Aposentadoria

```
Usuário (30 anos): "Quando posso me aposentar?"

Dina: "Se você começar a investir R$ 4.500,00 por mês agora,
aos 65 anos terá um patrimônio de aproximadamente R$ 1.500.000,00,
suficiente para uma renda de R$ 5.000,00/mês. O tempo é seu maior
aliado nessa batalha pela independência financeira!"
```

### 3. Orientação Estratégica

```
Perfil: Renda 4.000, Gastos 3.000, Sobra 1.000

Dina: "Com essa sobra de R$ 1.000,00, sugiro a seguinte estratégia:
- 50% para reserva de emergência (sua linha de defesa)
- 30% para investimentos de longo prazo (seu ataque)
- 20% para objetivos de curto prazo (suas batalhas menores)

Vamos traçar esse plano juntos?"
```

---

## ⚠️ Aviso Importante

**Este projeto tem finalidade exclusivamente educativa.**

Todas as simulações, cálculos e orientações fornecidas por Dina são apenas para fins educativos e não constituem:

- Recomendações de investimento personalizadas
- Aconselhamento financeiro profissional
- Consultoria de investimentos
- Análise de perfil de investidor

Para decisões financeiras importantes, **sempre consulte um profissional qualificado**.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

**Áreas para contribuição:**
- Novos simuladores financeiros
- Melhorias na interface estratégica
- Novos tópicos no FAQ
- Traduções para outros idiomas
- Melhorias na acessibilidade

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- **DeepSeek** - Pela API de IA generativa acessível
- **Streamlit** - Pela framework incrível para aplicações de dados
- **Comunidade Python** - Pela biblioteca rica de ferramentas

---

## 📞 Suporte

- **Issues:** [GitHub Issues](https://github.com/seu-usuario/dina-estrategista-financeira/issues)
- **Documentação Técnica:** [CLAUDE.md](CLAUDE.md)
- **DeepSeek Platform:** https://platform.deepseek.com/

---

## 🎉 Demo

[![Demo Dina](https://img.shields.io/badge/Demo-Online-orange.svg)](http://localhost:8501)

**Experimente a Dina localmente seguindo as instruções de instalação acima!**

---

<div align="center">

**🎯 Desenvolvido com disciplina para sua vitória financeira 🎯**

*[Feito com estratégia e Python]*

</div>
