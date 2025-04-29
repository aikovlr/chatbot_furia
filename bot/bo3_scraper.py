from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path="C:\\Users\\Matheus\\Desktop\\Rafael\\fatec\\Estagio\\chromedriver-win64\\chromedriver.exe")  # <-- ajusta aqui
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_team_stats(team_slug):
    url = f"https://bo3.gg/teams/{team_slug}/stats"
    driver = setup_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".stats-player"))
        )
        time.sleep(2)
        players_elements = driver.find_elements(By.CSS_SELECTOR, ".stats-player")
        stats = []
        for player in players_elements:
            name = player.find_element(By.CSS_SELECTOR, ".name").text.strip()
            rating = player.find_element(By.CSS_SELECTOR, ".rating").text.strip()
            kd = player.find_element(By.CSS_SELECTOR, ".kd").text.strip()
            adr = player.find_element(By.CSS_SELECTOR, ".adr").text.strip()
            kast = player.find_element(By.CSS_SELECTOR, ".kast").text.strip()
            stats.append(f"{name}: Rating {rating}, K/D {kd}, ADR {adr}, KAST {kast}")
        return stats
    except Exception as e:
        return [f"Erro ao carregar jogadores do time '{team_slug}': {e}"]
    finally:
        driver.quit()
