from utils.db import db

class Coordenada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coordenadaX = db.Column(db.REAL)
    coordenadaY = db.Column(db.REAL)
    titulo = db.Column(db.String(100))
    parrafo = db.Column(db.String(100))

    def __init__(self, coordenadaX, coordenadaY, titulo, parrafo):
        self.coordenadaX = coordenadaX
        self.coordenadaY = coordenadaY
        self.titulo = titulo
        self.parrafo = parrafo
        