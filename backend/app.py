import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
