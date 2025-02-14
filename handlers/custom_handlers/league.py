import json
from telebot.types import Message
from loader import bot
from utils.api_requests import fetch_api_data
from config_data.config import url_leagues
from utils.utils import save_search

@bot.message_handler(commands=["league"])
def league_by_name(message: Message):
    bot.send_message(message.chat.id, "Введите название лиги:")
    bot.register_next_step_handler(message, process_league_search)

def process_league_search(message: Message):
    league_name = message.text.strip()
    leagues_data = fetch_api_data(url_leagues)

    if "response" not in leagues_data:
        bot.send_message(message.chat.id, "Ошибка при загрузке данных лиг.")
        return

    league_info = next((league for league in leagues_data["response"]
                        if league["league"]["name"].lower() == league_name.lower()), None)

    if not league_info:
        bot.send_message(message.chat.id, f"Лига '{league_name}' не найдена.")
        return

    league_details = (
        f"Название лиги: {league_info['league']['name']}\n"
        f"Страна: {league_info['country']['name']}\n"
        f"Логотип: {league_info['league']['logo']}\n"
        f"Флаг: {league_info['country']['flag']}"
    )

    save_search(message.chat.id,"Лига:",league_info['league']['name'])

    bot.send_message(message.chat.id,league_details)

