from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from Api.schemas import AuteurSchema

from models import Auteur, Livre
auteur_bp = Blueprint('auteurs', __name__)


@auteur_bp.post('/add_auteur')
@jwt_required()
def add_auteur():
    data = request.get_json()
    new_auteur = Auteur(nom=data.get('nom'))
    new_auteur.save()
    if data['livres'] !='':
        for l in data['livres']:
            livre = Livre.query.filter(Livre.titre==l)
            new_auteur.livres.append(livre)

    return jsonify({"message": "Auteur created"}), 201

@auteur_bp.get('/auteurs')
@jwt_required()
def get_auteurs():
    claims = get_jwt()
    if claims.get('is_staff') == True:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)
        auteurs = Auteur.query.paginate(
            page=page,
            per_page=per_page
        )
        result = AuteurSchema().dump(auteurs, many=True)

        return jsonify(
            result
        ), 200
    else:
        return jsonify({"message": "You dont have permission to access this !"}), 401