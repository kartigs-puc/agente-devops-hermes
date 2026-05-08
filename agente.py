from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def gerar_nome_versionado(prefixo):
    os.makedirs("output", exist_ok=True)

    arquivos = os.listdir("output")
    versoes = []

    padrao = rf"{prefixo}-v(\d+)\.md"

    for arquivo in arquivos:
        match = re.match(padrao, arquivo)
        if match:
            versoes.append(int(match.group(1)))

    proxima_versao = max(versoes) + 1 if versoes else 1

    return f"output/{prefixo}-v{proxima_versao}.md"


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

Responda somente com o Markdown final.
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

arquivo_saida = gerar_nome_versionado("documentacao")

with open(arquivo_saida, "w") as f:
    f.write(resultado)

print(f"Documentação gerada com sucesso: {arquivo_saida}")
