from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001"
)

def ask_ai(question, context="", history=None):

    prompt = f"""
    You are an AI assistant.

    Previous Conversation:
    {history}

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - Use context if available
    - Be accurate and concise
    """

    response = llm.invoke(prompt)
    return response.content