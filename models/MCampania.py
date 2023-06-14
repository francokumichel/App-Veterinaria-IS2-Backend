from utils.db import db

class Campania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))

    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        