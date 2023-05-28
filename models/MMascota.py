from utils.db import db

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    edad =  db.Column(db.Integer)
    raza = db.Column(db.String(100))
    color = db.Column(db.String(100))
    tamano = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __init__(self, nombre, edad, raza, color, tamano, sexo, usuario_id):
        self.nombre = nombre
        self.edad = edad
        self.raza = raza
        self.color = color
        self.tamano = tamano
        self.sexo = sexo
        self.usuario_id = usuario_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "raza": self.raza,
            "color": self.color,
            "tamano": self.tamano,
            "sexo": self.sexo,
            "usuario_id": self.usuario_id
        }