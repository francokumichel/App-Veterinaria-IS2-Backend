from flask import Blueprint, jsonify, request
from models.MTurno import Turno
from models.MMascota import Mascota
from utils.db import db
from services.email_service import enviar_email
from services.fecha_service import calcular_fecha_turno, es_menor_4_meses

turno = Blueprint('turno', __name__)


@turno.route("/turno/add", methods=["POST"])
def agregar_turno():
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")
    usuario_id = request.json.get("usuario_id")
    mascota_id = request.json.get("mascota_id")

    mascota = Mascota.query.get(mascota_id)

    if not mascota:
        return jsonify({"error": "No se encontró la mascota asociada"}), 404

    # Realizar las verificaciones aquí antes de crear el nuevo turno
    if motivo == "vacunación" and es_menor_4_meses(mascota.edad):
        # El animal es menor a 4 meses, se programa el turno 21 días después
        fecha_turno = calcular_fecha_turno(21)
    elif motivo == "vacunación" and not es_menor_4_meses(mascota.edad):
        # El animal es mayor a 4 meses, se programa el turno 1 año después
        fecha_turno = calcular_fecha_turno(365)
    elif motivo == "vacunación antirrábica" and mascota.es_menor_de_4_meses():
        # No se puede solicitar turno de vacunación antirrábica para un animal menor a 4 meses
        return jsonify({"error": "No se puede solicitar turno de vacunación antirrábica para un animal menor a 4 meses"}), 400
    elif mascota.necesita_vacuna() and not mascota.ha_pasado_1_año_desde_ultima_vacuna():
        # No se puede solicitar turno si no ha pasado 1 año desde la última vacuna
        return jsonify({"error": "No se puede solicitar turno, no ha pasado 1 año desde la última vacuna"}), 400

    nuevo_turno = Turno(horario=horario, motivo=motivo, estado="pendiente",
                        usuario_id=usuario_id, mascota_id=mascota_id)
    db.session.add(nuevo_turno)
    db.session.commit()

    return jsonify({"message": "Turno agregado satisfactoriamente", "fecha_turno": fecha_turno})


@turno.route("/turno/get", methods=["GET"])
def obtener_turnos():
    turnos = Turno.query.all()
    turnos_json = [
        {
            "id": turno.id,
            "nombre_usuario": turno.usuario.nombre,
            "apellido_usuario": turno.usuario.apellido,
            "nombre_mascota": turno.mascota.nombre,
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
        "nombre_usuario": turno.usuario.nombre,
        "apellido_usuario": turno.usuario.apellido,
        "nombre_mascota": turno.mascota.nombre,
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
