# Bot da FURIA Esports — Counter-Strike 2

Bot do Telegram que fornece informações em tempo real sobre o time competitivo de CS2 da FURIA Esports. Feito com Python, scraping via Selenium, integração com HLTV.org e respostas inteligentes com OpenAI.

## Funcionalidades

- /partidas — Mostra as próximas partidas da FURIA (via HLTV)
- /elenco — Exibe o elenco atual e a staff técnica
- /historico — Mostra as últimas 5 partidas jogadas
- /stats - stats dos jogadores da furia.
- info - Informaçòes sobre a fúria (redes sociais, SAC e etc.)

## Instalação

```bash
git clone https://github.com/seu-usuario/furia-cs-bot.git
cd furia-cs-bot
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

## Configuração

Certifique-se de instalar o chromedriver compativel com sua versão do Chrome e selecionar o diretório correto para o scrapper.
Crie um arquivo `.env` na raiz com suas chaves:

```
TELEGRAM_API_KEY=sua_chave
PANDASCORE_API_KEY=sua_chave
CHROMEDRIVER=diretório_chromedriver.exe
```

## Executar

```bash
python main.py
```
