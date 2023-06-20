from utils.db import db

class Donacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.REAL)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    DNI = db.Column(db.String(100))
    campania_id = db.Column(db.Integer, db.ForeignKey(
        'campania.id'), nullable=True)

    def __init__(self, monto, nombre, apellido, DNI, campania_id):
        self.monto = monto
        self.nombre = nombre
        self.apellido = apellido
        self.DNI = DNI
        self.campania_id = campania_id
        