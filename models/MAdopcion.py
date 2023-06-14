from utils.db import db

class Adopcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(500))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    finalizada = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, descripcion, mascota_id, usuario_id, finalizada):
        self.titulo = titulo
        self.descripcion = descripcion
        self.mascota_id = mascota_id
        self.usuario_id = usuario_id
        self.finalizada = finalizada

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "mascota_id": self.mascota_id,
            "usuario_id": self.usuario_id
        }
