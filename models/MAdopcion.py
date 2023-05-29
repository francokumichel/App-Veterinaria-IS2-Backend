from utils.db import db

class Adopcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

    def __init__(self, titulo, descripcion, mascota_id):
        self.titulo = titulo
        self.descripcion = descripcion
        self.mascota_id = mascota_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.titulo,
            "fecha": self.descripcion,
            "mascota_id": self.mascota_id
        }
