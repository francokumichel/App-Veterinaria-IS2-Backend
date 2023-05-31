from flask import Blueprint, jsonify, request
from models.MUsuario import Usuario
from utils.db import db
from services.email_service import enviar_email

usuario = Blueprint('usuario', __name__)


@usuario.route("/usuario/add", methods=["POST"])
def agregar_usuario():
    usuario = Usuario.query.filter_by(DNI=request.json.get("DNI")).first()
    if usuario:
        return jsonify({"error": "Ese DNI ya esta usado"})

    usuario = Usuario.query.filter_by(email=request.json.get("email")).first()
    if usuario:
        return jsonify({"error": "Ese email ya esta usado"})
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    DNI = request.json.get("DNI")
    email = request.json.get("email")
    telefono = request.json.get("telefono")
    password = request.json.get("password")
    mascotas = []

    # Validar los datos del formulario aquí si es necesario

    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, DNI=DNI, email=email,
                            telefono=telefono, password=password, mascotas=mascotas, admin=False)
    db.session.add(nuevo_usuario)
    db.session.commit()

    enviar_email(email, "Bienvenido a OhMyDog!",
                 "Bienvenido a OhMyDog!, gracias por registrarte en nuestra plataforma. Su contraseña es: " + password)
    return jsonify({"success": "Usuario agregado satisfactoriamente"})


@usuario.route("/usuario/get", methods=["GET"])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    usuario_json = [
        {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "DNI": usuario.DNI,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "password": usuario.password,
            "admin": usuario.admin,
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas if mascota.anonima == False]
        }
        for usuario in usuarios
    ]
    return jsonify(usuario_json)


@usuario.route("/usuario/getById/<id>", methods=["GET"])
def obtener_usuario_by_id(id):
    usuario = Usuario.query.filter_by(id=id).first()
    usuario_json = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "DNI": usuario.DNI,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "password": usuario.password,
        "admin": usuario.admin,
        "mascotas": [mascota.to_dict() for mascota in usuario.mascotas if mascota.anonima == False]
    }
    return jsonify(usuario_json)


@usuario.route("/usuario/put/<id>", methods=["PUT"])
def modificar_usuario(id):
    usuario = Usuario.query.filter_by(email=request.json.get("email")).first()
    if usuario and usuario.id != request.json.get("id"):
        return jsonify({"error": "Ese email ya esta usado"})

    usuario = Usuario.query.filter_by(DNI=request.json.get("DNI")).first()
    if usuario and usuario.id != request.json.get("id"):
        return jsonify({"error": "Ese DNI ya esta usado"})

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    email = request.json.get("email")
    telefono = request.json.get("telefono")
    password = request.json.get("password")

    # Actualiza los campos del turno existente
    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.email = email
    usuario.telefono = telefono
    usuario.password = password

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"success": "Usuario actualizado satisfactoriamente"})


@usuario.route("/usuario/putReducido/<id>", methods=["PUT"])
def modificar_usuario_reducido(id):
    usuario = Usuario.query.filter_by(email=request.json.get("email")).first()
    if usuario and usuario.id != request.json.get("id"):
        return jsonify({"error": "Ese email ya esta usado"})

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"})

    email = request.json.get("email")
    password = request.json.get("password")

    # Actualiza los campos del turno existente
    usuario.email = email
    usuario.password = password

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"success": "Usuario actualizado satisfactoriamente"})


@usuario.route("/usuario/delete/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado satisfactoriamente"})


@usuario.route("/usuario/getByNombre/<nombre>", methods=["GET"])
def obtener_por_nombre(nombre):
    usuario = Usuario.query.filter_by(nombre=nombre).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    usuario_json = [
        {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "DNI": usuario.DNI,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "password": usuario.password,
            "admin": usuario.admin,
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas if mascota.anonima == False]
        }
    ]

    return jsonify(usuario_json)


@usuario.route("/usuario/getByDocumento/<DNI>", methods=["GET"])
def obtener_por_documento(DNI):
    usuario = Usuario.query.filter_by(DNI=DNI).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    usuario_json = [
        {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "DNI": usuario.DNI,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "password": usuario.password,
            "admin": usuario.admin,
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas if mascota.anonima == False]
        }
    ]

    return jsonify(usuario_json)


@usuario.route("/login", methods=["POST"])
def login():
    user = Usuario.query.filter_by(email=request.json.get("email")).first()
    if (not user):
        responseObject = {
            'status': False,
            'message': 'Correo inexistente.'
        }

    if (user) and (user.password != request.json.get("password")):
        responseObject = {
            'status': False,
            'message': 'Contraseña incorrecta.'
        }

    if (user) and (user.password == request.json.get("password")):
        responseObject = {
            "status": True,
            "message": 'Logeado correctamente.',
            "auth_token": user.email,
            "authorities": user.admin
        }

    return jsonify(responseObject)


@usuario.route("/usuario/mainUsuario/<email>", methods=["GET"])
def main_usuario(email):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    usuario_json = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "DNI": usuario.DNI,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "password": usuario.password,
        "admin": usuario.admin,
        "mascotas": [mascota.to_dict() for mascota in usuario.mascotas if mascota.anonima == False]
    }

    return jsonify(usuario_json)
