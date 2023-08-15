import os
import requests


class TelegramAPI:
    telegram_token = os.getenv("TELEGRAM_TOKEN")

    def send_message(cls, chat_id, message):
        url = f"https://api.telegram.org/bot{cls.telegram_token}/sendMessage"
        json_ = {"chat_id": chat_id, "text": message}
        requests.post(
            url=url,
            json=json_,
        )

    def send_poll(cls, chat_id, question, options):
        url = f"https://api.telegram.org/bot{cls.telegram_token}/sendPoll"
        json_ = {
            "chat_id": chat_id,
            "question": question,
            "options": options,
            "is_anonymous": False,
            "allows_multiple_answers": True,
        }
        requests.post(url=url, json=json_)
