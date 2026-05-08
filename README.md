# Agente DevOps Hermes

Projeto simples para estudo de agentes IA usando:
- Python
- Docker
- OpenRouter
- LLMs
- Tools com subprocess

## Funcionalidades

- Analisa Dockerfiles
- Gera documentação automática
- Executa tools do sistema
- Usa LLM para interpretação

## Como executar

```bash
docker run --rm -it \
  -v "$PWD":/workspace \
  -w /workspace \
  --entrypoint bash \
  hermes-local




