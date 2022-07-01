import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot


def get_result_message(title, url, is_negative):
    if is_negative:
        result = "⚠️ Необходимо исправить замечания."
    else:
        result = "🚀 Всё хорошо, можно приступать к следующему уроку!"
    return f'Преподаватель проверил работу "[{title}]({url})".\n{result}'


def get_user_reviews(dvmn_token, bot_token, chat_id):
    timestamp = time.time()
    url = "https://dvmn.org/api/long_polling/"
    while True:
        try:
            response = requests.get(
                url,
                headers={"Authorization": f"Token {dvmn_token}"},
                params={"timestamp": timestamp},
                timeout=60,
            )
            response.raise_for_status()
            reviews = response.json()

            status = reviews.get("status")

            if status == "found":
                timestamp = reviews.get("last_attempt_timestamp")
                result = reviews.get("new_attempts")[0]
                message = get_result_message(
                    title=result["lesson_title"],
                    url=result["lesson_url"],
                    is_negative=result["is_negative"],
                )
            elif status == "timeout":
                timestamp = reviews.get("timestamp_to_request")

            send_bot_message(bot_token, chat_id, message)

        except requests.exceptions.HTTPError as err:
            print(f"Возникла ошибка при выполнении HTTP-запроса:\n{err}")
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
            continue


def send_bot_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message, parse_mode="markdown")


if __name__ == "__main__":
    load_dotenv()
    dvmn_token = os.environ["DVMN_TOKEN"]
    bot_token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    get_user_reviews(dvmn_token, bot_token, chat_id)
