from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st

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

st.header("Travel Planner")
username = st.text_input("Name")
destination = st.text_input("Destination")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
budget = st.slider("Select Budget", 10000, 1000000)
interest = st.multiselect(
    "Interests", ["Adventure", "Beaches", "Nature", "Shopping"])
travel_style = st.selectbox(
    "Travel Style", ["Luxury", "Solo", "Group", "Family"])
dietary_preferences = st.selectbox(
    "Dietary Preferences", ["Vegetarian", "Non-Vegetarian", "Vegan"])

if st.button("Submit"):
    chain = template | model | StrOutputParser()  # LCEL

    st.write_stream(chain.stream({'username': username, 'destination': destination, 'start_date': start_date, 'end_date': end_date,
                    'interests': interest, 'travel_style': travel_style, 'dietary_preferences': dietary_preferences, 'budget': budget}))
