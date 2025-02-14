from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    welcome_text = (
        "Manen debila\n"
        "👋 <b>Привет! Я футбольный бот!</b>\n\n"
        "⚽ Я могу искать игроков, их статистику, команды и лиги.\n"
    )

    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")
