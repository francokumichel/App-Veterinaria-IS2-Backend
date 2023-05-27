from flask import Blueprint, jsonify, request
from models.turnos import Turno
from utils.db import db

turnos = Blueprint('turnos', __name__)


@turnos.route("/agregar_turno", methods=["POST"])
def agregar_turno():
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")

    # Validar los datos del formulario aquí si es necesario

    nuevo_turno = Turno(horario=horario, motivo=motivo)
    db.session.add(nuevo_turno)
    db.session.commit()

    return "Turno agregado satisfactoriamente"


@turnos.route("/obtener_turnos", methods=["GET"])
def obtener_turnos():
    turnos = Turno.query.all()
    turnos_json = [
        {
            "id": turno.id,
            "horario": turno.horario,
            "motivo": turno.motivo
        }
        for turno in turnos
    ]
    return jsonify(turnos_json)


@turnos.route("/modificar_turno/<id>", methods=["PUT"])
def modificar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")

    # Actualiza los campos del turno existente
    turno.horario = horario
    turno.motivo = motivo

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Turno actualizado satisfactoriamente"})
