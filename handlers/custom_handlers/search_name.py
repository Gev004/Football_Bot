from telebot.types import Message
import requests
import datetime
import json
from loader import bot
from config_data.config import API_KEY, url_leagues, url_players
from utils.api_requests import fetch_api_data
from utils.utils import save_search


@bot.message_handler(commands=["search_by_name"])
def start_search_by_name(message: Message):
    bot.send_message(message.chat.id, "Введите имя игрока:")
    bot.register_next_step_handler(message, process_player_search)


def process_player_search(message: Message):
    player_name = message.text.strip()

    fetch_player_info(message,player_name)

def fetch_player_info(message: Message, player_name: str):

    season = str(datetime.datetime.now().year - 1)

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }

    response_leagues = requests.get(url_leagues, headers=headers)
    leagues_data = response_leagues.json()

    if "response" not in leagues_data:
        bot.send_message(message.chat.id, "Ошибка при загрузке данных лиг.")
        return

    play_id = None
    for league in leagues_data["response"]:
        league_id = league["league"]["id"]
        params = {"league": str(league_id), "search": player_name}
        response = requests.get(url_players, headers=headers, params=params)
        player_data = response.json()

        if "response" in player_data and player_data["response"]:
            play_id = player_data["response"][0]["player"]["id"]
            break

    if not play_id:
        bot.send_message(message.chat.id, f"Игрок '{player_name}' не найден в лигах.")
        return

    querystring = {"id": str(play_id), "season": season}
    response = requests.get(url_players, headers=headers, params=querystring)
    final_data = response.json()

    if "response" not in final_data or not final_data["response"]:
        bot.send_message(message.chat.id, "Ошибка: Нет детальных данных о игроке.")
        return

    player_info = final_data["response"][0]["player"]
    statistics = final_data["response"][0]["statistics"][0]

    player_details = (
        f"👤 Имя: {player_name}\n"
        f"🎂 озраст: {player_info['age']}\n"
        f"🌍 Национальность: {player_info['nationality']}\n"
        f"📏 Рост: {player_info.get('height', 'N/A')}\n"
        f"⚖️ Вес: {player_info.get('weight', 'N/A')}\n"
        f"🏆 Лига: {statistics['league']['name']}\n"
        f"⚽ Команда: {statistics['team']['name']}\n"
        f"📍 Позиция: {statistics['games']['position']}\n"
    )

    save_search(message.chat.id, "Поиск по имени",player_name)

    bot.send_message(message.chat.id, player_details)

