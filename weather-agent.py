import requests

# OpenWeatherMap API setup
API_KEY = 'ba430379809d45632fbe4e51200ac5f8'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_real_weather_forecast(location):
    # Create the complete URL for the API request
    url = BASE_URL + "q=" + location + "&appid=" + API_KEY + "&units=metric"

    # Send a request to the OpenWeatherMap API
    response = requests.get(url)

    # If the response is valid (status code 200)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]['description']
        temp = main['temp']
        humidity = main['humidity']
        forecast = f"The weather in {location} is {weather} with a temperature of {temp}°C and humidity of {humidity}%."
        return forecast
    else:
        return f"Error fetching weather data for {location}."

# Updated NicoAgent to use the real weather API
class NicoAgent:
    def __init__(self, name):
        self.name = name

    def provide_weather_forecast(self, location):
        return get_real_weather_forecast(location)

# Function to ask the user for input
def ask_for_weather():
    location = input("Enter the location for the weather forecast: ")

    # Nico gives a real weather forecast
    forecast = nico.provide_weather_forecast(location)
    print(f"\nNico (Real Weather Forecast): {forecast}")

# Setting up the agent
nico = NicoAgent("Nico")

# Initiating the conversation by asking for user input
ask_for_weather()
