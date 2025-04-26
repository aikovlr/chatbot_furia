from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def perguntar_openai(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um especialista em e-sports, CS2 e FURIA."},
                  {"role": "user", "content": pergunta}]
    )
    return resposta.choices[0].message["content"]
