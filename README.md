# ⚽ Football_Bot – Telegram Bot for Football Statistics Search

Football_Bot is a Telegram bot that allows you to search for information about football players, their statistics, teams, and leagues using the API-Football.

Link to the Telegram bot: [https://t.me/pokinokBot](https://t.me/pokinokBot)

## 🚀 Features

- 🔎 **Player Search** – Search by name with key information displayed.
- 📊 **Player Statistics** – Data about matches, goals, and assists for a season or throughout the player's career.
- 🏆 **League Information** – Name, country, and logo.
- 🏟️ **Team Data** – Name, country, foundation year, and stadium.
- 🆘 **Help Commands** – Information about the bot’s features.

## 📂 Project Structure

```plaintext
Football_Bot/
│── config_data/         # Configuration files
│   ├── config.py        # API and bot settings
│── handlers/            # Command handlers
│   ├── custom_handlers/ # Custom handlers
│   ├── default_handlers/# Basic commands (/start, /help)
│── utils/               # Utility modules
│   ├── api_requests.py  # API-Football requests
│── loader.py            # Bot initialization
│── main.py              # Main entry file
│── .env                 # Environment variables (API keys, etc.)
