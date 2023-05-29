from flask import Blueprint, jsonify, request
from models.MVacuna import Vacuna
from utils.db import db

vacuna = Blueprint('vacuna', __name__)


@vacuna.route("/vacuna/add", methods=["POST"])
def agregar_vacuna():
    nombre = request.json.get("nombre")
    fecha = request.json.get("fecha")
    mascota_id = request.json.get("mascota_id")

    # Validar los datos del formulario aquí si es necesario

    nuevo_vacuna = Vacuna(nombre=nombre, fecha=fecha, mascota_id=mascota_id)
    db.session.add(nuevo_vacuna)
    db.session.commit()

    return "Vacuna agregado satisfactoriamente"


@vacuna.route("/vacuna/get", methods=["GET"])
def obtener_vacunas():
    vacunas = Vacuna.query.all()
    vacunas_json = [
        {
            "id": vacuna.id,
            "nombre": vacuna.nombre,
            "fecha": vacuna.fecha,
            "mascota_id": vacuna.mascota_id
        }
        for vacuna in vacunas
    ]
    return jsonify(vacunas_json)

@vacuna.route("/vacuna/getById/<id>", methods=["GET"])
def obtener_vacuna_by_id(id):
    vacuna = Vacuna.query.filter_by(id=id).first()
    vacuna_json = {
            "id": vacuna.id,
            "nombre": vacuna.nombre,
            "fecha": vacuna.fecha,
            "mascota_id": vacuna.mascota_id
        }
    return jsonify(vacuna_json)

@vacuna.route("/vacuna/put/<id>", methods=["PUT"])
def modificar_vacuna(id):
    vacuna = Vacuna.query.get(id)
    if not vacuna:
        return jsonify({"error": "Vacuna no encontrado"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    nombre = request.json.get("nombre")
    fecha = request.json.get("fecha")
    mascota_id = request.json.get("mascota_id")

    # Actualiza los campos del turno existente
    vacuna.nombre = nombre
    vacuna.fecha = fecha
    vacuna.mascota_id = mascota_id

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Vacuna actualizado satisfactoriamente"})

@vacuna.route("/vacuna/delete/<id>", methods=["DELETE"])
def eliminar_vacuna(id):
    vacuna = Vacuna.query.get(id)
    if not vacuna:
        return jsonify({"error": "Vacuna no encontrado"}), 404

    db.session.delete(vacuna)
    db.session.commit()

    return jsonify({"message": "Vacuna eliminado satisfactoriamente"})

@vacuna.route("/vacuna/getByMascotaId/<id>", methods=["GET"])
def buscar_por_mascota_id(id):
    vacunas = Vacuna.query.filter_by(mascota_id=id)

    if not vacunas:
        return jsonify({"error": "Vacunas no encontradas"}), 404
    
    vacunas_json = [
       {
            "id": vacuna.id,
            "nombre": vacuna.nombre,
            "fecha": vacuna.fecha,
            "mascota_id": vacuna.mascota_id
        }
        for vacuna in vacunas
    ]

    return jsonify(vacunas_json)