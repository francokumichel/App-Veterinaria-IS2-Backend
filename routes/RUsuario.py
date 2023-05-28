from flask import Blueprint, jsonify, request
from models.MMascota import Mascota
from models.MUsuario import Usuario
from utils.db import db

usuario = Blueprint('usuario', __name__)


@usuario.route("/usuario/add", methods=["POST"])
def agregar_usuario():
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    DNI = request.json.get("DNI")
    email = request.json.get("email")
    telefono = request.json.get("telefono")
    password = request.json.get("password")
    mascotas = []

    # Validar los datos del formulario aquí si es necesario

    nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, DNI=DNI, email=email, telefono=telefono, password=password, mascotas=mascotas)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return "Usuario agregado satisfactoriamente"


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
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas]
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
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas]
        }
    return jsonify(usuario_json)


@usuario.route("/usuario/put/<id>", methods=["PUT"])
def modificar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    DNI = request.json.get("DNI")
    email = request.json.get("email")
    telefono = request.json.get("telefono")
    password = request.json.get("password")

    # Actualiza los campos del turno existente
    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.DNI = DNI
    usuario.email = email
    usuario.telefono = telefono
    usuario.password = password

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Usuario actualizado satisfactoriamente"})

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
            "mascotas": [mascota.to_dict() for mascota in usuario.mascotas]
        }
    ]

    return jsonify(usuario_json)