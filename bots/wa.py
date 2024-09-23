import requests
from autogen import Agent

API_KEY = 'your_valid_api_key'  # Replace with your actual OpenWeatherMap API key

class WeatherAgent(Agent):
    def __init__(self, agent_name, api_key):
        super().__init__()
        self.agent_name = agent_name
        self.api_key = api_key

    def get_forecast_data(self, location):
        BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
        
        # Parameters for the weather API request
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"  # For Celsius; use "imperial" for Fahrenheit
        }

        try:
            # Make the request to the forecast API using params argument
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            # Print the raw response for debugging
            print("Raw API Response:", data)

            # Check for successful response
            if response.status_code == 200:
                forecast_list = data['list']
                
                # Get the forecast for the next 12 hours (usually in 3-hour intervals)
                forecast_data = []
                for forecast in forecast_list[:4]:  # Get 4 periods (3-hour interval * 4 = 12 hours)
                    forecast_data.append({
                        'timestamp': forecast['dt_txt'],
                        'description': forecast['weather'][0]['description'],
                        'temperature': forecast['main']['temp'],
                        'humidity': forecast['main']['humidity']
                    })

                return {
                    'location': data['city']['name'],
                    'country': data['city']['country'],
                    'forecasts': forecast_data
                }
            else:
                return f"Error: {data.get('message', 'City not found or unable to fetch data')}"

        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def extract_location(self, message):
        # Remove unnecessary words from the message (like "forecast", "next 12 hours")
        exclude_terms = ["forecast", "next", "hours"]
        words = message.split()
        location = ' '.join([word for word in words if word.lower() not in exclude_terms])

        # Handle cases where location may need a country code, e.g., "London, GB"
        if location.lower() == "london":
            location += ",GB"  # Specify UK for London

        return location.strip()

    def run(self, message):
        # Extract the location from the message
        location = self.extract_location(message)

        if not location:
            return "Please specify a location for the weather forecast."

        # Fetch the forecast data
        forecast_data = self.get_forecast_data(location)

        if isinstance(forecast_data, dict):
            response = f"Weather forecast for {forecast_data['location']}, {forecast_data['country']} for the next 12 hours:\n"
            for forecast in forecast_data['forecasts']:
                response += (f"At {forecast['timestamp']}:\n"
                             f"- Description: {forecast['description']}\n"
                             f"- Temperature: {forecast['temperature']}°C\n"
                             f"- Humidity: {forecast['humidity']}%\n\n")
            print(response)
            return response
        else:
            # Handle errors (e.g., city not found)
            print(forecast_data)
            return forecast_data
