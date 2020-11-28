import datetime
import directions
import send_email
import weather

def main():
    # weather params
    lat = 32.777981
    lon = -96.796211
    exclude = ["minutely", "hourly"]
    unit = "imperial"

    # directions params
    origin = "Uptown, Dallas, TX"
    destination = "5420 LBJ Freeway Dallas TX"
    waypoints = []
    avoid = ["tolls"]

    # email params
    subject = f"Wake Up! {datetime.date.today().strftime('%x')}"
    to = "" # email address that will receive email

    #################### Change params above ####################

    # build msg, send email
    msg = "<html><body>"
    weather_url = weather.url(lat, lon, exclude=exclude, unit=unit) 
    weather_json = weather.request(weather_url)
    weather_msg = weather.parse(weather_json)
    msg += weather_msg

    directions_url = directions.url(origin, destination, waypoints=waypoints, avoid=avoid)
    directions_json = directions.request(directions_url)
    directions_msg = directions.parse(directions_json)
    msg += directions_msg
    msg += "</body></html>"

    send_email.send(msg, subject, to)

if __name__ == "__main__":
    main()