from flask import Blueprint, jsonify, request
from models.MVeterinaria import Veterinaria
from utils.db import db
import math

veterinaria = Blueprint('veterinaria', __name__)


@veterinaria.route("/veterinaria/add", methods=["POST"])
def agregar_veterinaria():
    coordenadaX = request.json.get("coordenadaX")
    coordenadaY = request.json.get("coordenadaY")
    titulo = request.json.get("titulo")
    parrafo = request.json.get("parrafo")

    nueva_veterinaria = Veterinaria(coordenadaX=coordenadaX, coordenadaY=coordenadaY, titulo=titulo, parrafo=parrafo)
    db.session.add(nueva_veterinaria)
    db.session.commit()

    return jsonify({"message": "Veterinaria agregada satisfactoriamente"})


@veterinaria.route("/veterinaria/get", methods=["GET"])
def obtener_veterinarias():
    veterinarias = Veterinaria.query.all()
    veterinaria_json = [
        {
            "id": veterinaria.id,
            "coordenadaX": veterinaria.coordenadaX,
            "coordenadaY": veterinaria.coordenadaY,
            "titulo": veterinaria.titulo,
            "parrafo": veterinaria.parrafo
        }
        for veterinaria in veterinarias
    ]
    return jsonify(veterinaria_json)

@veterinaria.route("/veterinaria/getById/<id>", methods=["GET"])
def obtener_veterinaria_by_id(id):
    veterinaria = Veterinaria.query.filter_by(id=id).first()
    if not veterinaria:
        return jsonify({"error": "Veterinaria no encontrada"})
    
    veterinaria_json = {
           "id": veterinaria.id,
            "coordenadaX": veterinaria.coordenadaX,
            "coordenadaY": veterinaria.coordenadaY,
            "titulo": veterinaria.titulo,
            "parrafo": veterinaria.parrafo
        }
    return jsonify(veterinaria_json)


@veterinaria.route("/veterinaria/put/<id>", methods=["PUT"])
def modificar_veterinaria(id):
    veterinaria = Veterinaria.query.get(id)
    if not veterinaria:
        return jsonify({"error": "Veterinaria no encontrada"})


    # Obtén los nuevos datos del formulario o solicitud
    coordenadaX = request.json.get("coordenadaX")
    coordenadaY = request.json.get("coordenadaY")
    titulo = request.json.get("titulo")
    parrafo = request.json.get("parrafo")

    # Actualiza los campos de la campaña existente
    veterinaria.coordenadaX = coordenadaX
    veterinaria.coordenadaY = coordenadaY
    veterinaria.titulo = titulo
    veterinaria.parrafo = parrafo

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Veterinaria actualizada satisfactoriamente"})


@veterinaria.route("/veterinaria/delete/<id>", methods=["DELETE"])
def eliminar_veterinaria(id):
    veterinaria = Veterinaria.query.get(id)
    if not veterinaria:
        return jsonify({"error": "Veterinaria no encontrada"}), 404

    db.session.delete(veterinaria)
    db.session.commit()

    return jsonify({"message": "Veterinaria eliminada satisfactoriamente"})