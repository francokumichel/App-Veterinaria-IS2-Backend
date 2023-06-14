from flask import Blueprint, jsonify, request
from models.MCampania import Campania
from utils.db import db

campania = Blueprint('campania', __name__)


@campania.route("/campania/add", methods=["POST"])
def agregar_campania():
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")
   
    # Validar los datos del formulario aquí si es necesario

    nueva_campania = Campania(titulo=titulo, descripcion=descripcion)
    db.session.add(nueva_campania)
    db.session.commit()

    return "Campaña agregada satisfactoriamente"


@campania.route("/campania/get", methods=["GET"])
def obtener_campanias():
    campanias = Campania.query.all()
    campania_json = [
        {
            "id": campania.id,
            "titulo": campania.titulo,
            "descripcion": campania.descripcion,
        }
        for campania in campanias
    ]
    return jsonify(campania_json)

@campania.route("/campania/getById/<id>", methods=["GET"])
def obtener_campania_by_id(id):
    campania = Campania.query.filter_by(id=id).first()
    campania_json = {
           "id": campania.id,
           "titulo": campania.titulo,
           "descripcion": campania.descripcion,
        }
    return jsonify(campania_json)


@campania.route("/campania/put/<id>", methods=["PUT"])
def modificar_campania(id):
    campania = Campania.query.get(id)
    if not campania:
        return jsonify({"error": "Campaña no encontrada"}), 404

    # Obtén los nuevos datos del formulario o solicitud
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")

    # Actualiza los campos de la campaña existente
    campania.titulo = titulo
    campania.descripcion = descripcion

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Campaña actualizada satisfactoriamente"})


@campania.route("/campania/delete/<id>", methods=["DELETE"])
def eliminar_campania(id):
    campania = Campania.query.get(id)
    if not campania:
        return jsonify({"error": "Campaña no encontrada"}), 404

    db.session.delete(campania)
    db.session.commit()

    return jsonify({"message": "Campaña eliminada satisfactoriamente"})
