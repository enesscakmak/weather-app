import requests, json
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from config import api_key
from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import StringField, SubmitField

base_url = "https://api.openweathermap.org/data/2.5/weather?"

app = Flask(__name__)


class WeatherForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:city>', methods=['GET', 'POST'])
def index():
    form = WeatherForm()
    if form.validate_on_submit():
        city = form.city.data
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            main = x["main"]
            current_temperature = main["temp"]
            current_pressure = main["pressure"]
            current_humidity = main["humidity"]
            weather = x["weather"]
            country = x["country"]
            name = x["name"]
            weather_description = weather[0]["description"]
            return render_template('index.html', city=city, country=country, name=name, current_temperature=current_temperature,
                                   current_pressure=current_pressure, current_humidity=current_humidity,
                                   weather_description=weather_description)
        else:
            flash("City Not Found")
            return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
