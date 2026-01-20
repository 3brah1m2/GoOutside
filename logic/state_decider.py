import os
from dotenv import load_dotenv
from groq import Groq
from logic.weather_data_extractor import WeatherDataExtractor
load_dotenv()

class StateDecider:
    def __init__(self):
        self.data = WeatherDataExtractor()
        self.pm25 = self.data.get_pm25()
        self.current_weather = self.data.get_current_weather()
        self.PROMPT = f"""
        Classify outdoor safety as one of: SAFE, CAUTION, UNSAFE.

        Rules:
        - Use only the input data.
        - Output exactly TWO lines.
        - Line 1: the state (SAFE, CAUTION, or UNSAFE).
        - Line 2: a single short explanation.
        - No extra text.
        - When unsure, choose the safer option.
        - Health > convenience.

        Input:
        "temp": {self.current_weather['temperature_2m']},
        "feels_like": {self.current_weather['apparent_temperature']},
        "rain": {self.current_weather['precipitation']},
        "code": {self.current_weather['weather_code']},
        "wind": {self.current_weather['wind_speed_10m']},
        "gusts": {self.current_weather['wind_gusts_10m']},
        "pm25": {self.pm25}

        Guidelines:
        - PM2.5 > 35 = risk
        - PM2.5 > 55 = hazardous
        - Strong wind, rain, or bad weather code increase risk
        """

    def check_weather(self):
        client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{self.PROMPT}",
                }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0
        )

        return chat_completion.choices[0].message.content