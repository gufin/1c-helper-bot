# Secound hackathon Yandex workshops. Telegram bot implementation.
🛠 The Telegram bot allows you to connect to standard 1c configurations (UT, ERP, UNF) and receive data on employee stock balances and vacation balances. The bot can also perform several functions for the support team:

- Create a delivery file
- Update a specific database
- Run cost calculation

# 🚀 Project installation

Clone the repository

```sh
git clone git@github.com:gufin/1c-helper-bot.git
```

Install and activate the virtual environment

```sh
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
```
Install dependencies from requirements.txt file:
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Run the bot
```sh
python helper_bot.py
```
## :shipit: In the plans
- Make it possible to work with the database
- Make the code look good
- Make universal extension for 1C
- Write a tests :grinning:

