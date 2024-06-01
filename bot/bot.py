import datetime
import logging

from bot.wikipedia_info_retriever import get_random_links_from_wikipedia
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
            question="Confirmen asistencia!",
            options=["Confirmo asistencia", "No confirmo asistencia"],
        )


def send_random_wikipedia_articles(telegram_api):
    links = get_random_links_from_wikipedia()
    links = [links[0]]  # Return only one link
    message = "Random Wikipedia links of the day:\n\n"
    for i, link in enumerate(links):
        message += f"{i} - {link}\n"
    telegram_api.send_message(chat_id="506901938", message=message)


def send_weather_messages(telegram_api, today):
    try:
        weather_forecast = get_weather_forecast(today)
        logging.debug(f"weather_forecast: {weather_forecast}")
        telegram_api.send_message(
            chat_id="506901938",
            message=f"rain tomorrow: {weather_forecast['avg_rain_tomorrow']}",
        )
        telegram_api.send_message(
            chat_id="506901938",
            message=f"wind force tomorrow: {weather_forecast['avg_wind_tomorrow']}",
        )
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


if __name__ == "__main__":
    telegram_api = TelegramAPI()
    today = datetime.datetime.today()
    run(telegram_api, today)
