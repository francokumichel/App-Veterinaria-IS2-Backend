from utils.db import db

class Campania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    seleccionada = db.Column(db.Boolean, default=False)
    donaciones = db.relationship(
        'Donacion', backref='campania', lazy=False)

    def __init__(self, titulo, descripcion, seleccionada):
        self.titulo = titulo
        self.descripcion = descripcion
        self.seleccionada = seleccionada
        