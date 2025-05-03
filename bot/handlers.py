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
            "🔥 Fala! Eu sou o Bot da Furia CS2!\nAqui você encontra informações de todas as line-ups\n\n"
            "Escolha uma opção:\n"
            "/partidas – ver as próximas partidas.\n"
            "/elenco – elencos atuais.\n"
            "/historico – ultimas 5 partidas jogadas.\n"
            "/stats - stats dos jogadores da furia.\n"
            "/info - Informações sobre a furia (redes sociais, SAC e etc...)"
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
        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")
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
        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")

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
        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")
#COMANDO STATS
    @bot.message_handler(commands=['stats'])
    def stats(msg):
        texto=('Deseja ver as estatísticas de qual elenco?\n\n'
        '/statsfuria -> Furia principal.\n'
        '/statsfuriafe -> Furia fe.\n'
        '\nClique na opção desejada.')
        bot.send_message(msg.chat.id, texto)
        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")
#COMANDO STATS FURIA MAIN
    @bot.message_handler(commands=['statsfuria'])
    def statsfuria(msg):
        bot.send_message(msg.chat.id, "Carregando estatísticas...")
        try:
            furia_main = fetch_team_stats("furia")

            texto = "*Estatísticas dos jogadores da Furia (via BO3.gg):*\n\n"
            texto += "\n".join(furia_main) + "\n"
            texto += "Caso as estatísticas não apareçam, tente executar o comando novamente."

            bot.send_message(msg.chat.id, texto, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(msg.chat.id, "Erro ao buscar estatísticas.")
            print(e)

        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")
#COMANDO STATS FURIA-FE
    @bot.message_handler(commands=['statsfuriafe'])
    def statsfuriafe(msg):
        bot.send_message(msg.chat.id, "Carregando estatísticas...")
        try:
            furia_fe = fetch_team_stats("furia-fe")

            texto = "*Estatísticas das jogadoras da Furia fe (via BO3.gg):*\n\n"
            texto += "\n".join(furia_fe) + "\n"
            texto += "Caso as estatísticas não apareçam, tente executar o comando novamente."

            bot.send_message(msg.chat.id, texto, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(msg.chat.id, "Erro ao buscar estatísticas.")
            print(e)

        bot.send_message(msg.chat.id,"Caso deseje voltar para o inicio, digite ou clique em /inicio.")

#COMANDO INFO
    @bot.message_handler(commands=['info'])
    def info(msg):
        texto = "Quem somos?\n\n"
        texto += "Somos FURIA. Uma organização de esports que nasceu do desejo de representar o Brasil no CS e conquistou muito mais que isso: expandimos nossas ligas, disputamos os principais títulos, adotamos novos objetivos e ganhamos um propósito maior. Somos muito mais que o sucesso competitivo.\nSomos um movimento sociocultural\n Nossa história é de pioneirismo, grandes conquistas e tradição. Nosso presente é de desejo, garra e estratégia. A pantera estampada no peito estampa também nosso futuro de glória. Nossos pilares de performance, lifestyle, conteúdo, business, tecnologia e social são os principais constituintes do movimento FURIA, que representa uma unidade que respeita as individualidades e impacta positivamente os contextos em que se insere. Unimos pessoas e alimentamos sonhos dentro e fora dos jogos.\n"
        texto += "\nSAC da furia*:\nsac@furia.gg\n"
        texto += "\nNossas redes sociais:\n\n"
        texto += "https://www.instagram.com/furiagg\n"
        texto += "https://x.com/FURIA\n"
        texto += "https://www.tiktok.com/@furia\n"
        texto += "\nSite oficial da FURIA LifeStyle:"
        texto += "\nhttps://www.furia.gg/"
                
        bot.send_message(msg.chat.id, texto)
        bot.send_message(msg.chat.id, "Caso deseje voltar para o inicio, digite ou clique em /inicio.")
