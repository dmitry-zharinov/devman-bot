import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv
from telegram import Bot


def get_user_reviews(dvmn_token, bot_token, chat_id):
    timestamp = time.time()
    url = 'https://dvmn.org/api/long_polling/'
    while True:
      try:
        response = requests.get(
          url, 
          headers={'Authorization': f'Token {dvmn_token}'},
          params={'timestamp': timestamp},
          timeout=60
        )
        response.raise_for_status()
        reviews = response.json()

        status = reviews.get('status')
        
        if status == 'found':
          timestamp = reviews['last_attempt_timestamp']
        elif status == 'timeout':
          timestamp = reviews['timestamp_to_request']

        pprint(response.text)
        send_bot_message(
          bot_token,
          chat_id,
          'Преподаватель проверил работу!'
        )

      except requests.exceptions.HTTPError as err:
        print(f"Возникла ошибка при выполнении HTTP-запроса:\n{err}")
      except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        continue


def send_bot_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(
      chat_id=chat_id,
      text=message)

if __name__ == '__main__':
  load_dotenv()
  dvmn_token = os.environ["DVMN_TOKEN"]
  bot_token = os.environ["BOT_TOKEN"]
  chat_id = os.environ["CHAT_ID"]
  get_user_reviews(dvmn_token, bot_token, chat_id)


