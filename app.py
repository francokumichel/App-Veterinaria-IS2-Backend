from flask import Flask
from routes.RTurno import turno
from routes.RUsuario import usuario
from routes.RMascota import mascota
from routes.RAnuncio import anuncio
from routes.RVacuna import vacuna
from routes.RAdopcion import adopcion
from utils.db import init_app
from config import DATABASE_CONNECTION_URI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_app(app)

app.register_blueprint(turno)
app.register_blueprint(mascota)
app.register_blueprint(usuario)
app.register_blueprint(anuncio)
app.register_blueprint(vacuna)
app.register_blueprint(adopcion)