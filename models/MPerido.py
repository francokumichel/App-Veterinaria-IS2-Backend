from utils.db import db

class Perdido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, nombre, titulo, descripcion, email):
        self.nombre = nombre
        self.titulo = titulo
        self.email = email
        self.descripcion = descripcion