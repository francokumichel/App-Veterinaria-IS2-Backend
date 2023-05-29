from utils.db import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    DNI = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)
    mascotas = db.relationship('Mascota', backref='usuario', lazy=True, cascade="all, delete-orphan")
    adopciones = db.relationship('Adopcion', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def __init__(self, nombre, apellido, DNI, email, telefono, password, mascotas, admin):
        self.nombre = nombre
        self.apellido = apellido
        self.DNI = DNI
        self.email = email
        self.telefono = telefono
        self.password = password
        self.mascotas = mascotas
        self.admin = admin  
        


