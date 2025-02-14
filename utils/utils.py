from telebot.types import BotCommand
from loader import bot

def set_bot_command():
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Вывести справку"),
        BotCommand("search_by_name", "Поиск игрока по имени"),
        BotCommand("stats", "Статистика игрока"),
        BotCommand("league", "Поиск лиги"),
        BotCommand("team", "Поиск команды"),
    ]
    bot.set_my_commands(commands)