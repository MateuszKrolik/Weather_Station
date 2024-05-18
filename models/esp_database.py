# ./models/esp_database.py
from sqlalchemy.sql import func
from extensions import db

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor = db.Column(db.String(30))
    location = db.Column(db.String(30))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    reading_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.current_timestamp())