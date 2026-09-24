import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor


# Load environment variables
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("Tavily_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


# Streamlit UI
st.title("🤖 LangChain AI Agent")

st.write("Ask a question and let the agent use Tavily Search and Weather tools.")


# Tavily Search Tool
search_tool = TavilySearchResults(
    api_key=TAVILY_API_KEY,
    max_results=2
)


# Weather Tool
@tool
def get_weather_data(city: str):
    """Fetch current weather information for a city."""

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)
    data = response.json()

    if "current" not in data:
        return f"Could not retrieve weather data for {city}."

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


# Tools
tools = [
    search_tool,
    get_weather_data
]


# LLM
llm = ChatOpenAI(
    temperature=0,
    model="google/gemini-2.5-flash-lite",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=2500
)


# Prompt
prompt = hub.pull("hwchase17/react")


# Create Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


# User Input
user_input = st.text_input(
    "Enter your question:",
    placeholder="Ask anything..."
)


# Run Agent
if st.button("Run Agent"):

    if user_input:

        with st.spinner("Agent is working..."):

            response = agent_executor.invoke({
                "input": user_input
            })

        st.subheader("Result")
        st.write(response["output"])

    else:
        st.warning("Please enter a question.")
        