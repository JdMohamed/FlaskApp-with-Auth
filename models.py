from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User : {self.username}, Role : {self.role}>'

    def get_id(self):
        return self.uid

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlockList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=True)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<Token {self.jti}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


auteur_livre = db.Table(
  'auteur_livre',
  db.Column('auteur_id', db.Integer, db.ForeignKey('auteur.id')),
  db.Column('livre_id', db.Integer, db.ForeignKey('livre.id'))
)


class Auteur(db.Model):
    __tablename__ = 'auteur'
    id = db.Column(db.Integer(), primary_key=True)
    nom = db.Column(db.String(), nullable=False)
    #livres = db.relationship('Livre', secondary='auteur_livre', backref='livres')

    def __repr__(self):
        return f"{self.nom}"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Livre(db.Model):
    __tablename__ = 'livre'

    id = db.Column(db.Integer(), primary_key=True)
    titre = db.Column(db.String(), nullable=False)
    nb_pages = db.Column(db.String(), nullable=False)
    auteurs = db.relationship('Auteur', secondary='auteur_livre', backref='auteurs')
    def __repr__(self):
        return f"{self.titre}"

    def save(self):
        db.session.add(self)
        db.session.commit()


