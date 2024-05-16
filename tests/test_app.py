# ./tests/test_app.py
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
from app import create_app, db
from models.esp_database import SensorData

@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    }
    app = create_app(test_config)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_insert_reading(client, app):
    print("Test 1: Insert a reading into the database and check the response and SensorData count.")
    response = client.post('/', data={'api_key': os.getenv('API_KEY_VALUE'), 'sensor': 'test_sensor', 'location': 'test_location', 'temperature': '1', 'humidity': '2', 'pressure': '3'}, content_type='multipart/form-data')
    assert response.status_code == 200, 'Response status code is not 200'
    with app.app_context():
        assert SensorData.query.count() == 1, 'SensorData count is not 1 after insert'
                        
def test_get_last_reading(client):
    print("Test 2: Retrieve the last reading and check the response.")
    response = client.get('/')
    assert response.status_code == 200, 'Response status code is not 200'

def test_min_max_avg_reading(client, app):
    print("Test 3: Insert multiple readings and check the min, max, and average values.")
    for i in range(10):
        client.post('/', data={'api_key': os.getenv('API_KEY_VALUE'), 'sensor': 'test_sensor', 'location': 'test_location', 'temperature': str(i), 'humidity': str(i), 'pressure': str(i)}, content_type='multipart/form-data')
    response = client.get('/?readingsCount=10')
    assert response.status_code == 200, 'Response status code is not 200'
    with app.app_context():
        assert SensorData.query.count() == 10, 'SensorData count is not 10 after insert'

# CMD: pytest -s 