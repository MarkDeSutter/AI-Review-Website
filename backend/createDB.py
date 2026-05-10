from app import app
from extensions import db
from models import *

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
