import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class ScrappingError(Exception):
    pass


def search_wind_velocity_in_samil_in_eltiempoes(headless=True):
    try:
        browser = init_browser(headless)
        url = "https://www.eltiempo.es/vigo-samil.html"
        browser.get(url)  # loads page
        if not headless:
            click_on_accept_cookies(browser)
        today_forecasted_velocity = get_today_forecasted_velocity(browser)
        return today_forecasted_velocity
    except Exception as e:
        logging.error(e)
        raise ScrappingError


def init_browser(headless: bool):
    options = webdriver.ChromeOptions()
    options.add_argument('headless') if headless else ""
    browser = webdriver.Chrome(options=options)
    return browser


def click_on_accept_cookies(browser):
    cookies_button = WebDriverWait(browser, 5).until(
        expected_conditions.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
    )
    cookies_button.click()


def get_today_forecasted_velocity(browser):
    WebDriverWait(browser, 5).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".velocity span.wind-text-value"))
    )
    forecasted_velocities = browser.find_elements(By.CSS_SELECTOR, ".velocity span.wind-text-value")
    forecasted_velocities = [
        float(velocity.text) for velocity in forecasted_velocities if velocity.text.isnumeric()
    ]
    logging.info(f"forecasted velocities: {forecasted_velocities}")
    today_forecasted_velocity = forecasted_velocities[0]
    return today_forecasted_velocity


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    search_wind_velocity_in_samil_in_eltiempoes(headless=True)
