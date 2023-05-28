from utils.db import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    DNI = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(100))
    password = db.Column(db.String(100))
    mascotas = db.relationship('Mascota', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def __init__(self, nombre, apellido, DNI, email, telefono, password, mascotas):
        self.nombre = nombre
        self.apellido = apellido
        self.DNI = DNI
        self.email = email
        self.telefono = telefono
        self.password = password
        self.mascotas = mascotas

