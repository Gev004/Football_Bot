import datetime
import json
from telebot.types import Message
from loader import bot
from utils.api_requests import fetch_api_data
from config_data.config import url_leagues, url_players
import time

from utils.utils import save_search


@bot.message_handler(commands=["stats"])
def player_stats_command(message: Message):
    bot.send_message(message.chat.id, "Введите имя игрока:")
    bot.register_next_step_handler(message, ask_for_specific_year)

def ask_for_specific_year(message: Message):
    player_name = message.text.strip()
    bot.send_message(message.chat.id, "Вам нужна статистика за конкретный год? (Да/Нет)")
    bot.register_next_step_handler(message, lambda msg: process_year_choice(msg, player_name))

def process_year_choice(message: Message, player_name: str):
    answers_yes = ["yes", "Yes", "այո", "Այո", "Да", "да"]
    answers_no = ["no", "NO", "Ոչ", "ոչ", "Нет", "нет"]

    user_response = message.text.strip()

    if user_response in answers_yes:
        bot.send_message(message.chat.id, "Введите год:")
        bot.register_next_step_handler(message, lambda msg: fetch_player_statistics(msg, player_name, msg.text.strip()))
    elif user_response in answers_no:
        fetch_career_statistics(message, player_name)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите 'Да' или 'Нет'.")
        bot.register_next_step_handler(message, lambda msg: process_year_choice(msg, player_name))

def fetch_player_statistics(message: Message, player_name: str, season: str):
    leagues_data = fetch_api_data(url_leagues)
    if "response" not in leagues_data:
        bot.send_message(message.chat.id, "Ошибка при загрузке данных лиг.")
        return

    player_id = None
    for league in leagues_data["response"]:
        league_id = league["league"]["id"]
        params = {"league": str(league_id), "search": player_name}
        player_data = fetch_api_data(url_players, params)

        if "response" in player_data and player_data["response"]:
            player_id = player_data["response"][0]["player"]["id"]
            break

    if not player_id:
        bot.reply_to(message, f"Игрок '{player_name}' не найден.")
        return

    params = {"id": str(player_id), "season": season}
    final_data = fetch_api_data(url_players, params)

    if "response" not in final_data or not final_data["response"]:
        bot.reply_to(message, "Ошибка: Нет данных о игроке.")
        return

    statistics = final_data["response"][0]["statistics"][0]

    player_stats = (
        f"Игрок:{player_name}\n"
        f"Лига:{statistics["league"]["name"]}\n"
        f"Команда:{statistics["team"]["name"]}\n"
        f"Матчи:{statistics["games"].get("appearences", 0)}\n"
        f"Голы:{statistics["goals"].get("total", 0)}\n"
        f"Ассисты:{statistics["goals"].get("assists", 0)}"
    )

    bot.send_message(message.chat.id,player_stats)

def fetch_career_statistics(message: Message, player_name: str):
    leagues_data = fetch_api_data(url_leagues)
    if "response" not in leagues_data:
        bot.send_message(message.chat.id, "Ошибка при загрузке данных лиг.")
        return

    player_id = None
    for league in leagues_data["response"]:
        league_id = league["league"]["id"]
        params = {"league": str(league_id), "search": player_name}
        player_data = fetch_api_data(url_players, params)

        if "response" in player_data and player_data["response"]:
            player_id = player_data["response"][0]["player"]["id"]
            break

    if not player_id:
        bot.reply_to(message, f"Игрок '{player_name}' не найден.")
        return

    current_year = datetime.datetime.now().year
    total_matches = 0
    total_goals = 0
    total_assists = 0

    for year in range(2000, current_year + 1):  # Checking stats from 2000 onwards
        time.sleep(5)
        params = {"id": str(player_id), "season": str(year)}
        final_data = fetch_api_data(url_players, params)

        if "response" in final_data and final_data["response"]:
            for stat in final_data["response"][0]["statistics"]:
                if isinstance(stat["games"].get("appearences", 0),int) and isinstance(stat["goals"].get("total", 0),int):
                    total_matches += stat["games"].get("appearences", 0)
                    total_goals += stat["goals"].get("total", 0)
                if stat["goals"].get("assists") is not None:
                    total_assists += stat["goals"]["assists"]


    player_info = final_data["response"][0]["player"]

    career_stats = (
        f"Игрок: {player_name}\n"
        f"Возраст: {player_info.get('age')}\n"
        f"Национальность: {player_info.get('nationality')}\n"
        f"Матчи за карьеру: {total_matches}\n"
        f"Голы за карьеру: {total_goals}\n"
        f"Ассисты за карьеру: {total_assists}"
    )

    save_search(message.chat.id,f"Статистика игрока:", player_name)


    bot.send_message(message.chat.id, career_stats)