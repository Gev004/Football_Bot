import json
from telebot.types import Message
from loader import bot
from utils.api_requests import fetch_api_data
from config_data.config import url_teams
from utils.utils import save_search


@bot.message_handler(commands=["team"])
def team_by_name(message: Message):
    bot.send_message(message.chat.id, "Введите название команды:")
    bot.register_next_step_handler(message, process_team_search)

def process_team_search(message: Message):
    team_name = message.text.strip()
    params = {"search": team_name}
    teams_data = fetch_api_data(url_teams, params)
    if "response" not in teams_data or not teams_data["response"]:
        bot.send_message(message.chat.id, f"Команда '{team_name}' не найдена.")
        save_search(message.chat.id, "❌Поиск по команде:",team_name)
        return

    team_info = teams_data["response"][0]
    team_details = (
        f"🏆 Название команды: {team_info['team']['name'].capitalize()}\n"
        f"🌍 Страна: {team_info['team']['country']}\n"
        f"📅 Основана: {team_info['team']['founded']}\n"
        f"🏟️ Стадион: {team_info['venue']['name']}\n"
        f"📍 Город: {team_info['venue']['city']}\n"
        f"👥 Вместимость: {team_info['venue']['capacity']}\n"
        f"🔗 Логотип: {team_info['team']['logo']}\n"
        f"🔗 Фото стадиона: {team_info['venue']['image']}"
    )


    save_search(message.chat.id, "✅Поиск по команде:",team_info['team']['name'])


    bot.send_message(message.chat.id, team_details)

