import logging
from bot import bot
from bot.telegram_api import TelegramAPI
import functions_framework
import datetime


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
    logging.basicConfig(level=logging.INFO)
    telegram_api = TelegramAPI()
    today = datetime.datetime.today()
    bot.run(telegram_api, today)
    return ""
