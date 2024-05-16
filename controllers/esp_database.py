# controllers/esp_database.py
from models.esp_database import SensorData
from extensions import db

def insert_reading(sensor, location, temperature, humidity, pressure):
    reading = SensorData(sensor=sensor, location=location, temperature=temperature, humidity=humidity, pressure=pressure)
    db.session.add(reading)
    db.session.commit()

def get_all_readings(limit):
    return SensorData.query.order_by(SensorData.reading_time.desc()).limit(limit).all()

def get_last_reading():
    return SensorData.query.order_by(SensorData.reading_time.desc()).first()

def min_max_avg_reading(limit, value):
    readings = SensorData.query.order_by(SensorData.reading_time.desc()).limit(limit).all()
    values = [getattr(reading, value) for reading in readings if getattr(reading, value) is not None]
    return min(values, default=0), max(values, default=0), (sum(values) / len(values)) if values else 0