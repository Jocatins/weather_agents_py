from autogen import Agent
from weather_agent import WeatherAgent
from chat_agent import ChatAgent

API_KEY = 'ba430379809d45632fbe4e51200ac5f8'

class GeneralAgent(Agent):
    def __init__(self, agent_name, llm, api_key):
        super().__init__()
        self.agent_name = agent_name
        self.llm = llm
        self.weather_agent = WeatherAgent(agent_name="WeatherAgent", api_key=api_key)
        self.chat_agent = ChatAgent(agent_name="ChatAgent", llm=llm)
        self.weather_query_active = False  # Track if weather query is ongoing

    def is_weather_query(self, message):
        weather_terms = ["weather", "forecast", "temperature", "rain", "sun", "humidity"]
        return any(term in message.lower() for term in weather_terms)

    async def run(self, message):
        if self.is_weather_query(message) or self.weather_query_active:
            print("Delegating to WeatherAgent")
            self.weather_query_active = True  # Mark weather query as active
            response = await self.weather_agent.run(message)
            
            # If the forecast is completed, reset the weather query state
            if "forecast for" in response or "Error" in response:
                self.weather_query_active = False

            return response
        else:
            print("Delegating to ChatAgent")
            return self.chat_agent.run(message)
