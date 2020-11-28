import datetime
import send_email
import weather

def main():
    # weather params
    # Dallas
    lat = 32.777981
    lon = -96.796211
    exclude = ["minutely", "hourly"]
    unit = "imperial"

    # build URL, make request, parse JSON, send email 
    weather_url = weather.url(lat, lon, exclude=exclude, unit=unit) 
    weather_json = weather.request(weather_url)
    weather_msg = weather.parse(weather_json)
    subject = f"Wake Up! {datetime.date.today().strftime('%x')}"
    to = "" # email address that will receive email
    send_email.send(weather_msg, subject, to)

if __name__ == "__main__":
    main()