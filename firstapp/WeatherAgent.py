from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
import os
from datetime import date
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)


@tool
def getWeatherData(city: str):
    """
    Get the current weather information from openweathermap based on city name
    """
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "unit": "metric"
    })
    if response.status_code != 200:
        return "Unable to fetch data from API"
    return response.json()


@tool
def getAQI(city: str):
    """
    Get the current air quality index from openweathermap based on city name
    """
    response = requests.get("http://api.openweathermap.org/data/2.5/air_pollution", {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY")
    })
    if response.status_code != 200:
        print(response)
        return "Unable to fetch data from API"

    return response.json()


agent = create_agent(
    model=llm,
    system_prompt=f"You are a helpful AI weather agent who answers queries about the latest weather information or air quality index as of today {date.today()} with a bit of humour. Keep your tone professional while answering the questions. Use emojis while generating response to make your responses looks good. Do not make up things and give only real time information. Always answer with updated information using tools. If you cannot access tools or does not have latest information, simply refuse politely. You only answer queries related to the weather updates. Do not answer any other questions and refuse politely",
    checkpointer=InMemorySaver(),
    tools=[getWeatherData, getAQI]
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
