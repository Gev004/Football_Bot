import requests
from config_data.config import API_KEY

def fetch_api_data(url, params=None):
    """Helper function to request API data"""
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
