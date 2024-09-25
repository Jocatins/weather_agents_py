import asyncio
from custom_llm import CustomLLM
from general_agent import GeneralAgent
from weather_agent import WeatherAgent

# Initialize variables
API_KEY = ''
lm_server_url = "http://localhost:1234" 
local_llm = CustomLLM(lm_server_url)

# Create the  agent
weather_agent = WeatherAgent(agent_name="WeatherAgent", api_key=API_KEY)
general_agent = GeneralAgent(agent_name="GeneralAgent", llm=local_llm, api_key=API_KEY)

async def start_chat():
    # print("Start chatting with the General Agent! Type 'exit' to stop the chat.\n")
    
    # general_agent = GeneralAgent(agent_name="GeneralAgent", llm=local_llm, api_key=API_KEY)

    while True:
        user_input = input("Enter text: ")

        if user_input.lower() == 'exit':
            print("Chat ended.")
            break

        # Keep looping until a complete response (weather forecast) is received
        while True:
            response = await general_agent.run(user_input)
            
            # If the response is asking for more information, prompt the user
            print(response)
            
            if "forecast for" in response or "Error" in response:
                break
            
            user_input = input("Enter time range: ")

# Begin the chat
if __name__ == "__main__":
     asyncio.run(start_chat())
