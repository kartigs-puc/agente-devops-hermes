from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def listar_arquivos():
    resultado = subprocess.run(
        ["ls", "-la"],
        capture_output=True,
        text=True
    )
    return resultado.stdout

lista_arquivos = listar_arquivos()

with open("input/Dockerfile", "r") as f:
    dockerfile = f.read()

prompt = f"""
Você é um agente DevOps.

Você tem acesso ao resultado da ferramenta listar_arquivos().

Resultado da tool:
{lista_arquivos}

Dockerfile encontrado:
{dockerfile}

Com base nisso:
1. Explique quais arquivos existem no projeto.
2. Explique o Dockerfile.
3. Diga se parece faltar algum arquivo importante.
4. Gere uma documentação em Markdown.

Responda somente com o Markdown final.
"""

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

resultado = response.choices[0].message.content

with open("output/documentacao_com_tool.md", "w") as f:
    f.write(resultado)

print("Documentação com tool gerada em output/documentacao_com_tool.md")
