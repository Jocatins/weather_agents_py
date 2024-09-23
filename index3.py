import requests
from autogen import Agent  # Assuming autogen's Agent class is available

# Define the custom LLM handler to interact with the local LM server
class CustomLLM:
    def __init__(self, server_url):
        self.server_url = server_url

    def chat_completion(self, prompt):
        try:
            # Send POST request to the /v1/chat/completions endpoint
            response = requests.post(
                f'{self.server_url}/v1/chat/completions',
                json={
                    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",  # Replace with the actual model name
                    'messages': [{'role': 'user', 'content': prompt}]
                }
            )
            response_json = response.json()

            # Log the response for debugging purposes
            print("Response JSON:", response_json)

            # Check if 'choices' key exists in the response
            if 'choices' in response_json:
                return response_json['choices'][0]['message']['content']
            else:
                # Handle the case where 'choices' is not in the response
                return f"Error: Unexpected response structure: {response_json}"

        except Exception as e:
            return f"Exception occurred: {str(e)}"

# Agent class that uses the Autogen framework
class CustomAgent(Agent):
    def __init__(self, agent_name, llm):
        super().__init__()
        self.agent_name = agent_name  # Use a different attribute name
        self.llm = llm

    def run(self, message):
        response = self.llm.chat_completion(message)
        print(f"{self.agent_name} received: {response}")
        return response

# Initialize the local LLM connection
lm_server_url = "http://localhost:1234"  # LM Studio server URL
local_llm = CustomLLM(lm_server_url)

# Create two agents using Autogen framework and the custom LLM
agent_one = CustomAgent(agent_name="Agent One", llm=local_llm)
agent_two = CustomAgent(agent_name="Agent Two", llm=local_llm)

# Simulate the communication between the two agents
message = "Hello, Agent Two!"
for i in range(5):
    print(f"Round {i+1}:")
    response = agent_two.run(f"Agent One says: {message}")
    message = agent_one.run(f"Agent Two says: {response}")
