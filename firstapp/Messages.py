from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

conversation_history = [
    SystemMessage(content="You are a helpful AI assistant who gives answers with a bit of humour. Add emojis to make your responses looks good. Use professional tone to answer queries. You are only allowed to give answers about python. If any other questions are asked politely reject.")
]
while True:
    user_input = input("You: ")
    conversation_history.append(HumanMessage(content=user_input))
    if user_input.lower() == "exit":
        break
    response = model.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.text))
    print(f"AI: {response.text}")

print(conversation_history)
