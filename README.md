# README - Agente LangGraph + Ollama (usando o modelo gemma3)

Este guia explica como configurar e rodar um agente conversacional simples usando Python, LangGraph, Ollama, e o modelo local gemma3. Ideal para quem está começando com programação e ambientes virtuais.

## 🚀 Pré-requisitos

1. **Baixe e instale o Python 3.10 no seu computador.**
2. **Anaconda Prompt (recomendado)**
3. **Ollama instalado**: https://ollama.com/download
4. **Modelo gemma3 baixado**:
  
## 🛠️ Como usar

1. Clone o repositório para sua máquina usando o comando abaixo :
   
git clone https://github.com/Magda-tech/agente_langgraph_ollama.git

2. Crie um ambiente Conda no Anaconda Prompt:
   ```
   conda create -n langgraph_ollama python=3.10 # cria o ambiente
   conda activate langgraph_ollama              # ativa o ambiente
   cd agente_langgraph_ollama                   # entra na pasta onde está o arquivo requirements.txt
   pip install -r requirements.txt              # instala os pacotes no ambiente ativo

   ```
   
 3. Inicie o modelo gemma3 (em outro terminal):
    
   ```
  ollama run gemma3
   ```

4. Volte para o terminal no ambiente ativado langgraph_ollama e rode:
   
   ```
   pip install langchain-ollama
    ```
6. Abra o VS Code, use o comando Ctrl+Shift+P (Windows) e selecione Python: Select Interpreter e escolha o interpretador Python do ambiente Conda criado (langgraph_ollama).
 
 Agora você pode rodar o arquivo Python direto no VS Code usando o botão de execução ou terminal integrado.
 Digite suas perguntas no terminal. Para sair, digite sair.

## 🧪 Exemplos para testar

- `Quanto é 8 * 5?`
- `Onde fica o Brasil?`
- `Explique o que é LangGraph`

---
# Arquivos principais

agente_langgraph_ollama.py — código principal do agente

requirements.txt — dependências Python

.gitignore — arquivos ignorados no repositório

✅ Feito por Magda Monteiro para aprender sobre agentes inteligentes com modelos locais.
