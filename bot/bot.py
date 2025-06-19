import datetime
import logging

from bot.development_links_retriever import get_development_links
from bot.wikipedia_info_retriever import get_random_link_from_wikipedia
from bot.weather_info_retriever import get_weather_forecast
from bot.telegram_api import TelegramAPI


def run(telegram_api: TelegramAPI, today: datetime.datetime):
    # everyday
    send_random_wikipedia_articles(telegram_api)
    send_weather_messages(telegram_api, today)

    is_friday = today.weekday() == 4
    if is_friday:
        telegram_api.send_message(
            chat_id="506901938",
            message="No te olvides de leer",
        )
    is_saturday = today.weekday() == 5
    if is_saturday:
        telegram_api.send_poll(
            chat_id="-965755935",
            question="¿Quedamos?",
            options=[
                "OK!, Domingo 21:00",
                "Venga!, Lunes 21:00",
                "Sí, Martes 21:00",
                "No, sry",
            ],
        )
    is_first_day_of_odd_month = today.day == 1 and today.month % 2 == 1
    if is_first_day_of_odd_month:
        links = get_development_links()
        telegram_api.send_message(
            chat_id="506901938",
            message=links,
        )
    is_odd_day = today.day % 2 == 1
    if is_odd_day:
        telegram_api.send_message(
            chat_id="-1001811303682",
            message="Usemos el stepper!",
        )


def send_random_wikipedia_articles(telegram_api):
    links = get_random_link_from_wikipedia()
    links = [links[0]]  # Return only one link
    message = "Random Wikipedia link of the day:\n"
    for i, link in enumerate(links):
        message += f"{i} - {link['link']}\n"
    telegram_api.send_message(chat_id="506901938", message=message)


def send_weather_messages(telegram_api, today):
    try:
        weather_forecast = get_weather_forecast(today)
        logging.debug(f"Weather_forecast: {weather_forecast}")
        telegram_api.send_message(
            chat_id="506901938",
            message=f"""
            Rain today: {weather_forecast['avg_rain_today']:.2f}-{weather_forecast['max_rain_today']:.2f}"
            Wind today: {weather_forecast['avg_wind_today']:.2f}-{weather_forecast['max_wind_today']:.2f}"
            """,
        )
    except Exception as e:
        logging.exception(e)
        return


def is_even_week(today):
    week_number = today.isocalendar()[1]
    return week_number % 2 == 0


if __name__ == "__main__":
    telegram_api = TelegramAPI()
    today = august_first = datetime.datetime(datetime.datetime.now().year, 8, 1)
    run(telegram_api, today)
