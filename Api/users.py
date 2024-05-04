from flask import Blueprint, request, jsonify
from models import User
from Api.schemas import UserSchema
from flask_jwt_extended import jwt_required,get_jwt
user_bp = Blueprint('users', __name__)


@user_bp.get('/users')
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims.get('is_staff') == True:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)
        users = User.query.paginate(
            page=page,
            per_page=per_page
        )
        result = UserSchema().dump(users,many=True)


        return jsonify(
            result
        ),200
    else:
        return jsonify({"message":"You dont have permission to access this !"}),401


@user_bp.get('/<uid>')
def get_user(uid):
    user = User.query.filter(User.uid==uid).first()
    if user is not None:
        result = UserSchema().dump(user)
        return jsonify(result),200
    else:
        return jsonify({""
                        "message":"User Not Found"}),404


