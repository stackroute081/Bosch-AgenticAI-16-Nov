from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)

template = PromptTemplate(
    template="Write an article about {topic} in {no_of_words} words", input_variables=["topic", "no_of_words"])
prompt = template.invoke({"topic": "AI", "no_of_words": "100"})
print(prompt)
response = model.invoke(prompt)
print(response.text)
