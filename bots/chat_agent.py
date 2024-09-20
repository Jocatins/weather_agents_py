from autogen import Agent

class ChatAgent(Agent):
    def __init__(self, agent_name, llm):
        super().__init__()
        self.agent_name = agent_name
        self.llm = llm

    def run(self, message):
        response = self.llm.chat_completion(message)
        print(f"{self.agent_name} received: {response}")
        return response
