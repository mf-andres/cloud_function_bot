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
                "OK!, Domingo 21:30",
                "Venga!, Lunes 21:30",
                "Sí, Martes 21:30",
                "No, sry",
            ],
        )
    is_day_7_or_21 = today.day in [7, 21]
    if is_day_7_or_21:
        telegram_api.send_message(
            chat_id="506901938",
            message="Checkout venues and rol events",
        )
    is_day_14 = today.day == 14
    if is_day_14:
        telegram_api.send_message(
            chat_id="506901938",
            message="https://hoxe.vigo.org/axenda/?lang=cas",
        )
    is_first_day_of_odd_month = today.day == 1 and today.month % 2 == 1
    if is_first_day_of_odd_month:
        links = get_development_links()
        telegram_api.send_message(
            chat_id="506901938",
            message=links,
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
        if weather_forecast["is_going_to_rain_today"]:
            telegram_api.send_message(
                chat_id="506901938",
                message=f"""
                Rain today: {weather_forecast['avg_rain_today']:.2f}-{weather_forecast['max_rain_today']:.2f}
                """,
            )
        if weather_forecast["is_going_to_rain_tomorrow"]:
            telegram_api.send_message(
                chat_id="506901938",
                message=f"""
                Rain tomorrow: {weather_forecast['avg_rain_tomorrow']:.2f}-{weather_forecast['max_rain_tomorrow']:.2f}
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
