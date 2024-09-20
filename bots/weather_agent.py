from autogen import Agent

class WeatherAgent(Agent):
    def __init__(self, agent_name, llm):
        super().__init__()
        self.agent_name = agent_name
        self.llm = llm

    def run(self, message):
        # Placeholder for the actual weather logic
        response = f"{self.agent_name}: Here is the weather forecast for {message}"
        print(response)
        return response
