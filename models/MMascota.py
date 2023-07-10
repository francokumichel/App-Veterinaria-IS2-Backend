from utils.db import db


class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fechaN = db.Column(db.Date())
    raza = db.Column(db.String(100))
    color = db.Column(db.String(100))
    tamano = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)
    vacunas = db.relationship(
        'Vacuna', backref='mascota', lazy=True, cascade="all, delete-orphan")
    turnos = db.relationship('Turno', backref='mascota',
                             lazy=True)
    adopcion = db.relationship(
        "Adopcion", uselist=False, backref="mascota", cascade="all, delete-orphan")
    
    cruza = db.relationship(
        "Cruza", uselist=False, backref="mascota", cascade="all, delete-orphan")

    anonima = db.Column(db.Boolean, default=False)

    def __init__(self, nombre, fechaN, raza, color, tamano, sexo, usuario_id, vacunas, anonima):
        self.nombre = nombre
        self.fechaN = fechaN
        self.raza = raza
        self.color = color
        self.tamano = tamano
        self.sexo = sexo
        self.usuario_id = usuario_id
        self.vacunas = vacunas
        self.anonima = anonima

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fechaN": self.fechaN,
            "raza": self.raza,
            "color": self.color,
            "tamano": self.tamano,
            "sexo": self.sexo,
            "usuario_id": self.usuario_id,
            "anonima": self.anonima,
            "vacunas": [vacuna.to_dict() for vacuna in self.vacunas],
            "turnos": [turno.to_dict() for turno in self.turnos],
            "adopcion": self.adopcion.to_dict() if self.adopcion else None,
            "cruza": self.cruza.to_dict() if self.cruza else None
        }
