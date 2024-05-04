from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import request, Blueprint, jsonify
from models import User, TokenBlockList
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                current_user,
                                get_jwt_identity, get_jwt)

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get('username'))

    if user is not None:
        return jsonify({"error": "User already exist"}), 403
    else:
        hashed_password = generate_password_hash(data.get('password'))
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=hashed_password,
            role=data.get('role'))
        new_user.save()
        return jsonify({"message": "User created"}), 201


@auth_bp.post('/login')
def login():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    if user and (check_password_hash(user.password, data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify(
            {
                "message": "logged In",
                "tokens": {
                    "access": access_token,
                    "refresh": refresh_token
                }

            }
        ), 200
    return jsonify({"error": "Invalid username or password"}), 400


@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({"User details": {"user": current_user.username, "email": current_user.email}})


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token":new_access_token})

@auth_bp.get('/logout')
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()
    jti = jwt['jti']

    token_obj = TokenBlockList(jti=jti)

    token_obj.save()

    return jsonify({"message":"Logged Out Successfully"}),200



