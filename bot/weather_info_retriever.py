import datetime
import logging
import statistics
import requests


def get_weather_forecast(today):
    # 1. Target endpoint for Vigo, Galicia (Coordinates adjusted slightly to match yours)
    url = "https://api.open-meteo.com/v1/forecast"
    
    # We ask for 2 forecast days to cover today and tomorrow fully
    params = {
        "latitude": 42.20,
        "longitude": -8.70,
        "hourly": ["precipitation"],
        "forecast_days": 2,
        "timezone": "Europe/Madrid"
    }
    
    api_response = requests.get(url, params=params)
    weather_data = api_response.json()
    logging.info(f"weather data: {weather_data}")

    # Open-Meteo returns flat lists of 48 values (24 hours * 2 days)
    hourly_data = weather_data.get("hourly", {})
    all_rain_values = hourly_data.get("precipitation", [0]*48)

    # 2. Slice arrays into 24-hour windows for today vs tomorrow
    today_rain_values = all_rain_values[0:24]
    tomorrow_rain_values = all_rain_values[24:48]

    # 3. Evaluate conditional metrics using your logic functions
    is_going_to_rain_today = check_rain_threshold(today_rain_values)
    is_going_to_rain_tomorrow = check_rain_threshold(tomorrow_rain_values)

    weather_forecast = {
        "is_going_to_rain_today": is_going_to_rain_today,
        "is_going_to_rain_tomorrow": is_going_to_rain_tomorrow,
        "avg_rain_today": statistics.mean(today_rain_values) if today_rain_values else 0,
        "max_rain_today": max(today_rain_values) if today_rain_values else 0,
    }
    
    logging.info(weather_forecast)
    return weather_forecast
    # TODO mensaje para cuando haya niebla
    # TODO mensaje para cuando nieve


def check_rain_threshold(rain_values):
    STRONG_RAIN_VALUE = 3.5  # mm/h
    logging.info(f"rain values: {rain_values}")
    return any(value >= STRONG_RAIN_VALUE for value in rain_values)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    today = datetime.datetime.today()
    weather_forecast = get_weather_forecast(today)