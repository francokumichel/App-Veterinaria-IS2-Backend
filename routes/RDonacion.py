from flask import Blueprint, jsonify, request
from models.MDonacion import Donacion
from utils.db import db
from datetime import datetime, timedelta

donacion = Blueprint('donacion', __name__)


@donacion.route("/donacion/add", methods=["POST"])
def agregar_donacion():
    fecha_vencimiento = datetime.strptime(request.json.get("fechaVencimiento"), "%Y-%m")
    if (datetime.now() > fecha_vencimiento):
        return jsonify({"error": "Fecha de vencimiento no puede ser menor a la fecha actual" })

    monto = request.json.get("monto")
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    DNI = request.json.get("DNI")
    campania_id = request.json.get("campania_id")

    nueva_donacion = Donacion(monto=monto, nombre=nombre, apellido=apellido, DNI=DNI, campania_id=campania_id)

    db.session.add(nueva_donacion)
    db.session.commit()

    return jsonify({"message": "Donacion agregada satisfactoriamente"})


@donacion.route("/donacion/get", methods=["GET"])
def obtener_donacions():
    donaciones = Donacion.query.all()
    donacion_json = [
        {
            "id": donacion.id,
            "monto": donacion.monto,
            "nombre": donacion.nombre,
            "apellido": donacion.apellido,
            "DNI": donacion.DNI,
            "campania_id": donacion.campania_id
        }
        for donacion in donaciones
    ]
    return jsonify(donacion_json)

@donacion.route("/donacion/getById/<id>", methods=["GET"])
def obtener_donacion_by_id(id):
    donacion = Donacion.query.filter_by(id=id).first()
    donacion_json = {
            "id": donacion.id,
            "monto": donacion.monto,
            "nombre": donacion.nombre,
            "apellido": donacion.apellido,
            "DNI": donacion.DNI,
            "campania_id": donacion.campania_id
        }
    return jsonify(donacion_json)


@donacion.route("/donacion/put/<id>", methods=["PUT"])
def modificar_donacion(id):
    donacion = Donacion.query.get(id)
    if not donacion:
        return jsonify({"error": "Donacion no encontrada"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    monto = request.json.get("monto")
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    DNI = request.json.get("DNI")

    # Actualiza los campos de la campaña existente
    donacion.monto = monto
    donacion.nombre = nombre
    donacion.apellido = apellido
    donacion.DNI = DNI

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Donacion actualizada satisfactoriamente"})


@donacion.route("/donacion/delete/<id>", methods=["DELETE"])
def eliminar_donacion(id):
    donacion = Donacion.query.get(id)
    if not donacion:
        return jsonify({"error": "Donacion no encontrada"}), 404

    db.session.delete(donacion)
    db.session.commit()

    return jsonify({"message": "Donacion eliminada satisfactoriamente"})