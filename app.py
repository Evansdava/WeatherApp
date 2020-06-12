from flask import Flask, request, render_template
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")


@app.route("/")
def index():
    """Show the homepage and ask for a location"""
    return render_template("index.html")


@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    state = request.args.get("state")
    country = request.args.get("country")
    mood = request.args.get("mood")

    url = "https://api.openweathermap.org/data/2.5/weather"

    if country and not state:
        url += f"?q={city},{country}"
    elif country:
        url += f"?q={city},{state},{country}"
    elif state:
        url += f"?q={city},{state}"
    else:
        url += f"?q={city}"

    url += f"&appid={API_KEY}"

    r = requests.get(url)
    if r.status_code == 200:  # If the request was successful
        response = json.loads(r.content)
        weather = response["weather"]
        temp = response["main"]
        city = response["name"]
    else:
        weather = None
        temp = None
        city = None

    return render_template("weather.html", weather=weather, mood=mood,
                           temp=temp, city=city, state=state, country=country)
