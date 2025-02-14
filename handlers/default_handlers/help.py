from telebot.types import Message, BotCommand
from loader import bot

COMMANDS = [
    BotCommand("start", "Запустить бота"),
    BotCommand("help", "Вывести справку"),
    BotCommand("search_by_name", "Поиск игрока по имени"),
    BotCommand("stats", "Статистика игрока"),
    BotCommand("league", "Поиск лиги"),
    BotCommand("team", "Поиск команды"),
]

bot.set_my_commands(COMMANDS)

@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{cmd.command} - {cmd.description}" for cmd in COMMANDS]
    bot.reply_to(message, "\n".join(text))
