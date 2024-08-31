import datetime
import os
import logging
import statistics
import requests

api_key = os.getenv("METEOSIX_API_KEY")


def get_weather_forecast(today):
    url = "https://servizos.meteogalicia.gal/apiv4/getNumericForecastInfo"
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
    params = {
        "coords": "-8.70,42.20",
        "startTime": today.strftime("%Y-%m-%dT%H:%M:%S"),
        "endTime": tomorrow.strftime("%Y-%m-%dT%H:%M:%S"),
        "API_KEY": api_key,
    }
    api_response = requests.get(url, params=params)
    weather_data = api_response.json()
    logging.info(f"weather data: {weather_data}")

    today_weather_variables = weather_data["features"][0]["properties"]["days"][0][
        "variables"
    ]
    tomorrow_weather_variables = weather_data["features"][0]["properties"]["days"][1][
        "variables"
    ]

    is_going_to_rain_today, today_rain_values = is_going_to_rain(
        today_weather_variables
    )
    is_going_to_rain_tomorrow, tomorrow_rain_values = is_going_to_rain(
        tomorrow_weather_variables
    )
    is_going_to_be_windy_today, today_wind_values = is_going_to_be_windy(
        today_weather_variables
    )
    is_going_to_be_windy_tomorrow, tomorrow_wind_values = is_going_to_be_windy(
        tomorrow_weather_variables
    )

    weather_forecast = {
        "is_going_to_rain_today": is_going_to_rain_today,
        "is_going_to_rain_tomorrow": is_going_to_rain_tomorrow,
        "is_going_to_be_windy_today": is_going_to_be_windy_today,
        "is_going_to_be_windy_tomorrow": is_going_to_be_windy_tomorrow,
        "avg_rain_today": statistics.mean(today_rain_values),
        "avg_wind_today": statistics.mean(today_wind_values),
        "max_rain_today": max(today_rain_values),
        "max_wind_today": max(today_wind_values),
    }
    logging.info(weather_forecast)
    return weather_forecast
    # TODO mensaje para cuando haya niebla
    # TODO mensaje para cuando nieve


def is_going_to_rain(variables):
    STRONG_RAIN_VALUE = 3.5
    rain_variable = [
        variable for variable in variables if variable["name"] == "precipitation_amount"
    ][0]
    rain_values = rain_variable["values"]
    rain_values = [value["value"] for value in rain_values]
    logging.info(f"rain values: {rain_values}")
    is_going_to_rain = any(
        [True for value in rain_values if value >= STRONG_RAIN_VALUE]
    )
    return is_going_to_rain, rain_values


def is_going_to_be_windy(variables):
    STRONG_WIND_VALUE = 10
    wind_variable = [variable for variable in variables if variable["name"] == "wind"][
        0
    ]
    wind_values = wind_variable["values"]
    wind_values = [value["moduleValue"] for value in wind_values]
    logging.info(f"wind values: {wind_values}")
    is_going_to_be_windy = any(
        [True for value in wind_values if value >= STRONG_WIND_VALUE]
    )
    return is_going_to_be_windy, wind_values


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    today = datetime.datetime.today()
    weather_forecast = get_weather_forecast(today)
