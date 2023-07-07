from flask import Blueprint, jsonify, request
from models.MCampania import Campania
from utils.db import db

campania = Blueprint('campania', __name__)


@campania.route("/campania/add", methods=["POST"])
def agregar_campania():
    titulo = request.json.get("titulo")
    descripcion = request.json.get("descripcion")

    campanias = Campania.query.all()
    for campania in campanias:
        campania.seleccionada = False

    nueva_campania = Campania(titulo=titulo, descripcion=descripcion, seleccionada=True)
    db.session.add(nueva_campania)
    db.session.commit()

    return jsonify({"message":"Campaña agregada satisfactoriamente"})


@campania.route("/campania/get", methods=["GET"])
def obtener_campanias():
    campanias = Campania.query.all()
    campania_json = [
        {
            "id": campania.id,
            "titulo": campania.titulo,
            "descripcion": campania.descripcion,
            "seleccionada": campania.seleccionada,
            "donaciones":  [donacion.to_dict() for donacion in campania.donaciones]
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
           "seleccionada": campania.seleccionada,
           "donaciones":  [donacion.to_dict() for donacion in campania.donaciones]
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

@campania.route("/campania/getByTitulo/<titulo>", methods=["GET"])
def obtener_por_titulo(titulo):
    campania = Campania.query.filter_by(titulo=titulo).first()

    if not campania:
        return jsonify({"error": "Campaña no encontrada"}), 404
    
    campania_json = [
        {
            "id": campania.id,
            "titulo": campania.titulo,
            "descripcion": campania.descripcion,
            "seleccionada": campania.seleccionada,
            "donaciones":  [donacion.to_dict() for donacion in campania.donaciones]
        }
    ]

    return jsonify(campania_json)

@campania.route("/campania/seleccionarCampaña/<id>", methods=["GET"])
def seleccionar_campania(id):

    campanias = Campania.query.all()
    for campania in campanias:
        campania.seleccionada = False

    campania = Campania.query.get(id)
    if not campania:
        return jsonify({"error": "Campaña no encontrada"}), 404

    seleccionada = True

    # Actualiza los campos de la campaña existente
    campania.seleccionada = seleccionada

    # Guarda los cambios en la base de datos
    db.session.commit()

    campania_json = [
        {
            "id": campania.id,
            "titulo": campania.titulo,
            "descripcion": campania.descripcion,
            "seleccionada": campania.seleccionada,
            "donaciones":  [donacion.to_dict() for donacion in campania.donaciones]
        }
        for campania in campanias
    ]
    return jsonify(campania_json)

@campania.route("/campania/getCampaniaSeleccionada", methods=["GET"])
def obtener_campania_seleccionada():
    campania = Campania.query.filter_by(seleccionada=True).first()

    if not campania:
        return jsonify({"error": "Campaña no encontrada"})
    
    campania_json = [
        {
            "id": campania.id,
            "titulo": campania.titulo,
            "descripcion": campania.descripcion,
            "seleccionada": campania.seleccionada,
            "donaciones":  [donacion.to_dict() for donacion in campania.donaciones]
        }
    ]

    return jsonify(campania_json)