from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_ollama import OllamaLLM
from typing import TypedDict

# Esquema do estado
class AgentState(TypedDict):
    mensagem: str
    resposta: str

# Modelo local personalizado
llm = OllamaLLM(model="gemma3")

# Ferramenta de cálculo
def calcular(state: AgentState) -> AgentState:
    pergunta = state["mensagem"]
    try:
        resultado = eval(pergunta.replace("quanto é", "").strip())
        return {"resposta": f"O resultado é {resultado}", "mensagem": pergunta}
    except:
        return {"resposta": "Não consegui calcular isso.", "mensagem": pergunta}

# Ferramenta de busca (simulada)
def buscar(state: AgentState) -> AgentState:
    return {"resposta": "Aqui está uma resposta simulada da base de conhecimento local.", "mensagem": state["mensagem"]}

# Decisor com roteamento
def decidir(state: AgentState) -> AgentState:
    pergunta = state["mensagem"]
    if "quanto é" in pergunta.lower():
        return {"mensagem": pergunta, "resposta": "calculo"}
    elif "onde" in pergunta.lower() or "quando" in pergunta.lower():
        return {"mensagem": pergunta, "resposta": "busca"}
    else:
        resposta = llm.invoke(pergunta)
        return {"mensagem": pergunta, "resposta": resposta}

# Criando o grafo
graph = StateGraph(state_schema=AgentState)
graph.add_node("decidir", RunnableLambda(decidir))
graph.add_node("calculo", RunnableLambda(calcular))
graph.add_node("busca", RunnableLambda(buscar))

graph.set_entry_point("decidir")

graph.add_conditional_edges(
    "decidir",
    lambda x: x["resposta"] if x["resposta"] in ["calculo", "busca"] else "fim",
    {
        "calculo": "calculo",
        "busca": "busca",
        "fim": END
    }
)

graph.add_edge("calculo", END)
graph.add_edge("busca", END)

app = graph.compile()

# Loop de chat interativo
print("🤖 Magda Assistente pronta! (digite 'sair' para encerrar)\n")
while True:
    entrada = input("Você: ")
    if entrada.strip().lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando a conversa. Até logo!")
        break

    saida = app.invoke({"mensagem": entrada})
    print(f"Magda: {saida['resposta']}\n")
