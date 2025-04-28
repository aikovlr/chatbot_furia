import os
import requests
from dotenv import load_dotenv

load_dotenv()
authorizationKey = os.getenv("PANDASCORE_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": authorizationKey
}

def get_upcoming_matches():
    url = "https://api.pandascore.co/csgo/matches?filter[future]=true&search[name]=furia&page=1&per_page=100"

    response = requests.get(url, headers=headers)
    return response.json()

def get_furia_teams():
    url = "https://api.pandascore.co/csgo/teams?sort=acronym&search[name]=furia"

    response = requests.get(url, headers=headers)
    return response.json()

def get_player_stats(nome):
    print(nome)

def get_last_matches():
    url = "https://api.pandascore.co/csgo/matches?filter[future]=false&search[name]=furia&page=1&per_page=5"

    response = requests.get(url, headers=headers)
    return response.json()

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# def setup_driver():
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)
#     return driver

# def get_upcoming_matches():
#     driver = setup_driver()
#     driver.get("https://www.hltv.org/team/8297/furia")
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()
#     partidas = []
#     for match in soup.select(".upcomingMatch"):
#         data = match.select_one(".matchTime")["data-unix"]
#         oponente = match.select_one(".matchTeamName").text.strip()
#         evento = match.select_one(".matchEventName").text.strip()
#         partidas.append({"data": "timestamp", "oponente": oponente, "evento": evento})
#     return partidas[:3]

# def get_team_roster():
#     driver = setup_driver()
#     driver.get("https://www.hltv.org/team/8297/furia")
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()
#     jogadores, staff = [], []
#     for div in soup.select(".bodyshot-team .player-holder"):
#         nome = div.select_one(".text-ellipsis").text.strip()
#         flag = div.select_one("img")["title"]
#         funcao = "Atirador"  # placeholder
#         jogadores.append({"nome": nome, "flag": f":flag_{flag.lower()}:", "funcao": funcao})
#     return jogadores, staff

# def get_player_stats(nome):
#     return f"*Estatísticas de {nome.capitalize()}* K/D: 1.10 Rating: 1.18 Headshots: 48%"

# def get_last_matches():
#     return [
#         {"data": "22/04", "oponente": "Team X", "evento": "ESL", "resultado": "W 16-12"},
#         {"data": "20/04", "oponente": "Team Y", "evento": "BLAST", "resultado": "L 14-16"},
#     ]
