from flask import Blueprint, jsonify, request
from models.MTurno import Turno
from utils.db import db

turno = Blueprint('turno', __name__)


@turno.route("/turno/add", methods=["POST"])
def agregar_turno():
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")

    # Validar los datos del formulario aquí si es necesario

    nuevo_turno = Turno(horario=horario, motivo=motivo)
    db.session.add(nuevo_turno)
    db.session.commit()

    return "Turno agregado satisfactoriamente"


@turno.route("/turno/get", methods=["GET"])
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

@turno.route("/turno/getById/<id>", methods=["GET"])
def obtener_turno_by_id(id):
    turno = Turno.query.filter_by(id=id).first()
    turno_json = {
            "id": turno.id,
            "horario": turno.horario,
            "motivo": turno.motivo
        }
    return jsonify(turno_json)


@turno.route("/turno/put/<id>", methods=["PUT"])
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

@turno.route("/turno/delete/<id>", methods=["DELETE"])
def eliminar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"}), 404

    db.session.delete(turno)
    db.session.commit()

    return jsonify({"message": "Turno eliminado satisfactoriamente"})