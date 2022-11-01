from flask import Flask, render_template, request
import requests
import configparser
from datetime import datetime as dt, timezone
from app.models import db
from app import create_app

app = create_app()
if __name__ == "__main__":
   app.run()

app = Flask(__name__)
app.debug = True

app.config.from_object('config')
db.init_app(app)
db.create_all()

@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_unit']
    api_key = get_api_key()
    if temp_units == "F":
        data = get_weather_results_imperial(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
    else:
        data = get_weather_results_metric(zip_code, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
    # tempc = (float(temp-32) * 5/9
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/w/" + icon + ".png"
    timestamp = 1661261478
    dt_obj = dt.fromtimestamp(timestamp)
    print(dt_obj)
    now = dt.now()
    print(now)
    utc_time = dt.now(timezone.utc)

    return render_template('results.html',
                           location=location, temp=temp, dt_obj=dt_obj, now=now, utc_time=utc_time,
                           feels_like=feels_like, weather=weather, icon_url=icon_url)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()



def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

print(get_weather_results_imperial("95129", get_api_key()))
print(get_weather_results_metric("95129", get_api_key()))


if __name__ == '__main__':
	app.run()