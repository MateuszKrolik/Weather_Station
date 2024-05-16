# ./app.py
import os

from flask import Flask
import pymysql

from extensions import db, API_KEY_VALUE
from routes import esp_database

def create_app(test_config=None):
    pymysql.install_as_MySQLdb()
    
    app = Flask(__name__, template_folder='views')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    
    esp_database.initialize_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)
