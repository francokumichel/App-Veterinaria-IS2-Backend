from utils.db import db


class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(100))
    motivo = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    nomMascota = db.Column(db.String(100))
    nomUsuario = db.Column(db.String(100))
    dniUser = db.Column(db.String(100))
    fecha = db.Column(db.DateTime(timezone=False))
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'))
    mascota_id = db.Column(db.Integer, db.ForeignKey(
        'mascota.id'))

    def __init__(self, horario, motivo, estado, nomMascota, nomUsuario, dniUser, fecha, usuario_id, mascota_id):
        self.horario = horario
        self.motivo = motivo
        self.estado = estado
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.mascota_id = mascota_id
        self.nomMascota = nomMascota
        self.nomUsuario = nomUsuario
        self.dniUser = dniUser

    def to_dict(self):
        return {
            "id": self.id,
            "horario": self.horario,
            "motivo": self.motivo,
            "estado": self.estado,
            "fecha": self.fecha,
            "usuario_id": self.usuario_id,
            "mascota_id": self.mascota_id,
            "nomEstado": self.nomMascota,
            "nomUsuario": self.nomUsuario,
            "dniUser": self.dniUser
        }
