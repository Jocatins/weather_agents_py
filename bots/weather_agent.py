import aiohttp
from autogen import Agent
import re  

API_KEY = '5ca83a42b2e769eff69979d4ae46a433'  

class WeatherAgent(Agent):
    def __init__(self, agent_name, api_key):
        super().__init__()
        self.agent_name = agent_name
        self.api_key = api_key
        self.location = None
        self.time_period = None

    def ask_for_location(self):
        return "Please provide the location for the weather forecast."

    def ask_for_time_period(self):
        return "Please specify the time period (e.g., 'next 12 hours', 'next 24 hours')."

    def extract_location(self, message):   
        match = re.search(r'for\s+([a-zA-Z\s]+)', message)
        if match:
            location = match.group(1).strip()
            return location
        else:
            return message.strip()  

    def format_location(self, location):
        """Format the location to ensure it's properly passed to the API."""
        location = location.strip()
        if ',' in location:
            parts = location.split(',')
            location = parts[0].strip() + ',' + parts[1].strip()  # Ensure no spaces around commas
        return location

    async def get_forecast_data(self, location):
        BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
        formatted_location = self.format_location(location)       
        # print(f"Formatted Location: {formatted_location}")
        
        params = {
            "q": formatted_location,
            "appid": self.api_key,
            "units": "metric"  
        }
        # print(f"Request URL: {BASE_URL} with params {params}")

        async with aiohttp.ClientSession() as session:
            try:
                # Make the request to the forecast API asynchronously
                async with session.get(BASE_URL, params=params) as response:
                    data = await response.json()

                    # print("Raw API Response:", data)

                    if response.status == 200:
                        # Get the first forecast (usually 3 hours ahead)
                        forecast = data['list'][0]
                        description = forecast['weather'][0]['description']
                        temp = forecast['main']['temp']
                        return f"The weather forecast for {location}: is {description}, and {temp}°C"
                    else:
                        return f"Error: {data.get('message', 'City not found or unable to fetch data')}"
            except Exception as e:
                return f"Exception occurred: {str(e)}"

    async def run(self, message):        
        if not self.location:
            self.location = self.extract_location(message)
            return self.ask_for_time_period()  
        
        if not self.time_period:
            self.time_period = message.strip()
            
            forecast = await self.get_forecast_data(self.location)

            self.location = None
            self.time_period = None
            return forecast

        self.location = None
        self.time_period = None
        return self.ask_for_location()
