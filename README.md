# 🤖 Magda Assistente com LangGraph + Ollama

Este projeto implementa um agente inteligente local utilizando a biblioteca [LangGraph](https://python.langchain.com/docs/langgraph/) com suporte a modelos LLM via [Ollama](https://ollama.com/), permitindo interações personalizadas, incluindo cálculo, busca simulada e respostas com LLMs locais. Com suporte a **memória de contexto**, o assistente lembra das mensagens anteriores dentro da sessão.

## 🚀 Visão geral

O agente é composto por:

- Um **grafo de decisão** construído com `StateGraph` do LangGraph
- Um modelo local rodando com o **Ollama** (neste caso, `gemma3`)
- Três funções principais:
  - `calcular`: resolve perguntas matemáticas simples
  - `buscar`: simula uma busca local
  - `decidir`: atua como um roteador inteligente entre as opções acima ou aciona o modelo LLM para perguntas abertas
- Suporte a **memória** com `MemorySaver`, para manter o contexto entre as interações

---

## 🛠️ Como usar

1. Clone o repositório para sua máquina:

```bash
git clone https://github.com/Magda-tech/agente_langgraph_ollama.git
```

2. Crie e ative o ambiente Conda:

```bash
conda create -n langgraph_ollama python=3.10
conda activate langgraph_ollama
cd agente_langgraph_ollama
pip install -r requirements.txt
```

3. Instale o pacote para conectar com o Ollama:

```bash
pip install langchain-ollama
```

4. Em outro terminal, inicie o modelo local:

```bash
ollama run gemma3
```

5. No VS Code:

   - Pressione `Ctrl+Shift+P`
   - Escolha `Python: Select Interpreter`
   - Selecione o ambiente `langgraph_ollama`

6. Execute o arquivo `agente_langgraph_ollama.py` diretamente no terminal ou pelo botão de execução do VS Code.

Agora você pode digitar perguntas diretamente no terminal. Para sair, digite `sair`.

---

## 🧠 Como funciona o código

### 1. Esquema de estado com `TypedDict`

Define o formato do estado compartilhado entre os nós:

```python
class AgentState(TypedDict):
    mensagens: List[BaseMessage]
```

> Usamos `mensagens` ao invés de `mensagem/resposta`, para possibilitar a **memória conversacional**.

### 2. Modelo local com `OllamaLLM`

Carrega o modelo `gemma3` via Ollama:

```python
llm = OllamaLLM(model="gemma3")
```

### 3. Funções do agente

- `calcular`: usa `eval()` para resolver perguntas matemáticas como "quanto é 10 * 5"
- `buscar`: retorna uma resposta genérica simulando uma base de dados
- `decidir`: roteador inteligente que identifica qual nó seguir:
  - Se a pergunta contém "quanto é", envia para `calcular`
  - Se contém "onde" ou "quando", envia para `buscar`
  - Caso contrário, usa o LLM local para gerar uma resposta

### 4. Grafo com LangGraph

- O grafo é criado com `StateGraph`
- Os nós são adicionados com `add_node()` usando `RunnableLambda`
- A lógica de rota é definida em `add_conditional_edges`

```python
lambda x: x["fluxo"] if x["fluxo"] in ["calculo", "busca"] else "fim"
```

### 5. Memória com `MemorySaver`

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)
```

Com isso, o agente consegue lembrar interações anteriores dentro de uma mesma sessão.

---

## 🔪 Exemplos para testar

- `Quanto é 8 * 5?`
- `Multiplique isso por 2` (após um cálculo anterior)
- `Onde fica o Brasil?`

---

## 📂 Arquivos principais

- `agente_langgraph_ollama.py`: código principal do agente
- `requirements.txt`: dependências Python
- `.gitignore`: arquivos ignorados pelo Git

---

## 💡 Sobre o decisor inteligente

O nó `decidir` atua como um roteador automático:

- Analisa a mensagem de entrada
- Direciona o fluxo do grafo para o nó adequado (`calculo`, `busca` ou `LLM`)
- Garante uma resposta contextual e adaptativa

Esse mecanismo permite que o agente combine lógica determinística com a inteligência de um modelo local, criando um sistema responsivo e versátil.

---

## 🔁 Executando após reiniciar o computador

Sempre que desligar ou reiniciar seu computador, **não será necessário reinstalar nada**, apenas seguir os passos abaixo para reativar seu assistente:

### 1. Abra dois terminais

#### Terminal 1: Ative o ambiente Conda e rode o agente

```bash
conda activate langgraph_ollama
cd agente_langgraph_ollama
python agente_langgraph_ollama.py
```

#### Terminal 2: Inicie o modelo local via Ollama

```bash
ollama run gemma3
```

### ✅ Pronto!

Agora você pode interagir normalmente com o assistente.\
Digite sua pergunta no primeiro terminal. Para encerrar, digite `sair`.

---

✅ Feito por **Magda Monteiro** para aprender sobre agentes inteligentes com modelos locais.
