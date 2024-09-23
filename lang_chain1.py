import os
import asyncio
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool

# Setting environment variables
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"  # Replace with a real key

# --- WEATHER AGENTS ---

# Tool 1: Weather API Tool (interacts with the weather API)
class WeatherAPITool(BaseTool):
    """Tool to fetch weather information."""

    name = "weather_api_tool"
    description = "Fetches real-time weather information."

    async def _run(self, location: str):
        """Run the weather tool."""
        try:
            response = await get_real_time_weather(location)  # Replace with your actual weather API call
            return response
        except Exception as e:
            print(f"Error in Weather API Tool: {e}")
            return None

    def _run_sync(self, location: str):
        return asyncio.run(self._run(location))


weather_api_tool = WeatherAPITool()

# Tool 2: Weather Feedback Tool (provides feedback based on the weather API response)
async def weather_feedback_tool(location):
    """Process the response from the Weather API tool and provide feedback."""
    weather_data = await weather_api_tool._run(location)
    if weather_data:
        return f"Weather Forecast for {location}: {weather_data}"
    else:
        return "Unable to fetch the weather data at the moment."


# --- GENERAL CHAT AGENTS ---

# Tool 3: Chat Tool (interacts with the LM server using LangChain's LLMChain)
llm = OpenAI(temperature=0.7)  # Initialize OpenAI LLM
chat_prompt = PromptTemplate(input_variables=["query"], template="You are a helpful assistant. {query}")
chat_llm_chain = LLMChain(llm=llm, prompt=chat_prompt)

# Tool 4: Chat Feedback Tool (provides feedback based on the LM response)
async def chat_feedback_tool(query):
    """Process the response from the Chat tool and provide feedback."""
    try:
        response = await chat_llm_chain.apredict(query)
        return f"General Query Response: {response}"
    except Exception as e:
        print("Error in Chat Feedback Tool:")
        return "Unable to process the query at the moment."


# --- MANAGER AGENT --- (Delegates tasks between weather and chat tools)

async def manager_agent(query, location=None):
    """Manager agent to delegate between weather forecast and general chat tools."""
    if "weather" in query.lower() or location:
        # If query relates to weather, delegate to the weather tools
        weather_response = await weather_feedback_tool(location)
        print(weather_response)
    else:
        # Otherwise, delegate to the general chat tools
        chat_response = await chat_feedback_tool(query)
        print(chat_response)


# --- MAIN FUNCTION TO INTERACT WITH USER ---

async def interact_with_user():
    """Function to interact with the user and simulate a conversation."""
    query = input("Enter your query: ")
    location = None

    # If the query is related to weather, ask for location
    if "weather" in query.lower():
        location = input("Enter the location for the weather forecast: ")

    # Delegate task to the manager agent
    await manager_agent(query, location)


if __name__ == "__main__":
    # Run the interaction asynchronously
    asyncio.run(interact_with_user())
