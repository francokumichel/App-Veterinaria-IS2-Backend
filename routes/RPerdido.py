from flask import Blueprint, jsonify, request
from models.MPerdido import Perdido
from utils.db import db
from services.email_service import enviar_email
from datetime import datetime, timedelta
import base64

perdido = Blueprint('perdido', __name__)


@perdido.route("/perdido/add", methods=["POST"])
def agregar_perdido():
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

    perdidos = Perdido.query.all()
    for perdido in perdidos:
        if perdido.nombre == request.json.get("nombre") and perdido.usuario_id == request.json.get("usuario_id") and perdido.encontrado == False:
            return jsonify({"error": "Ya existe un anuncio activo de perro perdido con esa mascota"})
    
    usuario_id = request.json.get("usuario_id")
    nombre = request.json.get("nombre")
    raza = request.json.get("raza")
    color = request.json.get("color")
    tamano = request.json.get("tamano")
    sexo = request.json.get("sexo")
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    email = request.json.get("email")
    tipo = request.json.get("imagen").get("tipo")
    nombreImg = request.json.get("imagen").get("nombre")
    base64 = request.json.get("imagen").get("base64")
    # Validar los datos del formulario aquí si es necesario

    nuevo_perdido = Perdido(nombre=nombre, raza=raza, color=color, tamano=tamano, sexo=sexo, titulo=titulo, descripcion=descripcion, email=email, tipo=tipo, nombreImg=nombreImg, base64=base64, usuario_id=usuario_id, encontrado=False)
    db.session.add(nuevo_perdido)
    db.session.commit()

    return jsonify({"message":"Anuncio de perro perdido agregado satisfactoriamente"})


@perdido.route("/perdido/get", methods=["GET"])
def obtener_perdidos():
    perdidos = Perdido.query.all()
    perdido_json = [
        {
            "id": perdido.id,
            "encontrado": perdido.encontrado,
            "usuario_id": perdido.usuario_id,
            "nombre": perdido.nombre,
            "raza": perdido.raza,
            "color": perdido.color,
            "tamano": perdido.tamano,
            "sexo": perdido.sexo,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
            "imagen": {
                "tipo": perdido.tipo,
                "nombre": perdido.nombreImg,
                "base64": base64.b64encode(perdido.base64).decode("utf-8", "ignore")
            }
        }
        for perdido in perdidos
    ]
    return jsonify(perdido_json)

@perdido.route("/perdido/getById/<id>", methods=["GET"])
def obtener_perdido_by_id(id):
    perdido = Perdido.query.filter_by(id=id).first()
    perdido_json = {
            "id": perdido.id,
            "encontrado": perdido.encontrado,
            "usuario_id": perdido.usuario_id,
            "nombre": perdido.nombre,
            "raza": perdido.raza,
            "color": perdido.color,
            "tamano":perdido.tamano,
            "sexo": perdido.sexo,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
            "imagen": {
                "tipo": perdido.tipo,
                "nombre": perdido.nombreImg,
                "base64": base64.b64encode(perdido.base64).decode("ascii", "ignore")
            }
        }
    return jsonify(perdido_json)


@perdido.route("/perdido/put/<id>", methods=["PUT"])
def modificar_perdido(id):
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

    perdido = Perdido.query.get(id)
    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"})

    # Obtén los nuevos datos del formulario o solicitud
    usuario_id = request.json.get("usuario_id")
    nombre = request.json.get("nombre")
    raza = request.json.get("raza")
    color = request.json.get("color")
    tamano = request.json.get("tamano")
    sexo = request.json.get("sexo")
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
    email = request.json.get("email")
    tipo = request.json.get("imagen").get("tipo")
    nombreImg = request.json.get("imagen").get("nombre")
    base64 = request.json.get("imagen").get("base64")
    encontrado = request.json.get("encontrado")

    # Actualiza los campos del anuncio existente
    perdido.usuario_id = usuario_id
    perdido.nombre = nombre
    perdido.raza = raza
    perdido.color = color
    perdido.tamano = tamano
    perdido.sexo = sexo
    perdido.titulo = titulo
    perdido.descripcion = descripcion
    perdido.email = email
    perdido.tipo = tipo
    perdido.nombreImg = nombreImg
    perdido.base64 = base64
    perdido.encontrado = encontrado

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Anuncio de perro perdido actualizado satisfactoriamente"})

@perdido.route("/perdido/putReducido/<id>", methods=["PUT"])
def modificar_perdido_reducido(id):
    perdido = Perdido.query.get(id)
    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"})

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
        return jsonify({"error": "Anuncio de perro perdido no encontrado"})

    db.session.delete(perdido)
    db.session.commit()

    return jsonify({"message": "Anuncio de perro perdido eliminado satisfactoriamente"})

@perdido.route("/perdido/getByNombre/<nombre>", methods=["GET"])
def obtener_por_nombre(nombre):
    perdido = perdido.query.filter_by(nombre=nombre).first()

    if not perdido:
        return jsonify({"error": "Anuncio de perro perdido no encontrado"})
    
    perdido_json = [
        {
            "id": perdido.id,
            "encontrado": perdido.encontrado,
            "usuario_id": perdido.usuario_id,
            "nombre": perdido.nombre,
            "raza": perdido.raza,
            "color": perdido.color,
            "tamano":perdido.tamano,
            "sexo": perdido.sexo,
            "titulo": perdido.titulo,
            "descripcion": perdido.descripcion,
            "email": perdido.email,
            "imagen": {
                "tipo": perdido.tipo,
                "nombre": perdido.nombreImg,
                "base64": base64.b64encode(perdido.base64).decode("ascii", "ignore")
            }
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