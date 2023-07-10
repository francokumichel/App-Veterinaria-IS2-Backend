from utils.db import db

class Cruza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaCelo = db.Column(db.DateTime(timezone=False))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __init__(self, fechaCelo, mascota_id, usuario_id):
        self.fechaCelo = fechaCelo
        self.mascota_id = mascota_id
        self.usuario_id = usuario_id


    def to_dict(self):
        return {
            "id": self.id,
            "fechaCelo": self.fechaCelo,
            "mascota_id": self.mascota_id,
            "usuario_id": self.usuario_id,
        }