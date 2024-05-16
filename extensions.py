#./extensions.py
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

API_KEY_VALUE = os.getenv("API_KEY_VALUE")

db = SQLAlchemy()


