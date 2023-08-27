import datetime
import os
from unittest.mock import Mock

from bot import bot

telegram_token = os.getenv("TELEGRAM_TOKEN")


def test_the_2023_1_1_is_not_even_week():
    my_datetime = datetime.datetime(2023, 1, 2, 9)
    assert not bot.is_even_week(my_datetime)


def test_the_2023_1_8_is_even_week():
    my_datetime = datetime.datetime(2023, 1, 9, 9)
    assert bot.is_even_week(my_datetime)


def test_chuinibot_sends_rol_reminder_on_mondays_even_weeks():
    telegram_api = Mock()
    telegram_api.send_message = Mock()
    my_datetime = datetime.datetime(2023, 1, 9, 9)
    bot.run(
        telegram_api,
        my_datetime,
    )
    telegram_api.send_message.assert_called_with(
        chat_id="-965755935",
        message="Buenos días compañeros! el rol vive la lucha sigue!!!",
    )


def test_chuinibot_sends_wikipedia_links_everyday():
    telegram_api = Mock()
    telegram_api.send_message = Mock()
    my_datetime = datetime.datetime(2023, 1, 9, 9)
    bot.run(
        telegram_api,
        my_datetime,
    )
    send_message_was_called = telegram_api.send_message.called
    wikipedia_links_were_sent = (
        "Random Wikipedia links of the day"
        in telegram_api.send_message.call_args_list[0].kwargs["message"]
    )
    assert send_message_was_called and wikipedia_links_were_sent
