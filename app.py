from flask import Flask, render_template, request, redirect, url_for, flash
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            city = request.form.get("city")

            # Geolocation
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(city)
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")

            # API call
            api_key = "aa6e78b130390f7f1c84ad1cfef2896e"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url).json()

            condition = response['weather'][0]['main']
            description = response['weather'][0]['description']
            temp = int(response['main']['temp'] - 273.15)  # Convert from Kelvin to Celsius
            pressure = response['main']['pressure']
            humidity = response['main']['humidity']
            wind = response['wind']['speed']

            return render_template("index.html", 
                    city=city, 
                    temp=temp, 
                    condition=condition, 
                    description=description, 
                    pressure=pressure, 
                    humidity=humidity, 
                    wind=wind, 
                    current_time=current_time)

        except Exception as e:
            flash("Invalid Entry! Please enter a valid city.")
            return redirect(url_for('index'))
    return render_template("index.html")


if __name__ == "__main__":
    app.secret_key = 'supersecretkey'
    app.run(debug=True)