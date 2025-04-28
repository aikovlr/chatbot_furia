
from telebot import types
from .pandascore_api import get_upcoming_matches, get_furia_teams, get_player_stats, get_last_matches
from .deepseek_api import is_pergunta_sobre_cs2, perguntar_deepseek
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
            "/historico – ultimas 5 partidas jogadas.\n"
            "/pergunta - tire suas dúvidas com o bot!"
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

#COMANDO PERGUNTA (DEEPSEEKAI)
    def obter_contexto_furia():
        """Busca dados da PandaScore para usar como contexto."""
        contexto = ""
    
        # Adiciona próximas partidas
        partidas = get_upcoming_matches()
        if partidas:
            contexto += "Próximas partidas da FURIA:\n"
            for p in partidas[:3]:  # Limita a 3 partidas
                contexto += f"- {p['opponents'][0]['opponent']['name']} vs {p['opponents'][1]['opponent']['name']}\n"
    
        # Adiciona elenco
        times = get_furia_teams()
        if times and times[0]['players']:
            contexto += "\nElenco atual:\n"
            for jogador in times[0]['players']:
                contexto += f"- {jogador['name']}\n"
    
        return contexto


    @bot.message_handler(commands=['pergunta'])
    def pergunta(msg):
        pergunta = msg.text.replace("/pergunta", "").strip()
    
        if not pergunta:
            return bot.send_message(msg.chat.id, "❓ Digite sua pergunta. Ex: /pergunta Qual o time mais forte do CS2?")
    
        # Busca contexto apenas se for sobre CS2/FURIA
        contexto = ""
        palavras_chave = ["furia", "cs2", "csgo", "jogo", "partida", "elenco", "estatística"]
        if any(palavra in pergunta.lower() for palavra in palavras_chave):
            # Adiciona próximas partidas ao contexto
            partidas = get_upcoming_matches()
            if partidas:
                contexto += "Próximas partidas da FURIA:\n"
                for p in partidas[:3]:  # Limita a 3 partidas
                    contexto += f"- {p['opponents'][0]['opponent']['name']} vs {p['opponents'][1]['opponent']['name']}\n"
        
            # Adiciona elenco ao contexto
            times = get_furia_teams()
            if times and times[0]['players']:
                contexto += "\nElenco atual:\n"
                for jogador in times[0]['players']:
                    contexto += f"- {jogador['name']}\n"
    
    # Chama a DeepSeek
        resposta = perguntar_deepseek(pergunta, contexto)
        bot.send_message(msg.chat.id, resposta)

        print(pergunta)
        print(is_pergunta_sobre_cs2(pergunta))

#    @bot.message_handler(commands=['Estatistica'])
#   def estatistica(msg):
#        texto = "Digite o nome de um jogador após o comando. Ex: `/Estatistica yuurih`"
#        bot.send_message(msg.chat.id, texto, parse_mode="Markdown")

    # @bot.message_handler(func=lambda m: m.text.startswith('/Estatistica '))
    # def estat_jogador(msg):
    #     nome = msg.text.replace("/Estatistica", "").strip().lower()
    #     stats = get_player_stats(nome)
    #     bot.send_message(msg.chat.id, stats, parse_mode="Markdown")