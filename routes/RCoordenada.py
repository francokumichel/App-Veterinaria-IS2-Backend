from flask import Blueprint, jsonify, request
from models.MCoordenada import Coordenada
from utils.db import db
import math

coordenada = Blueprint('coordenada', __name__)


@coordenada.route("/coordenada/add", methods=["POST"])
def agregar_coordenada():
    coordenadaX = request.json.get("coordenadaX")
    coordenadaY = request.json.get("coordenadaY")
    titulo = request.json.get("titulo")
    parrafo = request.json.get("parrafo")

    coordenadas = Coordenada.query.all()
    for coordenada in coordenadas:
        if math.dist([coordenadaX, coordenadaY], [coordenada.coordenadaX, coordenada.coordenadaY]) < 1:
            return jsonify({"error": "Ya existe una coordenada en ese lugar. Por favor cambialo." })

    nueva_coordenada = Coordenada(coordenadaX=coordenadaX, coordenadaY=coordenadaY, titulo=titulo, parrafo=parrafo)
    db.session.add(nueva_coordenada)
    db.session.commit()

    return "Coordenada agregada satisfactoriamente"


@coordenada.route("/coordenada/get", methods=["GET"])
def obtener_coordenadas():
    coordenadas = Coordenada.query.all()
    coordenada_json = [
        {
            "id": coordenada.id,
            "coordenadaX": coordenada.coordenadaX,
            "coordenadaY": coordenada.coordenadaY,
            "titulo": coordenada.titulo,
            "parrafo": coordenada.parrafo
        }
        for coordenada in coordenadas
    ]
    return jsonify(coordenada_json)

@coordenada.route("/coordenada/getById/<id>", methods=["GET"])
def obtener_coordenada_by_id(id):
    coordenada = Coordenada.query.filter_by(id=id).first()
    if not coordenada:
        return jsonify({"error": "Coordenada no encontrada"})
    
    coordenada_json = {
           "id": coordenada.id,
            "coordenadaX": coordenada.coordenadaX,
            "coordenadaY": coordenada.coordenadaY,
            "titulo": coordenada.titulo,
            "parrafo": coordenada.parrafo
        }
    return jsonify(coordenada_json)


@coordenada.route("/coordenada/put/<id>", methods=["PUT"])
def modificar_coordenada(id):
    coordenada = Coordenada.query.get(id)
    if not coordenada:
        return jsonify({"error": "Coordenada no encontrada"})
    
    coordenadas = Coordenada.query.all()
    for coordenada in coordenadas:
        if math.dist([coordenadaX, coordenadaY], [coordenada.coordenadaX, coordenada.coordenadaY]) < 1:
            return jsonify({"error": "Ya existe una coordenada en ese lugar. Por favor cambialo." })

    # Obtén los nuevos datos del formulario o solicitud
    coordenadaX = request.json.get("coordenadaX")
    coordenadaY = request.json.get("coordenadaY")
    titulo = request.json.get("titulo")
    parrafo = request.json.get("parrafo")

    # Actualiza los campos de la campaña existente
    coordenada.coordenadaX = coordenadaX
    coordenada.coordenadaY = coordenadaY
    coordenada.titulo = titulo
    coordenada.parrafo = parrafo

    # Guarda los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Coordenada actualizada satisfactoriamente"})


@coordenada.route("/coordenada/delete/<id>", methods=["DELETE"])
def eliminar_coordenada(id):
    coordenada = Coordenada.query.get(id)
    if not coordenada:
        return jsonify({"error": "Coordenada no encontrada"}), 404

    db.session.delete(coordenada)
    db.session.commit()

    return jsonify({"message": "Coordenada eliminada satisfactoriamente"})