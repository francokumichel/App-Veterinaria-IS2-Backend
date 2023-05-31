from utils.db import db

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    servicio = db.Column(db.String(100))
    zona = db.Column(db.String(100))
    disponibilidad = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, nombre, servicio, zona, email, disponibilidad):
        self.nombre = nombre
        self.servicio = servicio
        self.zona = zona
        self.email = email
        self.disponibilidad = disponibilidad

        
