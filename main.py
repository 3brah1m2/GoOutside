import requests
import os
from dotenv import load_dotenv
from logic.state_decider import StateDecider

load_dotenv()

def notify_discord(message):
    webhook = os.getenv("DISCORD_WEBHOOK")
    if not webhook:
        return
    requests.post(
        webhook,
        json={"content": message}
    )

decider = StateDecider().check_weather()
notify_discord(f'**Weather State**: \n{decider}')