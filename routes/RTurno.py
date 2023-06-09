from flask import Blueprint, jsonify, request
from models.MTurno import Turno
from models.MMascota import Mascota
from models.MUsuario import Usuario
from models.MVacuna import Vacuna
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
    nomUsuario = request.json.get("nomUsuario")
    nomMascota = request.json.get("nomMascota")
    dniUser = request.json.get("dniUser")

    mascota = Mascota.query.get(mascota_id)
    usuario = Usuario.query.get(usuario_id)
    admin = Usuario.query.filter_by(admin=True).first()

    if(request.json.get('fecha')):
        fecha_turno = datetime.strptime(request.json.get("fecha"), "%Y-%m-%d")
        if (fecha_turno < datetime.now()):
            return jsonify({"error": "Fecha de turno no puede ser menor o igual a la fecha actual"})
        
    turnos = Turno.query.filter_by(mascota_id=mascota_id).all()
    for turno in turnos:
        if turno.motivo == motivo and turno.estado == "Pendiente":
            return jsonify({"error": "Ya existe un turno pendiente para la mascota con el mismo motivo"})
        if turno.motivo == motivo and turno.estado == "Aceptado":
            return jsonify({"error": "Ya existe un turno Aceptado para la mascota con el mismo motivo"})
        if turno.motivo == motivo and turno.estado == "Modificado":
            return jsonify({"error": "Ya existe un turno Aceptado para la mascota con el mismo motivo"})

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
                fecha_turno = calcular_fecha_turno(22)
        else:
            # El animal es mayor a 4 meses, se programa el turno 1 año después
            fecha_turno = calcular_fecha_turno(366)

    nuevo_turno = Turno(horario=horario, motivo=motivo, estado="Pendiente", nomMascota=nomMascota, nomUsuario=nomUsuario, dniUser=dniUser,
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
            "mascota_id": turno.mascota_id,
            "nomMascota": turno.nomMascota,
            "nomUsuario": turno.nomUsuario,
            "dniUser": turno.dniUser
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
        "mascota": mascota.to_dict(),
        "nomMascota": turno.nomMascota,
        "nomUsuario": turno.nomUsuario,
        "dniUser": turno.dniUser
    }

    return jsonify(turno_json)


@turno.route("/turno/put/<id>", methods=["PUT"])
def modificar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"})

    # Obtengo los nuevos datos del formulario o solicitud
    horario = request.json.get("horario")
    usuario_id = request.json.get("usuario_id")

    # Actualizo los campos del turno existente
    turno.horario = horario
    turno.estado = "Modificado"

    # Guardo los cambios en la base de datos
    db.session.commit()

    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if usuario.admin:
        string_a_devolver = "administrador"
        otro_usuario = Usuario.query.filter_by(id=turno.usuario_id).first()
    else:
        otro_usuario = Usuario.query.filter_by(admin=True).first()
        string_a_devolver = f"usuario {otro_usuario.nombre}"

    enviar_email(otro_usuario.email,
                 "Modificación de turno",
                 f"El {string_a_devolver} ha modificado el turno. El nuevo horario es {turno.horario}")

    return jsonify({"message": "Turno actualizado satisfactoriamente"})


@turno.route("/turno/delete/<id>", methods=["DELETE"])
def eliminar_turno(id):
    turno = Turno.query.get(id)
    if not turno:
        return jsonify({"error": "Turno no encontrado"})

    db.session.delete(turno)
    db.session.commit()

    return jsonify({"message": "Turno eliminado satisfactoriamente"})


@turno.route("/turno/cambiarEstado/<id>", methods=["PUT"])
def cambiar_estado_turno(id):
    turno = Turno.query.get(id)
    estado_nuevo = request.json.get("estado")
    usuario_actual = request.json.get("usuario_actual")

    if not turno:
        return jsonify({"error": "Turno no encontrado"})
    
    turno.estado = estado_nuevo

    if usuario_actual['admin']:
        usuario_remitente = Usuario.query.filter_by(id=turno.usuario_id).first()
    else:
        usuario_remitente = Usuario.query.filter_by(admin=True).first()   


    db.session.commit()
    enviar_email(usuario_remitente.email, f"Turno {estado_nuevo}",
                 f"El turno ha sido {estado_nuevo}.")

    return jsonify({"message": f"Turno {estado_nuevo} satisfactoriamente"})

@turno.route("/turno/obtenerMontoDescuentoUsuario/<id>", methods=["GET"])
def obtener_monto_a_descontar(id):
    turno = Turno.query.get(id)

    usuario = Usuario.query.filter_by(id = turno.usuario_id).first()

    return jsonify({'monto_a_descontar': usuario.montoDonado})



@turno.route("/turno/confirmarAsistencia/<id>", methods=["PUT"])
def confirmar_asistencia(id):
    estado_nuevo = request.json.get("estado")
    print(estado_nuevo)
    turno = Turno.query.get(id)
    turno.estado = estado_nuevo
    if (turno.fecha > datetime.now()):
        return jsonify({"error": "Para confirmar la asistencia/no asistencia el dia actual debe ser mayor o igual a la fecha del turno"})
        
    if (estado_nuevo == "Asistió") & ("vacunación".lower() in turno.motivo.lower()):
        print("creando vacuna...", turno.mascota_id)        
        nueva_vacuna = Vacuna(nombre=turno.motivo, fecha=turno.fecha, mascota_id=turno.mascota_id)
        db.session.add(nueva_vacuna)    
    elif estado_nuevo == "No asistió":
        db.session.commit()
        return jsonify({"message": "Se ha confirmado con éxito la no asistencia al turno por parte del usuario"})
    
    db.session.commit()
    message = "Se ha confirmado con éxito la asistencia al turno por parte del usuario."
    return jsonify({"message": message if not "vacunación".lower() in turno.motivo.lower() else message + " Se ha actualizado la libreta de su mascota"})
    
#Hola

@turno.route("/turno/confirmarPago/<id>", methods=["PUT"])
def confirmar_pago(id):
    turno = Turno.query.get(id)
    usuario = Usuario.query.filter_by(id=turno.usuario_id).first()
    usuario.montoDonado = 0
    db.session.commit()
    return jsonify({"message": "El pago se ha realizado exitosamente"})