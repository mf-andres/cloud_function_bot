import datetime
import os
import logging
import requests

api_key = os.getenv("METEOSIX_API_KEY")


def get_weather_forecast(today):
    url = "https://servizos.meteogalicia.gal/apiv4/getNumericForecastInfo"
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
    params = {
        "coords": "-8.775869,42.210547",
        "startTime": today.strftime("%Y-%m-%dT%H:%M:%S"),
        "endTime": tomorrow.strftime("%Y-%m-%dT%H:%M:%S"),
        "API_KEY": api_key,
    }
    api_response = requests.get(url, params=params)
    weather_data = api_response.json()

    today_weather_variables = weather_data["features"][0]["properties"]["days"][0][
        "variables"
    ]
    tomorrow_weather_variables = weather_data["features"][0]["properties"]["days"][1][
        "variables"
    ]

    weather_forecast = {
        "is_going_to_rain_today": is_going_to_rain(today_weather_variables),
        "is_going_to_rain_tomorrow": is_going_to_rain(tomorrow_weather_variables),
        "is_going_to_be_windy_today": is_going_to_be_windy(today_weather_variables),
        "is_going_to_be_windy_tomorrow": is_going_to_be_windy(
            tomorrow_weather_variables
        ),
    }
    print(weather_forecast)
    return weather_forecast
    # TODO mensaje para cuando haya niebla
    # TODO mensaje para cuando nieve


def is_going_to_rain(variables):
    STRONG_RAIN_VALUE = 7.5
    rain_variable = [
        variable for variable in variables if variable["name"] == "precipitation_amount"
    ][0]
    rain_values = rain_variable["values"]
    is_going_to_rain = any(
        [True for value in rain_values if value["value"] >= STRONG_RAIN_VALUE]
    )
    return is_going_to_rain


def is_going_to_be_windy(variables):
    STRONG_WIND_VALUE = 11
    wind_variable = [variable for variable in variables if variable["name"] == "wind"][
        0
    ]
    wind_values = wind_variable["values"]
    print(wind_values)
    is_going_to_be_windy = any(
        [True for value in wind_values if value["moduleValue"] >= STRONG_WIND_VALUE]
    )
    return is_going_to_be_windy


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    today = datetime.datetime.today()
    get_weather_forecast(today)