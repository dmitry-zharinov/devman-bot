import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

TIMEOUT = 5


logger = logging.getLogger()


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_result_message(title, url, is_negative):
    if is_negative:
        result = "⚠️ Необходимо исправить замечания."
    else:
        result = "🚀 Всё хорошо, можно приступать к следующему уроку!"
    return f'Преподаватель проверил работу "[{title}]({url})".\n{result}'


def get_user_reviews(tg_bot, dvmn_token, tg_chat_id):
    timestamp = time.time()
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {dvmn_token}"}

    logging.info('Бот запущен.')

    while True:
        try:
            params = {"timestamp": timestamp}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=TIMEOUT,
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
                    is_negative=result["is_negative"])
                tg_bot.send_message(
                    chat_id=tg_chat_id,
                    text=message,
                    parse_mode="markdown")

            elif status == "timeout":
                timestamp = reviews.get("timestamp_to_request")
            else:
                logging.warning(response)
        except requests.exceptions.ReadTimeout:
            pass
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as err:
            logging.exception(err, exc_info=False)
            time.sleep(TIMEOUT)
            continue


def main():
    load_dotenv()
    dvmn_token = os.environ["DVMN_TOKEN"]
    tg_bot_token = os.environ["TG_BOT_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]

    tg_bot = Bot(token=tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))

    get_user_reviews(tg_bot, dvmn_token, tg_chat_id)


if __name__ == "__main__":
    main()
