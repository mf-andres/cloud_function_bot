import datetime

import requests

from bot.wind_velocity_scrapper import search_wind_velocity_in_samil_in_wisuki, ScrappingError
from bot.telegram_api import TelegramAPI
from urllib import parse


def run(telegram_api: TelegramAPI, today: datetime.datetime):
    # everyday
    send_random_wikipedia_articles(telegram_api)
    send_go_fly_the_kite_message(telegram_api)

    # each even week on mondays
    is_monday = today.weekday() == 0
    if is_monday:
        telegram_api.send_message(
            chat_id="-965755935",
            message="Buenos días compañeros! el rol vive la lucha sigue!!!",
        )
        telegram_api.send_poll(
            chat_id="-965755935",
            question="¿Qué noche tenéis hueco?",
            options=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
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
        "rnlimit": 5,  # Number of random pages to retrieve
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


# TODO unit test
def send_go_fly_the_kite_message(telegram_api):
    try:
        today_wind_velocity = search_wind_velocity_in_samil_in_wisuki()
        moderate_wind_velocity = 12.
        if today_wind_velocity > moderate_wind_velocity:
            message = f"Hoy es buen día para volar la cometa (velocidad del viento = {today_wind_velocity} km/h)"
            telegram_api.send_message(chat_id="506901938", message=message)
    except ScrappingError:
        return


def is_even_week(today):
    week_number = today.isocalendar()[1]
    return week_number % 2 == 0
