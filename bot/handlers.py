from telebot import types
from .pandascore_api import get_upcoming_matches, get_furia_teams, get_last_matches
from bot.bo3_scraper import fetch_team_stats
from dotenv import load_dotenv
from dateutil import parser
import pytz

load_dotenv()
tz = pytz.timezone('America/Sao_Paulo')
 

def registrar_handlers(bot):
#COMANDO START
    @bot.message_handler(commands=['start', 'help', 'inicio'])
    def responder(msg):
        texto = (
            "🔥 Fala! Eu sou o *Bot da FURIA CS2*!\nAqui você encontra informações de todas as line-ups!\n\n"
            "Escolha uma opção:\n"
            "/partidas – ver as próximas partidas.\n"
            "/elenco – elencos atuais.\n"
            "/historico – ultimas 5 partidas jogadas."
            "/stats - (em desenvolvimento...)"
        )
        bot.send_message(msg.chat.id, texto)

#COMANDO PARTIDAS
    @bot.message_handler(commands=['partidas'])
    def partidas(msg):
        partidas = get_upcoming_matches()

        if len(partidas) == 0:
            bot.send_message(msg.chat.id, 'Não há partidas marcadas.')
            return

        texto = "*Próximas partidas da FURIA:*\n\n"

        for partida in partidas:
            time1 = partida["opponents"][0]["opponent"]["name"]
            time2 = partida["opponents"][1]["opponent"]["name"]
            data = parser.parse(partida['begin_at']).astimezone(tz)
            data_formatada = data.strftime('%d/%m/%Y, %H:%M')

            texto += f"🏆({partida["league"]['name']} {partida['serie']['full_name']})\n📅 {data_formatada}\n{time1} 🆚 {time2}\n\n"

        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

#COMANDO ELENCO
    @bot.message_handler(commands=['elenco', 'Elenco'])
    def elenco(msg):
        times = get_furia_teams()
        texto = "*Elencos da FURIA CS2:*\n"

        for time in times:
            texto += f"*{time['name']}:*\n"

            if len(time['players']) != 0: 
                for jogador in time['players']:
                    texto += f"{jogador['name']}\n"
            else:
                texto += "Não há jogadores neste elenco.\n"
            
            texto += "\n"

        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

#COMANDO HISTORICO
    @bot.message_handler(commands=['historico', 'Historico', 'Histórico', 'histórico'])
    def historico(msg):
        partidas = get_last_matches()

        texto = "*Últimas 5 partidas da FURIA:*\n\n"
        for partida in partidas:
            time1 = partida["opponents"][0]["opponent"]
            time2 = partida["opponents"][1]["opponent"]

            data = parser.parse(partida['begin_at']).astimezone(tz)
            data_formatada = data.strftime('%d/%m/%Y, %H:%M')

            resultado1 = next(result for result in partida['results'] if result["team_id"] == time1['id'])
            resultado2 = next(result for result in partida['results'] if result["team_id"] == time2['id'])

            texto += f"🏆({partida["league"]['name']} {partida['serie']['full_name']})\n📅 {data_formatada}\n{time1['name']} {resultado1['score']} 🆚 {resultado2['score']} {time2['name']}\n\n"

        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")
    
    
    @bot.message_handler(commands=['stats'])
    def stats(msg):
        try:
            furia_main = fetch_team_stats("furia")
            furia_fe = fetch_team_stats("furia-fe")
            furia_academy = fetch_team_stats("furia-academy")
            
            text = "*Estatísticas dos jogadores da FURIA (via BO3.gg):*\n\n"
            text += "*FURIA Main:*\n" + "\n".join(furia_main) + "\n\n"
            text += "*FURIA Female:*\n" + "\n".join(furia_fe) + "\n\n"
            text += "*FURIA Academy:*\n" + "\n".join(furia_academy)
            
            bot.send_message(msg.chat.id, text, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(msg.chat.id, f"Erro ao buscar estatísticas: {e}")
