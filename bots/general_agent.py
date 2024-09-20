from autogen import Agent
from weather_agent import WeatherAgent
from chat_agent import ChatAgent

class GeneralAgent(Agent):
    def __init__(self, agent_name, llm):
        super().__init__()
        self.agent_name = agent_name
        self.llm = llm
        self.weather_agent = WeatherAgent(agent_name="WeatherAgent", llm=llm)
        self.chat_agent = ChatAgent(agent_name="ChatAgent", llm=llm)

    def is_weather_query(self, message):
        weather_terms = ["weather", "forecast", "temperature", "rain", "sun", "humidity"]
        return any(term in message.lower() for term in weather_terms)

    def run(self, message):
        if self.is_weather_query(message):
            print("Delegating to WeatherAgent")
            return self.weather_agent.run(message)
        else:
            print("Delegating to ChatAgent")
            return self.chat_agent.run(message)
