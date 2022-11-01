from flask import Blueprint, render_template, request, redirect
from app.models import db, Results
import configparser
import requests
from datetime import datetime

ui_bp = Blueprint(
    'ui_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@ui_bp.route('/')
def weather_dashboard():
    return render_template('home.html')


@ui_bp.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_unit']
    print(temp_units)
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
    dt_obj = datetime.fromtimestamp(timestamp)
    print(dt_obj)
    now = datetime.now()
    print(now)
    #utc_time = datetime.now()
    result = Results(location=location, temp=temp, dt_obj=dt_obj, feels_like=feels_like, weather=weather, icon_url=icon_url)
    db.session.add(result)
    db.session.commit()
    return render_template('results.html',
                           location=location, temp=temp, dt_obj=dt_obj, now=now,
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

@ui_bp.route('/results')
def list_results():
   results = Results.query
   return render_template('results.html', results=results)


@ui_bp.route('/api/results')
def results_all():
    return {'data': [result.to_dict() for result in Results.query]}
