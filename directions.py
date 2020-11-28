from bs4 import BeautifulSoup
import os
import requests

def url(origin, destination, waypoints=[], avoid=[]):
    """
    Return complete Google Directions URL

        Parameters:
            origin (string):      starting point
            destination (string): destination
            waypoints (list):     optional list of addresses to pass through
            avoid (list):         optional list to avoid (tolls, highways, ferries)

        Returns:
            base_url (str): URL to use for API call with params included

        Example: url("Uptown, Dallas, TX", "5420 LBJ Freeway Dallas TX", waypoints=["NorthPark Center Dallas, TX"], avoid=["tolls"])
    """

    base_url = f"https://maps.googleapis.com/maps/api/directions/json?"

    # Directions API key stored in environment variable 'DIRECTIONS_KEY'
    api_key = os.environ["DIRECTIONS_KEY"]

    # Required params
    base_url += f"origin={origin.strip().replace(' ', '+')}&destination={destination.strip().replace(' ', '+')}"

    # Optional params
    if len(waypoints):
        waypoints = list(map(lambda x: x.strip().replace(" ", "+"), waypoints))
        base_url += f"&waypoints=via:{'|'.join(waypoints)}"
    if len(avoid):
        base_url += f"&avoid={'|'.join(avoid)}"

    base_url += f"&key={api_key}"
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

    message = "<pre>"
    message += "<b>Commute:</b>\n"
    
    routes = body["routes"]
    if len(routes) == 0:
        message += "<b>No routes were returned</b></pre>"
        return message

    summaries = []
    durations = []
    distances = []
    for route in routes:
        leg = route["legs"][0]
        summaries.append(route["summary"])
        durations.append(leg["duration"]["text"])
        distances.append(leg["distance"]["text"])

    zipped = zip(summaries, durations, distances)
    for group in zipped:
        message += f"via {group[0]}: {group[1]}, {group[2]}\n"

    message += "</pre>"
    return message

def main():
    origin = "Uptown, Dallas, TX"
    destination = "5420 LBJ Freeway Dallas TX"
    waypoints = []
    avoid = ["tolls"]
    directions_url = url(origin, destination, waypoints=waypoints, avoid=avoid)
    directions_json = request(directions_url)
    directions_msg = parse(directions_json)
    text = BeautifulSoup(directions_msg, "html.parser").text.strip()
    print(text)

if __name__ == "__main__":
    main()