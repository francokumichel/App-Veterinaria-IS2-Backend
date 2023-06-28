from flask import Blueprint, jsonify, request
from models.MTurno import Turno
from models.MMascota import Mascota
from models.MUsuario import Usuario
from utils.db import db
from services.email_service import enviar_email
from services.fecha_service import calcular_fecha_turno, es_menor_4_meses, ha_pasado_1_año_desde_ultima_vacuna
from datetime import datetime

turno = Blueprint('turno', __name__)


@turno.route("/turno/add", methods=["POST"])
def agregar_turno():
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")
    usuario_id = request.json.get("usuario_id")
    mascota_id = request.json.get("mascota_id")

    mascota = Mascota.query.get(mascota_id)
    usuario = Usuario.query.get(usuario_id)
    admin = Usuario.query.filter_by(admin=True).first()

    fecha_turno = datetime.strptime(request.json.get("fecha"), "%Y-%m-%d")
    if (fecha_turno < datetime.now()):
        return jsonify({"error": "Fecha de turno no puede ser menor a la fecha actual"})

    if not mascota:
        return jsonify({"error": "No se encontró la mascota asociada"}), 404

    # Realizar las verificaciones aquí antes de crear el nuevo turno
    if "vacunación".lower() in motivo.lower():
        if not ha_pasado_1_año_desde_ultima_vacuna(mascota, motivo):
            # No se puede solicitar turno si no ha pasado 1 año desde la última vacuna
            return jsonify({"error": "No se puede solicitar turno, no ha pasado 1 año desde la última vacuna"})
        elif es_menor_4_meses(mascota.fechaN):
            if "antirrábica".lower() in motivo.lower():
                # No se puede solicitar turno de vacunación antirrábica para un animal menor a 4 meses
                return jsonify({"error": "No se puede solicitar turno de vacunación antirrábica para un animal menor a 4 meses"})
            else:
                # El animal es menor a 4 meses, se programa el turno 21 días después
                fecha_turno = calcular_fecha_turno(21)
        else:
            # El animal es mayor a 4 meses, se programa el turno 1 año después
            fecha_turno = calcular_fecha_turno(365)

    nuevo_turno = Turno(horario=horario, motivo=motivo, estado="Pendiente",
                        fecha=fecha_turno, usuario_id=usuario_id, mascota_id=mascota_id)
    db.session.add(nuevo_turno)
    db.session.commit()
    enviar_email(admin.email, "Solicitud de turno",
                 f"El usuario {usuario.nombre} ha solicitado un turno en el horario de {nuevo_turno.horario} y motivo {nuevo_turno.motivo}. Ante cualquier consulta, contactese con {usuario.email}")
    return jsonify({"message": "Turno agregado satisfactoriamente", "fecha_turno": fecha_turno})


@turno.route("/turno/get", methods=["GET"])
def obtener_turnos():
    turnos = Turno.query.all()
    turnos_json = [
        {
            "id": turno.id,
            "horario": turno.horario,
            "motivo": turno.motivo,
            "estado": turno.estado,
            "fecha": turno.fecha,
            "usuario_id": turno.usuario_id,
            "mascota_id": turno.mascota_id
        }
        for turno in turnos
    ]

    return jsonify(turnos_json)


@turno.route("/turno/getById/<id>", methods=["GET"])
def obtener_turno_by_id(id):
    turno = Turno.query.filter_by(id=id).first()
    mascota = Mascota.query.filter_by(id=turno.mascota_id).first()
    turno_json = {
        "id": turno.id,
        "horario": turno.horario,
        "motivo": turno.motivo,
        "estado": turno.estado,
        "fecha": turno.fecha,
        "usuario_id": turno.usuario_id,
        "mascota_id": turno.mascota_id,
        "mascota": mascota.to_dict()
    }

    return jsonify(turno_json)


@turno.route("/turno/put/<id>", methods=["PUT"])
def modificar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"}), 404

    fecha_turno = datetime.strptime(request.json.get("fecha"), "%Y-%m-%d")
    if (fecha_turno < datetime.now()):
        return jsonify({"error": "Fecha de turno no puede ser menor a la fecha actual"})

    # Obtengo los nuevos datos del formulario o solicitud
    horario = request.json.get("horario")
    motivo = request.json.get("motivo")

    # Actualizo los campos del turno existente
    turno.horario = horario
    turno.motivo = motivo

    # Guardo los cambios en la base de datos
    db.session.commit()

    usuario = Usuario.query.filter_by(id=turno.usuario_id).first()
    enviar_email(usuario.email,
                 "Modificación de turno",
                 f"Su turno ha sido modificado por el siguiente horario y motivo: /n Horario: {turno.horario} /n {turno.motivo}")

    return jsonify({"message": "Turno actualizado satisfactoriamente"})


@turno.route("/turno/delete/<id>", methods=["DELETE"])
def eliminar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"}), 404

    db.session.delete(turno)
    db.session.commit()

    return jsonify({"message": "Turno eliminado satisfactoriamente"})


@turno.route("/turno/cambiarEstado/<id>", methods=["PUT"])
def cambiar_estado_turno(id):
    turno = Turno.query.get(id)
    estado_nuevo = request.json.get("estado")
    email_emisor = request.json.get("email_emisor")

    if not turno:
        return jsonify({"error": "Turno no encontrado"})

    turno.estado = estado_nuevo
    db.session.commit()
    enviar_email(email_emisor, f"Turno {estado_nuevo}",
                 f"El turno ha sido {estado_nuevo}. Para mayor información, contactese con {email_emisor}")

    return jsonify({"message": f"Turno {estado_nuevo} satisfactoriamente"})
