from flask import Flask
from routes.turnos import turnos
from utils.db import init_app
from config import DATABASE_CONNECTION_URI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_app(app)

app.register_blueprint(turnos)
