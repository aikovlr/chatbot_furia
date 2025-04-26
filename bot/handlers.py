
from telebot import types
from .hltv_api import get_upcoming_matches, get_team_roster, get_player_stats, get_last_matches
from .openai_api import perguntar_openai
from dotenv import load_dotenv
import os

load_dotenv()

def registrar_handlers(bot):
    @bot.message_handler(commands=['Partidas'])
    def partidas(msg):
        partidas = get_upcoming_matches()
        texto = "*Próximas partidas da FURIA:*"
        for partida in partidas:
            texto += f"📅 {partida['data']} - 🆚 {partida['oponente']} ({partida['evento']})\n"

        print(partidas)
        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

    @bot.message_handler(commands=['Elenco'])
    def elenco(msg):
        jogadores, staff = get_team_roster()
        texto = "*Elenco da FURIA CS2:*"
        for player in jogadores:
            texto += f"{player['flag']} *{player['nome']}* - `{player['funcao']}`\n"
        texto += "\n*Staff Técnica:* "
        for membro in staff:
            texto += f"👤 {membro['nome']} - `{membro['funcao']}`\n"

        print("Elenco: " + texto)
        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

    @bot.message_handler(commands=['Estatistica'])
    def estatistica(msg):
        texto = "Digite o nome de um jogador após o comando. Ex: `/Estatistica yuurih`"
        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

    @bot.message_handler(commands=['Historico'])
    def historico(msg):
        historico = get_last_matches()
        texto = "*Últimas 5 partidas da FURIA:*"
        for partida in historico:
            texto += f"{partida['data']} - 🆚 {partida['oponente']} ({partida['evento']}) - *{partida['resultado']}*\n"
        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

    @bot.message_handler(commands=['Perguntar'])
    def perguntar(msg):
        pergunta = msg.text.replace("/Perguntar", "").strip()
        if not pergunta:
            bot.send_message(msg.chat.id, "Digite sua pergunta após o comando.")
            return
        resposta = perguntar_openai(pergunta)
        bot.send_message(msg.chat.id, resposta)

    @bot.message_handler(func=lambda m: m.text.startswith('/Estatistica '))
    def estat_jogador(msg):
        nome = msg.text.replace("/Estatistica", "").strip().lower()
        stats = get_player_stats(nome)
        bot.send_message(msg.chat.id, stats, parse_mode="Markdown")
