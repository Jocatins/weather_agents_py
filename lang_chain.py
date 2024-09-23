import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from typing import Optional, List

# Define a custom LLM class for interacting with your local LM Studio API
class LMStudioLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        API_URL = "http://localhost:1234/v1/completions"
        payload = {
            "prompt": prompt,
            "max_tokens": 100,
        }
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "").strip()
        else:
            return f"Error: {response.status_code} - {response.text}"

    @property
    def _identifying_params(self):
        return {}

    @property
    def _llm_type(self):
        return "lmstudio"

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["location", "period"],
    template="Provide a weather forecast for {location} for the {period}."
)

# Create the chain using Langchain and your custom LLM
llm = LMStudioLLM()
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# Function to ask the user for a weather forecast and return the model's response
def ask_for_weather():
    location = input("Enter the location for the weather forecast: ")
    period = input("Enter the time period (e.g., 'next 24 hours', 'next week'): ")
    
    # Get the forecast from the chain
    forecast = llm_chain.run({"location": location, "period": period})
    print(f"Weather Forecast: {forecast}")

# Ask the user for weather input and display the forecast
ask_for_weather()
