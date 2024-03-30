import requests, json
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired
from datetime import datetime

from config import api_key, SECRET_KEY
from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import StringField, SubmitField

base_url = "https://api.openweathermap.org/data/2.5/weather?"

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = SECRET_KEY


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
            current_temperature = f"{main['temp'] - 273.15:.1f}°C"
            weather = x["weather"]
            country = x["sys"]["country"]
            name = x["name"]
            icon = weather[0]["icon"]
            sunrise = datetime.utcfromtimestamp(x["sys"]["sunrise"]).strftime('%H:%M')
            sunset = datetime.utcfromtimestamp(x["sys"]["sunset"]).strftime('%H:%M')
            min_temp = f"{main['temp_min'] - 273.15:.1f}°C"
            max_temp = f"{main['temp_max'] - 273.15:.1f}°C"
            feels_like = f"{main['feels_like'] - 273.15:.1f}°C"
            pressure = f"{main['pressure']} hPa"
            humidity = f"{main['humidity']}%"
            wind = f"{x['wind']['speed']} m/s"
            weather_description = weather[0]["description"].title()
            return render_template('index.html', city=city, country=country, name=name, icon=icon,
                                   current_temperature=current_temperature, description=weather_description, form=form,
                                   min_temp=min_temp, max_temp=max_temp, sunrise=sunrise, sunset=sunset,
                                   feels_like=feels_like, pressure=pressure, humidity=humidity, wind=wind)
        else:
            flash("City Not Found")
            return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
