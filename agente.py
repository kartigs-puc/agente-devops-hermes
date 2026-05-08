from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

with open("input/Dockerfile", "r") as f:
    dockerfile = f.read()

prompt = f"""
Você é um agente DevOps iniciante-friendly.

Analise este Dockerfile:

{dockerfile}

Gere uma documentação em Markdown explicando:
1. objetivo da imagem
2. imagem base
3. cada instrução
4. porta exposta
5. como executar localmente
6. melhorias possíveis
"""

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

resultado = response.choices[0].message.content

with open("output/documentacao.md", "w") as f:
    f.write(resultado)

print("Documentação gerada com sucesso!")
