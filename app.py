from re import DEBUG
from flask import Flask, render_template, request
import requests
import utils
from dotenv import dotenv_values

config = dotenv_values(".env")

API_KEY = config['WEATHER_API_KEY']
API_URL = f'https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}'

app = Flask(__name__)

def get_city_weather(city):
    weather_req = requests.get(f'{API_URL}&q={city}')
    weather = weather_req.json()
    return weather
    


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        city_name = request.form['location']

        if city_name:
            weather = get_city_weather(city_name)
            weather['main']['temp'] = float(utils.fahrenheit_to_deg(weather['main']['temp']))
            return render_template("index.html", weather=weather)

    return render_template("index.html", weather = None)

if __name__ == '__main__':
    app.run(DEBUG=True)

