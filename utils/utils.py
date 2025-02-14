from collections import deque

from telebot.types import BotCommand, Message
from loader import bot

HISTORY_FILE = "search_history.json"


def set_bot_command():

    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Вывести справку"),
        BotCommand("search_by_name", "Поиск игрока по имени"),
        BotCommand("stats", "Статистика игрока"),
        BotCommand("league", "Поиск лиги"),
        BotCommand("team", "Поиск команды"),
        BotCommand("history", "История поиска")
    ]
    bot.set_my_commands(commands)


search_history = {}


def save_search(user_id, command,query):
    user_id = str(user_id)

    if user_id not in search_history:
        search_history[user_id] = deque(maxlen=5)
    search_history[user_id].append(f"{command}: {query}")


def get_user_history(user_id):
    """Get last 5 searches of a user."""
    user_id = str(user_id)
    return list(search_history.get(user_id, []))




@bot.message_handler(commands=["history"])
def show_history(message):
    user_id = message.chat.id
    history = get_user_history(user_id)

    if history:
        history_text = "\n".join(history)
        bot.send_message(message.chat.id, f"Ваши последние 5 запросов:\n{history_text}")
    else:
        bot.send_message(message.chat.id, "История поиска пуста.")

