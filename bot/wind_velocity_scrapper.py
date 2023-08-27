import logging

import requests
from bs4 import BeautifulSoup


class ScrappingError(Exception):
    pass


def search_wind_velocity_in_samil_in_wisuki():
    try:
        url = "https://es.wisuki.com/forecast/7317/samil"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features='html.parser')
        today_forecasted_velocity = get_forecasted_velocity(soup)
        return today_forecasted_velocity
    except Exception as e:
        logging.error(e)
        raise ScrappingError


def get_forecasted_velocity(soup):
    forecasted_velocity = soup.css.select("table.forecast.long tr:nth-child(4) td:nth-child(5)")[0]
    forecasted_velocity = float(forecasted_velocity.text)
    logging.info(f"forecasted velocity: {forecasted_velocity}")
    return forecasted_velocity


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    search_wind_velocity_in_samil_in_wisuki()
