from flask import Blueprint, jsonify, request
from models.MPerdido import Perdido
from utils.db import db
from services.email_service import enviar_email

perdido = Blueprint('perdido', __name__)


@perdido.route("/perdido/add", methods=["POST"])
def agregar_perdido():
    nombre = request.json.get("nombre")
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    email = request.json.get("email")

    # Validar los datos del formulario aquí si es necesario

    nuevo_perdido = Perdido(nombre=nombre, titulo=titulo, descripcion=descripcion, email=email)
    db.session.add(nuevo_perdido)
    db.session.commit()

    return "Anuncio de perro perdido agregado satisfactoriamente"


@perdido.route("/perdido/get", methods=["GET"])
def obtener_perdidos():
    perdidos = Perdido.query.all()
    perdido_json = [
        {
            "id": perdido.id,
            "nombre": perdido.nombre,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
        }
        for perdido in perdidos
    ]
    return jsonify(perdido_json)

@perdido.route("/perdido/getById/<id>", methods=["GET"])
def obtener_perdido_by_id(id):
    perdido = Perdido.query.filter_by(id=id).first()
    perdido_json = {
            "id": perdido.id,
            "nombre": perdido.nombre,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
        }
    return jsonify(perdido_json)


@perdido.route("/perdido/put/<id>", methods=["PUT"])
def modificar_perdido(id):
    perdido = Perdido.query.get(id)
    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    email = request.json.get("email")

    # Actualiza los campos del anuncio existente
    perdido.nombre = nombre
    perdido.titulo = titulo
    perdido.descripcion = descripcion
    perdido.email = email

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Anuncio de perro perdido actualizado satisfactoriamente"})

@perdido.route("/perdido/putReducido/<id>", methods=["PUT"])
def modificar_perdido_reducido(id):
    perdido = Perdido.query.get(id)
    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"}), 404

    email = request.json.get("email")

    # Actualiza los campos del anuncio existente
    perdido.email = email

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Anuncio de perro perdido actualizado satisfactoriamente"})


@perdido.route("/perdido/delete/<id>", methods=["DELETE"])
def eliminar_perdido(id):
    perdido = Perdido.query.get(id)
    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"}), 404

    db.session.delete(perdido)
    db.session.commit()

    return jsonify({"message": "Anuncio de perro perdido eliminado satisfactoriamente"})

@perdido.route("/perdido/getByNombre/<nombre>", methods=["GET"])
def obtener_por_nombre(nombre):
    perdido = perdido.query.filter_by(nombre=nombre).first()

    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"}), 404
    
    perdido_json = [
        {
            "id": perdido.id,
            "nombre": perdido.nombre,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
        }
    ]

    return jsonify(perdido_json)

@perdido.route("/perdido/enviarMail", methods=["POST"])
def mandar_mails():
    email_anunciante = request.json.get("email_anunciante")
    email_interesado = request.json.get("email_interesado")
    enviar_email(email_anunciante, "Anuncio de perro perdido", "Se ha registrado un interesado en su anuncio de perros perdidos. Su email es: " + email_interesado + ". Contactese con el para mas informacion.")
    message = enviar_email(email_interesado, "Anuncio de perro perdido", "El email del anunciante en el que estas interesado es: " + email_anunciante + ". Contactese con el para mas informacion.")
    return jsonify({"message": message})