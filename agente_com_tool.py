from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import subprocess

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


def listar_arquivos():
    resultado = subprocess.run(
        ["ls", "-la"],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        return f"Erro ao listar arquivos: {resultado.stderr}"

    return resultado.stdout


lista_arquivos = listar_arquivos()

with open("input/Dockerfile", "r") as f:
    dockerfile = f.read()

prompt = f"""
Você é um agente DevOps.

Você tem acesso ao resultado de uma ferramenta chamada listar_arquivos().

Resultado da tool listar_arquivos():

{lista_arquivos}

Dockerfile encontrado:

{dockerfile}

Com base nisso:
1. Explique quais arquivos existem no projeto.
2. Explique o Dockerfile.
3. Diga se parece faltar algum arquivo importante.
4. Aponte possíveis melhorias.
5. Gere uma documentação em Markdown.

Responda somente com o Markdown final.
"""

response = client.chat.completions.create(
    model="nousresearch/hermes-3-llama-3.1-70b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

resultado = response.choices[0].message.content

arquivo_saida = gerar_nome_versionado("documentacao-com-tool")

with open(arquivo_saida, "w") as f:
    f.write(resultado)

print(f"Documentação com tool gerada com sucesso: {arquivo_saida}")
