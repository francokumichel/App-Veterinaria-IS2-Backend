from utils.db import db


class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(100))
    motivo = db.Column(db.String(100))

    def __init__(self, horario, motivo):
        self.horario = horario
        self.motivo = motivo
