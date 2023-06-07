from flask import Blueprint, jsonify, request
from models.MAnuncio import Anuncio
from utils.db import db
from services.email_service import enviar_email

anuncio = Blueprint('anuncio', __name__)


@anuncio.route("/anuncio/add", methods=["POST"])
def agregar_anuncio():
    nombre = request.json.get("nombre")
    servicio = request.json.get("servicio")
    zona = request.json.get("zona")
    disponibilidad = request.json.get("disponibilidad")
    email = request.json.get("email")

    # Validar los datos del formulario aquí si es necesario

    nuevo_anuncio = Anuncio(nombre=nombre, servicio=servicio, zona=zona, disponibilidad=disponibilidad, email=email)
    db.session.add(nuevo_anuncio)
    db.session.commit()

    return "Anuncio agregado satisfactoriamente"


@anuncio.route("/anuncio/get", methods=["GET"])
def obtener_anuncios():
    anuncios = Anuncio.query.all()
    anuncio_json = [
        {
            "id": anuncio.id,
            "nombre": anuncio.nombre,
            "servicio": anuncio.servicio,
            "zona": anuncio.zona,
            "disponibilidad": anuncio.disponibilidad,
            "email": anuncio.email,
        }
        for anuncio in anuncios
    ]
    return jsonify(anuncio_json)

@anuncio.route("/anuncio/getById/<id>", methods=["GET"])
def obtener_anuncio_by_id(id):
    anuncio = Anuncio.query.filter_by(id=id).first()
    anuncio_json = {
            "id": anuncio.id,
            "nombre": anuncio.nombre,
            "servicio": anuncio.servicio,
            "zona": anuncio.zona,
            "disponibilidad": anuncio.disponibilidad,
            "email": anuncio.email,
        }
    return jsonify(anuncio_json)


@anuncio.route("/anuncio/put/<id>", methods=["PUT"])
def modificar_anuncio(id):
    anuncio = Anuncio.query.get(id)
    if not anuncio:
        return jsonify({"error": "Anuncio no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    servicio = request.json.get("servicio")
    zona = request.json.get("zona")
    disponibilidad = request.json.get("disponibilidad")
    email = request.json.get("email")

    # Actualiza los campos del anuncio existente
    anuncio.nombre = nombre
    anuncio.servicio = servicio
    anuncio.zona = zona
    anuncio.disponibilidad = disponibilidad
    anuncio.email = email

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Anuncio actualizado satisfactoriamente"})

@anuncio.route("/anuncio/putReducido/<id>", methods=["PUT"])
def modificar_anuncio_reducido(id):
    anuncio = Anuncio.query.get(id)
    if not anuncio:
        return jsonify({"error": "Anuncio no encontrado"}), 404

    email = request.json.get("email")

    # Actualiza los campos del anuncio existente
    anuncio.email = email

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Anuncio actualizado satisfactoriamente"})


@anuncio.route("/anuncio/delete/<id>", methods=["DELETE"])
def eliminar_anuncio(id):
    anuncio = Anuncio.query.get(id)
    if not anuncio:
        return jsonify({"error": "Anuncio no encontrado"}), 404

    db.session.delete(anuncio)
    db.session.commit()

    return jsonify({"message": "Anuncio eliminado satisfactoriamente"})

@anuncio.route("/anuncio/getByZona/<zona>", methods=["GET"])
def obtener_por_zona(zona):
    anuncio = Anuncio.query.filter_by(zona=zona).first()

    if not anuncio:
        return jsonify({"error": "Anuncio no encontrado"}), 404
    
    anuncio_json = [
        {
            "id": anuncio.id,
            "nombre": anuncio.nombre,
            "servicio": anuncio.servicio,
            "zona": anuncio.zona,
            "disponibilidad": anuncio.disponibilidad,
            "email": anuncio.email,
        }
    ]

    return jsonify(anuncio_json)

@anuncio.route("/anuncio/enviarMail", methods=["POST"])
def mandar_mails():
    email_anunciante = request.json.get("email_anunciante")
    email_interesado = request.json.get("email_interesado")
    enviar_email(email_anunciante, "Anuncio de Trabajo", "Se ha registrado un interesado en su anuncio de trabajo. Su email es: " + email_interesado + ". Contactese con el para mas informacion.")
    message = enviar_email(email_interesado, "Anuncio de Trabajo", "El email del anunciante en el que estas interesado es: " + email_anunciante + ". Contactese con el para mas informacion.")
    return jsonify({"message": message})