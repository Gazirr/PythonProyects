from flask import jsonify, request,Blueprint
from .models import Alumno
from .db import db 

bp = Blueprint('api', __name__)



@bp.route('/alumnos', methods =['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    return jsonify([a.to_dict() for a in alumnos]), 200

@bp.route('/alumnos/<int:alumno_id>', methods=['GET'])
def get_alumno(alumno_id):
    alumno = Alumno.query.get(alumno_id)

    if not alumno:
        return jsonify({"error":"Alumno no encontrado"}), 404
    
    return jsonify(alumno.to_dict()), 200

@bp.route('/alumnos', methods=['POST'])
def create_alumno():
    data = request.get_json()
    if not data: 
        return jsonify({"error": "Se requiere json"}), 400
    
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    edad = data.get('edad')

    if not nombre or not apellido or edad is None:
        return jsonify({"error": "Faltan Campos: nombre, apellido, edad"}), 400
    
    nuevo = Alumno(nombre=nombre,apellido=apellido, edad=edad)

    db.session.add(nuevo)

    db.session.commit()

    return jsonify(nuevo.to_dict()), 201


@bp.route('/alumnos/<int:alumno_id>', methods = ['PUT'])
def update_alumno(alumno_id):
    alumno = Alumno.query.get(alumno_id)

    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    data = request.get_json()

    if not data:
        return jsonify({"Error": "Se requiere JSON"}), 400
    
    alumno.nombre = data.get('nombre', alumno.nombre)
    alumno.apellido = data.get('apellido', alumno.apellido)
    alumno.edad = data.get('edad', alumno.edad)

    db.session.commit()

    return jsonify(alumno.to_dict()), 200

@bp.route('alumnos/<int:alumno_id>', methods = ['DELETE'])
def delete_alumno(alumno_id):
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"Error": "Alumno no encontrado"}), 404
    
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"message": "Alumno eliminado"}), 200
