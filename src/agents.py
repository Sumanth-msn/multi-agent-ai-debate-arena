import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,  # slight creativity for debate style
        max_retries=2,
    )


def run_for_agent(topic: str, search_results: str) -> str:
    from src.prompts import FOR_AGENT_PROMPT

    llm = get_llm()
    prompt = FOR_AGENT_PROMPT.format(topic=topic)
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(
            content=f"Here are some web search results to help:\n{search_results}\n\nNow make your argument FOR: {topic}"
        ),
    ]
    response = llm.invoke(messages)
    return response.content


def run_against_agent(topic: str, search_results: str) -> str:
    from src.prompts import AGAINST_AGENT_PROMPT

    llm = get_llm()
    prompt = AGAINST_AGENT_PROMPT.format(topic=topic)
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(
            content=f"Here are some web search results to help:\n{search_results}\n\nNow make your argument AGAINST: {topic}"
        ),
    ]
    response = llm.invoke(messages)
    return response.content


def run_judge_agent(topic: str, for_arg: str, against_arg: str) -> str:
    from src.prompts import JUDGE_PROMPT

    llm = get_llm()
    prompt = JUDGE_PROMPT.format(
        topic=topic, for_argument=for_arg, against_argument=against_arg
    )
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content
