from flask import Flask, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from os import environ
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    app.config['FLASK_SECRET_KEY'] = 'RGLMOPZSCHETTZAFQSRT'
    app.config['FLASK_JWT_SECRET_KEY'] = '1ee0f512c1ce0a66ddd6d548'
    app.secret_key = 'SecretKey'

    db.init_app(app)
    jwt.init_app(app)

    from models import User,TokenBlockList

    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    from Api import routes, users, auteurs, livres
    app.register_blueprint(routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(users.user_bp, url_prefix='/user')
    app.register_blueprint(auteurs.auteur_bp, url_prefix='/auteur')
    app.register_blueprint(livres.livre_bp, url_prefix='/livre')

    # load user

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_headers,jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()

    # additional claims

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        user=User.query.filter_by(username=identity).one_or_none()
        print(user.role)
        if user.role == "admin":
            return {"is_staff": True}
        return {"is_staff": False}

    # jwt error handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed", "error": "invalid token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Request doesnt contain valid token", "error": "Authorization required"}), 401
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_headers,jwt_data):
        jti = jwt_data['jti']

        token =db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()
        return token is not None

    migrate = Migrate(app, db)

    return app
