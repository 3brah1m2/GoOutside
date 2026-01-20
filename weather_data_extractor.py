from openaq import OpenAQ
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class WeatherDataExtractor:
    def __init__(self):
        pass

    def get_pm25(self):
        client = OpenAQ(api_key=os.getenv('AQ_API_KEY'))
        data = client.locations.latest(8156)
        diction = data.dict()
        client.close()
        return diction['results'][0]['value']

    def get_current_weather(self):
        url = os.getenv("OM_API_KEY")
        response = requests.get(url)
        data = response.json()
        return data['current']
    