from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.runnables import RunnableLambda
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

# Modelo local
llm = OllamaLLM(model="gemma3")

# Mensagem de sistema opcional (ajusta o comportamento do agente)
system_message = SystemMessage(content="Você é um assistente útil que pode fazer cálculos e responder perguntas gerais. Use o histórico da conversa para responder perguntas de acompanhamento.")

# Ferramenta de cálculo simples
def calcular(state: MessagesState) -> dict:
    mensagens = state["messages"]
    pergunta = mensagens[-1].content

    try:
        resultado = eval(pergunta.replace("quanto é", "").strip())
        resposta = f"O resultado é {resultado}"
    except:
        resposta = "Não consegui calcular isso."
    
    return {"messages": mensagens + [AIMessage(content=resposta)]}

# Ferramenta de busca (simulada)
def buscar(state: MessagesState) -> dict:
    mensagens = state["messages"]
    resposta = "Aqui está uma resposta simulada da base de conhecimento local."
    return {"messages": mensagens + [AIMessage(content=resposta)]}

# Decisor inteligente: escolhe qual caminho seguir
def decidir(state: MessagesState) -> dict:
    mensagens = state["messages"]
    ultima = mensagens[-1].content.lower()

    if "quanto é" in ultima:
        return {"messages": mensagens + [AIMessage(content="calculo")]}
    elif "onde" in ultima or "quando" in ultima:
        return {"messages": mensagens + [AIMessage(content="busca")]}
    else:
        # Inclui system message + histórico
        contexto = [system_message] + mensagens
        resposta = llm.invoke(contexto)
        return {"messages": mensagens + [AIMessage(content=resposta)]}

# Criar o grafo com suporte a memória
graph = StateGraph(MessagesState)
graph.add_node("decidir", RunnableLambda(decidir))
graph.add_node("calculo", RunnableLambda(calcular))
graph.add_node("busca", RunnableLambda(buscar))

graph.set_entry_point("decidir")

graph.add_conditional_edges(
    "decidir",
    lambda state: state["messages"][-1].content if state["messages"][-1].content in ["calculo", "busca"] else "fim",
    {
        "calculo": "calculo",
        "busca": "busca",
        "fim": END
    }
)

graph.add_edge("calculo", END)
graph.add_edge("busca", END)

# Ativa memória com checkpoint em RAM
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# Loop interativo
print("🤖 Magda Assistente com Memória pronta! (digite 'sair' para encerrar)\n")

thread_id = "1"  # ID da conversa

while True:
    entrada = input("Você: ")
    if entrada.strip().lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando a conversa. Até logo!")
        break

    mensagens = [HumanMessage(content=entrada)]
    saida = app.invoke({"messages": mensagens}, config={"configurable": {"thread_id": thread_id}})
    print(f"Magda: {saida['messages'][-1].content}\n")
