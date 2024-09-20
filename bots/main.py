from custom_llm import CustomLLM
from general_agent import GeneralAgent
# from weather_agent import WeatherAgent

# Initialize the local LLM connection
API_KEY = 'ba430379809d45632fbe4e51200ac5f8'
lm_server_url = "http://localhost:1234" 
local_llm = CustomLLM(lm_server_url)

# Create the  agent
# weather_agent = WeatherAgent(agent_name="WeatherAgent", api_key=API_KEY)
general_agent = GeneralAgent(agent_name="GeneralAgent", llm=local_llm)

# Start an interactive chat with the user
def start_chat():
    print("Start chatting with the General Agent! Type 'exit' to stop the chat.\n")
    
    while True:
        user_input = input("Enter text: ")
        
        if user_input.lower() == 'exit':
            print("Chat ended.")
            break

        # Pass the user's input to the general agent
        general_agent.run(user_input)

# Begin the chat
start_chat()
