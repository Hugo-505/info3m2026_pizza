from utils import db

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __init__(self, nome, email, senha, admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
    
    def __repr__(self):
        return "<Usuario {}>".format(self.nome)

class Pizza(db.Model):
    __tablename__= "pizza"
    id = db.Column(db.Integer, primary_key = True)
    sabor = db.Column(db.String(100))
    preco = db.Column(db.Float)

    def __init__(self, sabor, preco):
        self.sabor = sabor
        self.preco = preco
    
    def __repr__(self):
        return "<Pizza {}>".format(self.sabor)