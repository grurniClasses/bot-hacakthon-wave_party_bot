# Party Wave Bot

## The Team

- Participant 1 - Sara
- Participant 2 - Ayala
- Participant 3 - Igor

## About this bot

🏄‍♂️🤙 Welcome to PartyWave, your one-stop solution for all your beach-related needs! Our app allows you to register to your favorite beach and receive daily forecasts, so you never have to worry about the weather. In addition, you can share beach reports with other users, ensuring that everyone stays up-to-date on the latest conditions. Whether you're a seasoned beach-goer or a newbie, the PartyWave got you covered. Let's hit the waves! 🏄‍♀️🤙

Photos:

(./readme_pics/start1.jpeg)

(./readme_pics/start.jpeg)

(./readme_pics/forecast.jpeg)

(./readme_pics/photoup.jpeg)

## Instructions for Developers

### Prerequisites

- Python 3.10
- Poetry
- pymongo
- python-telegram-bot 13.15
- requests

### Setup

- git clone this repository
- cd into the project directory
- Install dependencies:

      poetry install

- Get an API Token for a bot via the [BotFather](https://telegram.me/BotFather)
- Create a `bot_settings.py` file with your bot token:

      BOT_TOKEN = 'xxxxxxx'

### Running the bot

- Run the bot:

      poetry run python bot.py
