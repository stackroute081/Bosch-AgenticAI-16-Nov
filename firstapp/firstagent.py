from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

tavily_tool = TavilySearch(
    max=5,
    topic="general"
)

agent = create_agent(
    model=llm,
    system_prompt="You are a helpful AI assistant who answer user queries. Keep your tone professional. Do not make up things or invent facts. For grounded information use tavily tool to get the latest information from the web. If you are not sure, simply say you don't know.",
    checkpointer=InMemorySaver(),
    tools=[tavily_tool]
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = agent.invoke({
        "messages": {
            "role": "user",
            "content": user_input
        }
    }, config={"configurable": {"thread_id": "1"}})
    print(f"AI: {response["messages"][-1].text}")
