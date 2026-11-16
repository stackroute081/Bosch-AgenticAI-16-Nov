from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

template = PromptTemplate(
    template="""
    You are a professional travel planner. Based on the user's profile, create a personalized traval itinerary. Include activities, must-see attractions, suggested local food, transportation tips, cultural do's and dont's and a basic packing checklist.
User Info:
- Name: {username}
- Destination: {destination}
- Travel Date: {start_date} to {end_date}
- Budget: {budget}
- Interest: {interests}
- Travel Style: {travel_style}
- Dietary Preferences: {dietary_preferences}

Ensure the plan fits the user's budget and travel style. Highlight one unique or offbeat experience they shouldn't miss. Keep the tone friendly and informative.
    """, input_variables=["username", "destination", "start_date", "end_date", "budget", "interests", "travel_style", "dietary_preferences"])

# prompt = template.invoke({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date': '25-01-2026', 'end_date': '30-01-2026',
#                          'interests': 'Adventure', 'travel_style': 'Solo', 'dietary_preferences': 'Non-Vegetarian', 'budget': '100000'})

# response = model.invoke(prompt)

chain = template | model | StrOutputParser()  # LCEL

# print(chain.invoke({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date': '25-01-2026', 'end_date': '30-01-2026',
#                     'interests': 'Adventure', 'travel_style': 'Solo', 'dietary_preferences': 'Non-Vegetarian', 'budget': '100000'}))

for chunk in chain.stream({'username': 'Dhiraj', 'destination': 'Singapore', 'start_date': '25-01-2026', 'end_date': '30-01-2026',
                           'interests': 'Adventure', 'travel_style': 'Solo', 'dietary_preferences': 'Non-Vegetarian', 'budget': '100000'}):
    print(chunk, end="", flush=True)
