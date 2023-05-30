from utils.db import db


class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(100))
    motivo = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)
    usuario = db.relationship(
        'Usuario', backref='turno', lazy=True)

    mascota_id = db.Column(db.Integer, db.ForeignKey(
        'mascota.id'), nullable=False)
    mascotas = db.relationship(
        'Mascota', backref='turno', lazy=True)

    def __init__(self, horario, motivo, usuario_id, mascota_id):
        self.horario = horario
        self.motivo = motivo
        self.usuario_id = usuario_id
        self.mascota_id = mascota_id
