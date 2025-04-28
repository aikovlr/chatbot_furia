import os
import requests
from .fallback_api import perguntar_openai
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def is_pergunta_sobre_cs2(pergunta):
    """Verifica se a pergunta é sobre CS2/FURIA."""
    palavras_chave = ["furia", "cs2", "csgo", "jogo", "partida", "elenco", "estatística", "skins", "major"]
    return any(palavra in pergunta.lower() for palavra in palavras_chave)

def perguntar_deepseek(pergunta, contexto=""):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    system_message = (
        "Você é um assistente especialista em CS2 e FURIA Esports. "
        "Quando receber informações de contexto anteriores da FURIA, "
        "USE ESSE CONTEXTO para responder perguntas relacionadas. "
        "Não invente dados se eles não estiverem no contexto."
    )

    messages = [{"role": "system", "content": system_message}]

    # Adiciona contexto
    if contexto and is_pergunta_sobre_cs2(pergunta):
        messages.append({"role": "assistant", "content": f"Aqui estão os dados recentes da FURIA:\n{contexto}"})
        messages.append({"role": "user", "content": pergunta})
    else:
        messages.append({"role": "user", "content": pergunta})


    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7
            },
            timeout=10
        )

        if response.status_code == 200:
            resposta = response.json()["choices"][0]["message"]["content"]
        else:
            resposta = f"🔴 Erro na API (DeepSeek): {response.text}"

    except Exception as e:
        resposta = f"⚠️ Falha na conexão: {str(e)}"

    #Fallback
    try:
        if "Erro na API" in resposta or "Falha na conexão" in resposta:
            return perguntar_openai(pergunta)  
        return resposta
    except:
        return perguntar_openai(pergunta) 

