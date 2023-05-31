from utils.db import db


class Vacuna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha = db.Column(db.DateTime(timezone=False))
    mascota_id = db.Column(db.Integer, db.ForeignKey(
        'mascota.id'), nullable=False)

    def __init__(self, nombre, fecha, mascota_id):
        self.nombre = nombre
        self.fecha = fecha
        self.mascota_id = mascota_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "mascota_id": self.mascota_id
        }

    @staticmethod
    def ultima_vacuna(mascota, nombre_vacuna):
        ultima_vacuna = Vacuna.query.filter_by(
            mascota_id=mascota.id, nombre=nombre_vacuna).order_by(Vacuna.fecha.desc()).first()
        return ultima_vacuna
