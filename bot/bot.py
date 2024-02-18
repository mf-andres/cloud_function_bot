import datetime
import logging

import requests

from bot.weather_info_retriever import get_weather_forecast
from bot.telegram_api import TelegramAPI
from urllib import parse


def run(telegram_api: TelegramAPI, today: datetime.datetime):
    # everyday
    send_random_wikipedia_articles(telegram_api)
    send_weather_messages(telegram_api)

    is_saturday = today.weekday() == 5
    if is_saturday:
        telegram_api.send_message(
            chat_id="-965755935",
            message="Reminder! Mañana rol a las 21:00.",
        )

    is_sunday = today.weekday() == 6
    if is_sunday:
        telegram_api.send_message(
            chat_id="-965755935",
            message="Hoy rol a las 21:00. ¿Alguna baja?",
        )
        telegram_api.send_poll(
            chat_id="-965755935",
            question="Hoy rol a las 21:00. Confirmen asistencia!",
            options=["Confirmo asistencia", "Me surgió un compromiso"],
        )


def send_random_wikipedia_articles(telegram_api):
    links = get_random_links_from_wikipedia()
    message = "Random Wikipedia links of the day:\n\n"
    for i, link in enumerate(links):
        message += f"{i} - {link}\n"
    telegram_api.send_message(chat_id="506901938", message=message)


def get_random_links_from_wikipedia():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 1,  # Number of random pages to retrieve
        "rnnamespace": 0,  # Only retrieve pages in the main namespace
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data["query"]["random"]

    # Print the page titles and links
    links = list()
    for page in pages:
        title = page["title"]
        title = parse.quote(title)
        link = f"https://en.wikipedia.org/wiki/{title}"
        links.append(link)
    return links


def send_weather_messages(telegram_api):
    try:
        weather_forecast = get_weather_forecast()
        logging.info(f"weather_forecast: {weather_forecast}")
        if weather_forecast["is_going_to_rain_today"]:
            message = "Hoxe chove!"
            telegram_api.send_message(chat_id="506901938", message=message)
        if weather_forecast["is_going_to_be_windy_today"]:
            message = "Hoy hay viento!"
            telegram_api.send_message(chat_id="506901938", message=message)
        if weather_forecast["is_going_to_rain_tomorrow"]:
            message = "Seica chove mañana!"
            telegram_api.send_message(chat_id="506901938", message=message)
    except Exception as e:
        logging.error(e)
        return


def is_even_week(today):
    week_number = today.isocalendar()[1]
    return week_number % 2 == 0
