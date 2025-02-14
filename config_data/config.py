import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    print("BOT_TOKEN is incorrect")

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("API_KEY is incorrect")

url_players = "https://api-football-v1.p.rapidapi.com/v3/players"
url_teams = "https://api-football-v1.p.rapidapi.com/v3/teams"
url_leagues = "https://api-football-v1.p.rapidapi.com/v3/leagues"



