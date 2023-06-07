from flask import Blueprint, jsonify, request
from models.MAdopcion import Adopcion
from models.MMascota import Mascota
from models.MUsuario import Usuario
from utils.db import db
from services.email_service import enviar_email

adopcion = Blueprint('adopcion', __name__)


@adopcion.route("/adopcion/add", methods=["POST"])
def agregar_adopcion():
    adopcion = Adopcion.query.filter_by(mascota_id=request.json.get("mascota_id")).first()
    if adopcion:
        return jsonify({"error": "Mascota ya utilizada en otra adopcion"})
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    mascota_id = request.json.get("mascota_id")
    usuario_id = request.json.get("usuario_id")
    finalizada = False

    # Validar los datos del formulario aquí si es necesario

    nuevo_adopcion = Adopcion(titulo=titulo, descripcion=descripcion, mascota_id=mascota_id, usuario_id=usuario_id, finalizada=finalizada)
    db.session.add(nuevo_adopcion)
    db.session.commit()

    return jsonify({"success": "Adopcion agregada exitosamente"})


@adopcion.route("/adopcion/get", methods=["GET"])
def obtener_adopciones():
    adopciones = Adopcion.query.all()
    adopciones_json = [
        {
            "id": adopcion.id,
            "titulo": adopcion.titulo,
            "descripcion": adopcion.descripcion,
            "mascota_id": adopcion.mascota_id,
            "mascota": Mascota.query.filter_by(id=adopcion.mascota_id).first().to_dict(),
            "usuario_id": adopcion.usuario_id,
            "finalizada": adopcion.finalizada
        }
        for adopcion in adopciones
    ]
    return jsonify(adopciones_json)

@adopcion.route("/adopcion/getById/<id>", methods=["GET"])
def obtener_adopcion_by_id(id):
    adopcion = Adopcion.query.filter_by(id=id).first()
    mascota = Mascota.query.filter_by(id=adopcion.mascota_id).first()
    adopcion_json = {
            "id": adopcion.id,
            "titulo": adopcion.titulo,
            "descripcion": adopcion.descripcion,
            "mascota_id": adopcion.mascota_id,
            "usuario_id": adopcion.usuario_id,
            "finalizada": adopcion.finalizada,
            "mascota": mascota.to_dict()
        }
    return jsonify(adopcion_json)

@adopcion.route("/adopcion/put/<id>", methods=["PUT"])
def modificar_adopcion(id):
    adopcion = Adopcion.query.get(id)
    if not adopcion:
        return jsonify({"error": "Adopcion no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    mascota_id = request.json.get("mascota_id")
    finalizada = request.json.get("finalizada")

    # Actualiza los campos del turno existente
    adopcion.titulo = titulo
    adopcion.descripcion = descripcion
    adopcion.mascota_id = mascota_id
    adopcion.finalizada = finalizada

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Adopcion actualizado satisfactoriamente"})

@adopcion.route("/adopcion/delete/<id>", methods=["DELETE"])
def eliminar_adopcion(id):
    adopcion = Adopcion.query.get(id)
    if not adopcion:
        return jsonify({"error": "Adopcion no encontrado"}), 404

    db.session.delete(adopcion)
    db.session.commit()

    return jsonify({"message": "Adopcion eliminado satisfactoriamente"})

@adopcion.route("/adopcion/getByMascotaId/<id>", methods=["GET"])
def buscar_por_mascota_id(id):
    adopcion = Adopcion.query.filter_by(mascota_id=id).first()

    if not adopcion:
        return jsonify({"error": "Adopcion no encontradas"}), 404
    
    mascota_json = {
            "id": adopcion.id,
            "titulo": adopcion.titulo,
            "descripcion": adopcion.descripcion,
            "mascota_id": adopcion.mascota_id,
            "usuario_id": adopcion.usuario_id,
            "finalizada": adopcion.finalizada
        }

    return jsonify(mascota_json)

@adopcion.route("/adopcion/enviarMail", methods=["POST"])
def mandar_mails():
    email = request.json.get("email")
    usuario_id = request.json.get("usuario_id")
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    enviar_email(usuario.email, "Adopcion", "Se ha registrado un interesado en la adopción de su mascota. Su email es: " + email + ". Contactese con el para mas informacion.")
    message = enviar_email(email, "Adopcion", "Tu solicitación de adopción ha sido exitosa, el usuario con el que quieres comunicarte tiene email: " + usuario.email + ". Contactese con el para mas informacion.")
    return jsonify({"message": message})