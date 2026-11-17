from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)


class ChatBotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def ChatbotNode(state: ChatBotState) -> ChatBotState:
    result = llm.invoke(state['messages'])
    return {'messages': [result]}


graph = StateGraph(ChatBotState)
graph.add_node('ChatbotNode', ChatbotNode)
graph.add_edge(START, 'ChatbotNode')
graph.add_edge('ChatbotNode', END)
workflow = graph.compile(checkpointer=InMemorySaver())

# image = workflow.get_graph().draw_mermaid_png()
# with open("chatbot_graph.png", mode="wb") as f:
#     f.write(image)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = workflow.invoke({'messages': HumanMessage(content=user_input)}, config={
                               "configurable": {"thread_id": "thread1"}})
    print(f"AI: {response['messages'][-1].text}")
