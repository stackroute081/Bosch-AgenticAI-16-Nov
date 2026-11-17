from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
import resend
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)


class Feedback(BaseModel):
    participant_name: str = Field(description="Name of the participant")
    sentiment: Literal["positive", "negative"] = Field(
        description="Sentiment of the overall feedback")
    highlights: list[str] = Field(
        description="List of highlights of the training program")
    lowlights: list[str] = Field(
        description="List of lowlights of the training program")
    rating: str = Field(description="Rating of the overall training program")
    email_address: str = Field(description="Email address of the participant")


class FeedbackState(TypedDict):
    feedback: str
    participant_name: str
    email_address: str
    sentiment: str
    rating: str
    email: str
    status: str


def AnalyzeFeedback(state: FeedbackState) -> FeedbackState:
    structured_model = llm.with_structured_output(Feedback)
    response = structured_model.invoke(state['feedback'])
    return {
        "participant_name": response.participant_name,
        "email_address": response.email_address,
        "sentiment": response.sentiment,
        "rating": response.rating,
    }


def GeneratePositiveEmail(state: FeedbackState) -> FeedbackState:
    response = llm.invoke(
        f"Write a thank you email to the participant for giving positive feedback about the training program. Email is from 'Training Team'. Use HTML format and make it elegant and professional. Participant name: {state['participant_name']}")
    print(response.text)
    return {'email': response.text}


def GenerateNegativeEmail(state: FeedbackState) -> FeedbackState:
    response = llm.invoke(
        f"Write an apology email to the participant for giving negative feedback about the training program. Email is from 'Training Team'. Use HTML format and make it elegant and professional. Participant name: {state['participant_name']}.")
    print(response.text)
    return {"email": response.text}


def CheckCondition(state: FeedbackState) -> Literal["GeneratePositiveEmail", "GenerateNegativeEmail"]:
    if state['sentiment'] == "positive":
        return "GeneratePositiveEmail"
    return "GenerateNegativeEmail"


def SendEmail(state: FeedbackState) -> FeedbackState:
    decision = interrupt({
        "question": "Do you want to send this email?"
    })
    if decision.lower() != "yes":
        return {"status": "Email Cancelled"}
    resend.api_key = os.getenv("RESEND_API_KEY")
    params: resend.Emails.SendParams = {
        "from": "training@resend.dev",
        "to": state['email_address'],
        "subject": "Reply from Training Manager",
        "html": state['email']
    }
    resend.Emails.send(params)
    return {"status": "Email Sent"}


graph = StateGraph(FeedbackState)
graph.add_node('AnalyzeFeedback', AnalyzeFeedback)
graph.add_node('GeneratePositiveEmail', GeneratePositiveEmail)
graph.add_node('GenerateNegativeEmail', GenerateNegativeEmail)
graph.add_node("SendEmail", SendEmail)

graph.add_edge(START, 'AnalyzeFeedback')
graph.add_conditional_edges('AnalyzeFeedback', CheckCondition)
graph.add_edge('GeneratePositiveEmail', 'SendEmail')
graph.add_edge('GenerateNegativeEmail', 'SendEmail')
graph.add_edge('SendEmail', END)

workflow = graph.compile(checkpointer=InMemorySaver())

image = workflow.get_graph().draw_mermaid_png()
with open("FeedbackWorkflow.png", mode="wb") as f:
    f.write(image)

response = workflow.invoke({'feedback': "The Java Fullstack training program did not meet expectations. Although it covered key technologies like Core Java, Spring Boot, Hibernate, and Angular, several sections were rushed—especially Spring Boot and Angular—leaving little time for hands-on practice. The lack of dedicated sessions on debugging and code optimization further reduced the program’s effectiveness. While the trainer was knowledgeable, the pace and structure limited meaningful learning and real-world application. Overall, the program requires better pacing and more practical focus. I would rate it 2 out of 5. Feedback given by Dhiraj Kumar. Email address - dhiraj2001@gmail.com"}, config={"configurable": {"thread_id": "thread1"}})

if "__interrupt__" in response:
    payload = response["__interrupt__"][0].value
    user_input = input(payload["question"]+" yes/no: ")
    result = workflow.invoke(Command(resume=user_input), config={
                             "configurable": {"thread_id": "thread1"}})
    print(result['status'])
