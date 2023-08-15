import functions_framework
import os
import datetime
import requests


@functions_framework.http
def manage(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    today = datetime.datetime.today()
    is_monday = today == 0
    if is_monday and is_even_week(today):
        send_message_to_telegram(
            chat_id="-965755935",
            message="Buenos días compañeros! esta semana toca reunirse de nuevo!",
            telegram_token=telegram_token,
        )
        send_poll_to_telegram(
            chat_id="-965755935",
            question="¿Qué día tenéis hueco?",
            options=["Lunes", "Martes", "Miércoles", "Jueves", "Sábado", "Domingo"],
            telegram_token=telegram_token,
        )
    return ""


def send_message_to_telegram(chat_id, message, telegram_token):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    json_ = {"chat_id": chat_id, "text": message}
    requests.post(
        url=url,
        json=json_,
    )


def send_poll_to_telegram(chat_id, question, options, telegram_token):
    url = f"https://api.telegram.org/bot{telegram_token}/sendPoll"
    json_ = {
        "chat_id": chat_id,
        "question": question,
        "options": options,
        "is_anonymous": False,
        "allows_multiple_answers": True,
    }
    requests.post(url=url, json=json_)


def is_even_week(today):
    target_date = datetime.datetime(2023, 1, 1)
    weeks_passed = (today - target_date).days // 7
    return weeks_passed % 2 == 0
