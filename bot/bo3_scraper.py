from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = CHROMEDRIVER

    service = Service(executable_path=CHROMEDRIVER)
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_team_stats(team_slug):
    url = f"https://bo3.gg/teams/{team_slug}#tab-stats"
    driver = setup_driver()
    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".item-button.player"))
        )
        
        ingame_stats = driver.find_element(By.CSS_SELECTOR, ".o-tab-content .o-layout:not([style*=\"display: none\"])")
        players = ingame_stats.find_elements(By.CSS_SELECTOR, ".item-button.player")
        
        stats_all = []
        for player in players:
            try:
                player.click()
                time.sleep(1)
                name = player.text

                table = ingame_stats.find_element(By.CSS_SELECTOR, ".c-table-ingame-stats")

                stats_names = table.find_elements(By.CSS_SELECTOR, ".table-cell.stat")
                stats_values = table.find_elements(By.CSS_SELECTOR, ".table-cell.avg")
                
                player_stats = map(lambda name, stat: f"{name.text} {stat.text}", stats_names, stats_values)

                stats_all.append(f"*{name}*: {", ".join(player_stats)}\n")
            except Exception as e:
                stats_all.append(f"Erro ao ler jogador: {e}")
        return stats_all
    except Exception as e:
        return [f"Erro ao carregar jogadores do time '{team_slug}': {e}"]
    finally:
        driver.quit()