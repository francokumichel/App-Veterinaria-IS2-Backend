from flask import Flask
from routes.RTurno import turno
from routes.RUsuario import usuario
from routes.RMascota import mascota
from routes.RAnuncio import anuncio
from routes.RVacuna import vacuna
from routes.RAdopcion import adopcion
from routes.RCampania import campania
from routes.RDonacion import donacion
from utils.db import init_app
from config import DATABASE_CONNECTION_URI
from services.email_service import mail
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración para envío de emails
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True

init_app(app)

app.register_blueprint(turno)
app.register_blueprint(mascota)
app.register_blueprint(usuario)
app.register_blueprint(anuncio)
app.register_blueprint(vacuna)
app.register_blueprint(adopcion)
app.register_blueprint(campania)
app.register_blueprint(donacion)

mail.init_app(app)  # Inicializo el servicio de email
