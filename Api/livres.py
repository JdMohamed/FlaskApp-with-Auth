from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from Api.schemas import LivreSchema
from app import db
from models import Livre, Auteur

livre_bp = Blueprint('livres', __name__)


@livre_bp.post('/add_livre')
@jwt_required()
def add_livre():
    claims = get_jwt()
    if claims.get('is_staff') == True:
        data = request.get_json()
        print(data)
        print(data)
        new_livre = Livre(titre=data.get('titre'), nb_pages=data.get('nb_pages'))
        new_livre.save()
        auteurs=data.get('auteurs')
        print(auteurs)
        for auteur in auteurs:
            print(auteur)
            auteur_obj = Auteur.query.filter(Auteur.nom == auteur['nom']).first()
            new_livre.auteurs.append(auteur_obj)
            db.session.commit()

        return jsonify({"message": "Livre created"}), 201
    else:
        return jsonify({"message": "You dont have permission to access this !"}), 401


@livre_bp.get('/livres')
@jwt_required()
def get_all_livres():
    claims = get_jwt()
    if claims.get('is_staff') == True:
        livres = Livre.query.all()
        result = LivreSchema().dump(livres, many=True)

        return jsonify(result), 200
    else :
        return jsonify({"message": "You dont have permission to access this !"}), 401

