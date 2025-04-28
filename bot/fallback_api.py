# fallback_api.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # <- carrega UMA VEZ só

def perguntar_openai(pergunta):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro no fallback: {str(e)}"
