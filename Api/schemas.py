from marshmallow import fields, Schema
class UserSchema(Schema):
    uid = fields.String()
    username = fields.String()
    email = fields.String()
    role = fields.String()
class AuteurSchema(Schema):
    id = fields.String()
    nom = fields.String()
    #livres = fields.List(fields.Nested(LivreSchema()), dump_only=True)

class LivreSchema(Schema):
    id=fields.Integer()
    titre=fields.String()
    nb_pages=fields.String()
    auteurs = fields.List(fields.Nested(AuteurSchema()), dump_only=True)
