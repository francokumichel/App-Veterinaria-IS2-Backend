from flask import Blueprint, jsonify, request
from models.MAdopcion import Adopcion
from models.MMascota import Mascota
from models.MUsuario import Usuario
from models.MCruza import Cruza
from utils.db import db
from services.email_service import enviar_email
from services.fecha_service import es_menor_1_anio
from datetime import datetime

cruza = Blueprint('cruza', __name__)

@cruza.route("/cruza/add", methods=["POST"])
def agregar_cruza():
    cruza = Cruza.query.filter_by(mascota_id=request.json.get("mascota_id")).first()
    if cruza:
        return jsonify({"error": "Mascota ya utilizada en otra cruza"})
    
    fecha_celo = request.json.get("fechaCelo")
    mascota_id = request.json.get("mascota_id")
    usuario_id = request.json.get("usuario_id")
    fecha_celo_prueba = datetime.strptime(fecha_celo, "%Y-%m-%d")

    if (fecha_celo_prueba < datetime.now()):
        return jsonify({"error": "La fecha de celo no puede ser menor a la fecha actual"})
    

    mascota = Mascota.query.filter_by(id=mascota_id).first()
    if es_menor_1_anio(mascota.fechaN):
        return jsonify({"error": "La mascota debe tener más de 1 año para poder registrarla para cruza"})

    nueva_cruza = Cruza(fechaCelo=fecha_celo, mascota_id=mascota_id, usuario_id=usuario_id)
    db.session.add(nueva_cruza)
    db.session.commit()

    return jsonify({"success": "Cruza agregada exitosamente"})

@cruza.route("/cruza/get", methods=["GET"])
def obtener_cruzas():
    cruzas = Cruza.query.all()

    cruzas_json = [
        {
            "id": cruza.id,
            "fechaCelo": cruza.fechaCelo,
            "mascota_id": cruza.mascota_id,
            "mascota": Mascota.query.filter_by(id=cruza.mascota_id).first().to_dict(),
            "usuario_id": cruza.usuario_id
        }
        for cruza in cruzas    
    ]

    return jsonify(cruzas_json)

@cruza.route("/cruza/getById/<id>", methods=["GET"])
def obtener_cruza(id):
    cruza = Cruza.query.filter_by(id=id).first()
    if not cruza:
        return jsonify({"error": "Cruza no encontrada"})
    mascota = Mascota.query.filter_by(id=cruza.mascota_id).first()

    cruza_json = {
            
            "id": cruza.id,
            "fechaCelo": cruza.fechaCelo,
            "mascota_id": cruza.mascota_id,
            "usuario_id": cruza.usuario_id,
            "mascota": mascota.to_dict()
        }   

    return jsonify(cruza_json)

@cruza.route("/cruza/put/<id>", methods=["PUT"])
def modificar_cruza(id):
    cruza = Cruza.query.get(id)
    if not cruza:
        return jsonify({"error": "Cruza no encontrada"})

    fecha_celo = request.json.get("fechaCelo")
    cruza.fechaCelo = fecha_celo

    db.session.commit()
    return jsonify({"message": "Cruza actualizada satisfactoriamente"})

@cruza.route("/cruza/delete/<id>", methods=["DELETE"])
def eliminar_cruza(id):
    cruza = Cruza.query.get(id)
    if not cruza:
        return jsonify({"error": "Cruza no encontrada"})

    db.session.delete(cruza)
    db.session.commit()
    return jsonify({"message": "Cruza eliminada satisfactoriamente"})

@cruza.route("/cruza/enviarMail", methods=["POST"])
def mandar_mails():
    email = request.json.get("email")
    usuario_id = request.json.get("usuario_id")
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    enviar_email(usuario.email, "Cruza", "Se ha registrado un interesado para cruza con su mascota. Su email es: " + email + ". Contactese con el para mas informacion.")
    message = enviar_email(email, "Cruza", "Tu solicitud de cruza ha sido exitosa, el usuario con el que quieres comunicarte tiene email: " + usuario.email + ". Contactese con el para mas informacion.")
    return jsonify({"message": message})