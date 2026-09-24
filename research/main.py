import os
import certifi
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI 
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
import requests

from langchain.agents import create_react_agent,AgentExecutor

#Load environment variables from .env file

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv() 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("Tavily_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

search_tool = TavilySearchResults(api_key=TAVILY_API_KEY,max_results=2)

@tool
def get_weather_data(city:str):
   """Fetch current weather information for a city """

   url =(
    f"https://api.weatherstack.com/current?"
    f"access_key={WEATHERSTACK_API_KEY}&query={city}"
   )
   response = requests.get(url)
   data=response.json() 

   if "current" not in data:
       return f"""Could not retrieve weather data for {city}.
       Please check the city name and try again."""
   return (
        f"City:{city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%\n   "
    )

result=search_tool.invoke("what is the latest news on Jev?")
result

# LLM initialization
llm = ChatOpenAI(
    temperature=0,
    model="google/gemini-2.5-flash-lite",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=4000
)

respoonse =llm.invoke("what is leap year?")
respoonse

# Prompt 
prompt=hub.pull("hwchase17/react")
prompt

# tools
tools=[search_tool,get_weather_data]

# Create the agent
agent = create_react_agent(llm=llm, tools=tools,prompt=prompt)

# agent execution
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run

response = agent_executor.invoke({
    "input":"Find the capital of India and "
    "then get the current weather in that city." 
})

print(response['output']) 


