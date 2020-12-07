from bs4 import BeautifulSoup
import datetime
import os
import requests

def url(lat, lon, exclude=[], unit=None):
    """
    Return complete OpenWeatherMap URL

        Parameters:
            lat (int):      latitude of location
            lon (int):      longitude of location
            exclude (list): optional exclusions: current, minutely, hourly, daily, alerts
            unit (string):  optional unit: standard, metric, imperial (defaults to standard units)

        Returns:
            base_url (str): URL to use for API call with params included

        Example: url(32.777981, -96.796211, exclude=["minutely", "hourly"], unit="imperial")
    """

    base_url = f"https://api.openweathermap.org/data/2.5/onecall?"

    # API key stored in environment variable 'WEATHER_KEY'
    api_key = os.environ["WEATHER_KEY"]

    # One Call API requires latitude/longitude values
    base_url += f"lat={lat}&lon={lon}"

    # optional params
    if len(exclude) > 0:
        base_url += f"&exclude={','.join(exclude)}"
    if unit:
        base_url += f"&units={unit}"

    base_url += f"&appid={api_key}"
    return base_url

def request(url):
    """Returns JSON body of requested URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response.json()

def parse(body):
    """Parses the JSON and returns HTML message"""

    # converts epoch to X:XX AM/PM
    offset = body["timezone_offset"]
    convert_epoch = lambda time: datetime.datetime.fromtimestamp(time + offset).strftime('%I:%M %p').lstrip('0')
    # converts mm to inches (can be changed to any unit)
    convert_mm = lambda mm: str(round(float(mm) / 25.4, 1)) + " in."
    message = "<pre>"

    # handle current
    current = body["current"]
    current_info = {
        "time": convert_epoch(current["dt"]),
        "temp": round(current["temp"]),
        "feel": round(current["feels_like"]),
        "conditions": [],
    }

    message += f"<b>Current Weather ({current_info['time']}):</b>\n"
    message += f"Temp: {current_info['temp']}&deg; (feels like {current_info['feel']}&deg;)\n"

    for desc in current["weather"]:
        current_info["conditions"].append(desc["description"])
    message += f"Conditions: {', '.join(current_info['conditions'])}\n"

    if "rain" in current:
        current_info["rain"] = convert_mm(current["rain"]["1h"])
        message += f"Rain: {current_info['rain']}\n"
    if "snow" in current:
        current_info["snow"] = convert_mm(current["snow"]["1h"])
        message += f"Snow: {current_info['snow']}\n"
    message += "\n"

    # handle daily
    message += "<b>Daily Forecast:</b>\n"
    daily = body["daily"]
    today = daily[0]
    daily_info = {
        "sunrise": convert_epoch(today["sunrise"]),
        "sunset": convert_epoch(today["sunset"]),
        "min": round(today["temp"]["min"]),
        "max": round(today["temp"]["max"]),
        "conditions": [] 
    }
    message += f"Sunrise/sunset: {daily_info['sunrise']} - {daily_info['sunset']}\n"
    message += f"Hi/Lo: {daily_info['max']}&deg;/{daily_info['min']}&deg;\n"

    for desc in today["weather"]:
        daily_info["conditions"].append(desc["description"])
    message += f"Conditions: {', '.join(daily_info['conditions'])}\n"

    if "rain" in today:
        daily_info["rain"] = convert_mm(today["rain"])
        message += f"Rain: {daily_info['rain']}\n"
    if "snow" in today:
        daily_info["snow"] = convert_mm(today["snow"])
        message += f"Snow: {daily_info['snow']}\n"

    # handle alerts
    alerts = []
    if "alerts" in body:
        for alert in body["alerts"]:
            alert_info = {
                "name": alert["event"],
                "start": convert_epoch(alert["start"]),
                "end": convert_epoch(alert["end"]),
                "desc": alert["description"]
            }
            alerts.append(alert_info)

    if len(alerts):
        message += "\n"
        message += "<b>Weather Alerts</b>\n"
        for alert in alerts:
            message += f"{alert['name']} from {alert['start']} - {alert['end']}\n"

    message += "</pre>"
    return message

def main():
    lat = 32.777981
    lon = -96.796211
    exclude = ["minutely", "hourly"]
    unit = "imperial"
    weather_url = url(lat, lon, exclude=exclude, unit=unit) 
    weather_json = request(weather_url)
    weather_msg = parse(weather_json)
    text = BeautifulSoup(weather_msg, "html.parser").text.strip()
    print(text)

if __name__ == "__main__":
    main()