from utils.utils import set_bot_command
from loader import bot
from handlers.custom_handlers import league, player_statistics, search_name, team
from handlers.default_handlers import start, help, echo


if __name__ == "__main__":
    bot.polling()