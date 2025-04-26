# Bot da FURIA Esports — Counter-Strike 2

Bot do Telegram que fornece informações em tempo real sobre o time competitivo de CS2 da FURIA Esports. Feito com Python, scraping via Selenium, integração com HLTV.org e respostas inteligentes com OpenAI.

## Funcionalidades
- /Partidas — Mostra as próximas partidas da FURIA (via HLTV)
- /Elenco — Exibe o elenco atual e a staff técnica com bandeiras e funções
- /Estatistica <jogador> — Retorna estatísticas oficiais do jogador via HLTV
- /Historico — Mostra as últimas 5 partidas jogadas
- /Perguntar <sua pergunta> — Inteligência Artificial responde perguntas sobre a FURIA e CS2

## Instalação
```bash
git clone https://github.com/seu-usuario/furia-cs-bot.git
cd furia-cs-bot
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

## Configuração
Crie um arquivo `.env` na raiz com suas chaves:
```
TELEGRAM_API_KEY=sua_chave
OPENAI_API_KEY=sua_chave
```

## Executar
```bash
python main.py
```
