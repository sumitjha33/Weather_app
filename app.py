from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a more secure key for production
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.form.get("city")
    
    if not city:
        return redirect(url_for('index'))

    try:
        # Geolocation
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        
        if not location:
            return redirect(url_for('index'))

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")

        # API call to OpenWeatherMap
        api_key = "aa6e78b130390f7f1c84ad1cfef2896e"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url).json()
        
        if response.get('cod') != 200:
            return redirect(url_for('index'))

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
        print(f"Error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
