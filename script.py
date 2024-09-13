import requests

# URL for your local model's API running on LM Studio
API_URL = "http://localhost:1234/v1/completions"

def generate_response_local(prompt, max_length=100):
    payload = {
        "prompt": prompt,
        "max_tokens": max_length,
    }
    
    # Make a POST request to your local LM Studio API
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Updated NicoAgent to provide weather forecast
class NicoAgent:
    def __init__(self, name):
        self.name = name

    def provide_weather_forecast(self, location, period):
        # Create the prompt dynamically based on user input
        prompt = f"Provide a weather forecast for {location} for the {period}."
        response = generate_response_local(prompt)
        return response

# User interaction and getting a forecast from Nico
def ask_for_weather():
    location = input("Enter the location for the weather forecast: ")
    period = input("Enter the time period (e.g., 'next 24 hours', 'next week'): ")

    # Nico gives a weather forecast
    forecast = nico.provide_weather_forecast(location, period)
    print(f"\nNico (Weather Forecast): {forecast}")

# Setting up the agent
nico = NicoAgent("Nico")

# Initiating the conversation by asking for user input
ask_for_weather()
