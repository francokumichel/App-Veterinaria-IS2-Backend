from flask import Blueprint, jsonify, request
from models.MMascota import Mascota
from utils.db import db
from datetime import datetime, timedelta

mascota = Blueprint('mascota', __name__)


@mascota.route("/mascota/add", methods=["POST"])
def agregar_mascota():
    fecha_nacimiento = datetime.strptime(request.json.get("fechaN"), "%Y-%m-%d")
    if (datetime.now() < fecha_nacimiento):
        return jsonify({"error": "Fecha de nacimiento no puede ser mayor a la fecha actual" })
    
    #Chequear que no exista otra mascota con el mismo nombre
    mascota = Mascota.query.filter_by(nombre=request.json.get("nombre")).first()
    if mascota:
        return jsonify({"error": "Ya existe una mascota con ese nombre. Por favor cambialo." })
    
    nombre = request.json.get("nombre")
    fechaN = request.json.get("fechaN")
    raza = request.json.get("raza")
    color = request.json.get("color")
    tamano = request.json.get("tamano")
    sexo = request.json.get("sexo")
    usuario_id = request.json.get("usuario_id")
    vacunas = []
    anonima = request.json.get("anonima")

    # Validar los datos del formulario aquí si es necesario

    nuevo_mascota = Mascota(nombre=nombre, fechaN=fechaN, raza=raza, color=color,
                            tamano=tamano, sexo=sexo, usuario_id=usuario_id, vacunas=vacunas, anonima=anonima)
    db.session.add(nuevo_mascota)
    db.session.commit()

    return jsonify({"mascota_id": nuevo_mascota.id})


@mascota.route("/mascota/get", methods=["GET"])
def obtener_mascotas():
    mascotas = Mascota.query.all()
    mascotas_json = [
        {
            "id": mascota.id,
            "nombre": mascota.nombre,
            "fechaN": mascota.fechaN,
            "raza": mascota.raza,
            "color": mascota.color,
            "tamano": mascota.tamano,
            "sexo": mascota.sexo,
            "usuario_id": mascota.usuario_id,
            "vacunas": [vacunas.to_dict() for vacunas in mascota.vacunas],
            "turnos": [turnos.to_dict() for turnos in mascota.turnos],
            "adopcion": mascota.adopcion.to_dict() if mascota.adopcion else None,
            "anonima": mascota.anonima
        }
        for mascota in mascotas
    ]
    return jsonify(mascotas_json)


@mascota.route("/mascota/getById/<id>", methods=["GET"])
def obtener_mascota_by_id(id):
    mascota = Mascota.query.filter_by(id=id).first()
    mascota_json = {
        "id": mascota.id,
        "nombre": mascota.nombre,
        "fechaN": mascota.fechaN,
        "raza": mascota.raza,
        "color": mascota.color,
        "tamano": mascota.tamano,
        "sexo": mascota.sexo,
        "usuario_id": mascota.usuario_id,
        "vacunas": [vacunas.to_dict() for vacunas in mascota.vacunas],
        "turnos": [turnos.to_dict() for turnos in mascota.turnos],
        "adopcion": mascota.adopcion.to_dict() if mascota.adopcion else None,
        "anonima": mascota.anonima
    }
    return jsonify(mascota_json)


@mascota.route("/mascota/put/<id>", methods=["PUT"])
def modificar_usuario(id):
    mascota = Mascota.query.get(id)
    if not mascota:
        return jsonify({"error": "Mascota no encontrado"}), 404
    
    fecha_nacimiento = datetime.strptime(request.json.get("fechaN"), "%Y-%m-%d")
    if (datetime.now() < fecha_nacimiento):
        return jsonify({"error": "Fecha de nacimiento no puede ser mayor a la fecha actual" })
    
    #Chequear que no exista otra mascota con el mismo nombre
    mascotaChequeo = Mascota.query.filter(Mascota.nombre==request.json.get("nombre"), Mascota.id!=request.json.get("id")).first()
    if mascotaChequeo:
        return jsonify({"error": "Ya existe una mascota con ese nombre. Por favor cambialo." })

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    fechaN = request.json.get("fechaN")
    raza = request.json.get("raza")
    color = request.json.get("color")
    tamano = request.json.get("tamano")
    sexo = request.json.get("sexo")
    usuario_id = request.json.get("usuario_id")

    # Actualiza los campos del turno existente
    mascota.nombre = nombre
    mascota.fechaN = fechaN
    mascota.raza = raza
    mascota.color = color
    mascota.tamano = tamano
    mascota.sexo = sexo
    mascota.usuario_id = usuario_id

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Mascota actualizado satisfactoriamente"})


@mascota.route("/mascota/delete/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    mascota = Mascota.query.get(id)
    if not mascota:
        return jsonify({"error": "Mascota no encontrado"})
    
    for turno in mascota.turnos:
        if turno.estado == "Pendiente":
            db.session.delete(turno)
        elif turno.estado == "Aceptado":
            turno.estado = "Finalizado"
            
    db.session.delete(mascota)
    db.session.commit()

    return jsonify({"message": "Mascota eliminado satisfactoriamente"})


@mascota.route("/mascota/getByUsuarioId/<id>", methods=["GET"])
def buscar_por_nombre(id):
    # Obtener el parámetro del nombre de mascota de la solicitud
    nombre_mascota = request.args.get("nombre")
    mascotas = Mascota.query.filter_by(
        usuario_id=id).filter_by(anonima=False).all()

    if nombre_mascota:
        mascotas_query = mascotas_query.filter(Mascota.nombre.ilike(
            f"%{nombre_mascota}%"))  # Filtrar por nombre de mascota si se proporciona

    if not mascotas:
        return jsonify({"error": "Mascotas no encontradas"}), 404

    mascotas_json = [
        {
            "id": mascota.id,
            "nombre": mascota.nombre,
            "fechaN": mascota.fechaN,
            "raza": mascota.raza,
            "color": mascota.color,
            "tamano": mascota.tamano,
            "sexo": mascota.sexo,
            "usuario_id": mascota.usuario_id,
            "vacunas": [vacunas.to_dict() for vacunas in mascota.vacunas],
            "anonima": mascota.anonima
        }
        for mascota in mascotas
    ]

    return jsonify(mascotas_json)
