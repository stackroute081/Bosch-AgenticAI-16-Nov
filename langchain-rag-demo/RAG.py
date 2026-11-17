from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from main import vector_store
from dotenv import load_dotenv

load_dotenv()

# ------------------Retrieval Process--------------
# Step 1. Create an instance o retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


# Step 2. Augmentation
prompt = PromptTemplate(
    template="""
     You are a helpful AI assistant. Answer the question using ONLY the context below
    Context:
    {context}
    Question:
    {question}
    """
)

# Step 3. Initializing LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

# Step 4. Create a retrieval pipeline
chain = (RunnableParallel(context=retriever,
         question=RunnablePassthrough())) | prompt | llm | StrOutputParser()

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    answer = chain.invoke(user_input)
    print(f"AI: {answer}")
