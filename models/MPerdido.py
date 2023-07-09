from utils.db import db

class Perdido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    encontrado = db.Column(db.Boolean, default=False)
    nombre = db.Column(db.String(100))
    raza = db.Column(db.String(100))
    color = db.Column(db.String(100))
    tamano = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    nombreImg = db.Column(db.String(100))
    base64 = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, nombre, raza, color, tamano, sexo, titulo, descripcion, email, tipo, nombreImg, base64, usuario_id, encontrado=False):
        self.nombre = nombre
        self.raza = raza
        self.color = color
        self.tamano = tamano
        self.sexo = sexo
        self.titulo = titulo
        self.email = email
        self.descripcion = descripcion
        self.tipo = tipo
        self.nombreImg = nombreImg
        self.base64 = base64
        self.usuario_id = usuario_id
        self.encontrado = encontrado