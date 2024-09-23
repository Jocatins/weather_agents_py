import requests
from autogen import Agent  

# Define the custom LLM handler to interact with the local LM server
class CustomLLM:
    def __init__(self, server_url):
        self.server_url = server_url

    def chat_completion(self, prompt):
        try:
        
            response = requests.post(
                f'{self.server_url}/v1/chat/completions',
                json={
                    "model": "gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",  
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

# Create an agent for the user using Autogen framework and the custom LLM
user_agent = CustomAgent(agent_name="User", llm=local_llm)
model_agent = CustomAgent(agent_name="Local Model", llm=local_llm)

# Start an interactive chat with the user
def start_chat():
    print("Start chatting with the Local Model! Type 'exit' to stop the chat.\n")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Chat ended.")
            break

        # Pass the user's input to the model and get a response
        model_response = model_agent.run(user_input)
        print(f"Local Model: {model_response}")

# Begin the chat
start_chat()
