#routes/esp_database.py
from flask import render_template, request
from controllers.esp_database import insert_reading, get_last_reading, min_max_avg_reading, get_all_readings
from extensions import API_KEY_VALUE

def initialize_routes(app):
    @app.route('/', methods=['POST'])
    def handle_post():
        api_key = request.form.get('api_key', '')
        if api_key != API_KEY_VALUE:
            return "Wrong API Key provided."

        sensor = request.form.get('sensor', '')
        location = request.form.get('location', '')
        temperature = request.form.get('temperature', '')
        humidity = request.form.get('humidity', '')
        pressure = request.form.get('pressure', '')

        result = insert_reading(sensor, location, temperature, humidity, pressure)
        return str(result)

    @app.route('/', methods=['GET'])
    def handle_get():
        readings_count = request.args.get('readingsCount', default=20, type=int)

        last_reading = get_last_reading()
        last_reading_time = last_reading.reading_time if last_reading else 0
        last_reading_temp = last_reading.temperature if last_reading else 0
        last_reading_humi = last_reading.humidity if last_reading else 0

        min_temp, max_temp, avg_temp = min_max_avg_reading(readings_count, 'temperature')
        min_humi, max_humi, avg_humi = min_max_avg_reading(readings_count, 'humidity')
        readings = get_all_readings(readings_count)

        return render_template('index.html', readings_count=readings_count, last_reading_time=last_reading_time,
                            min_temp=min_temp, max_temp=max_temp, avg_temp=avg_temp,
                            min_humi=min_humi, max_humi=max_humi, avg_humi=avg_humi,
                            last_reading_temp=last_reading_temp, last_reading_humi=last_reading_humi,
                            readings=readings)