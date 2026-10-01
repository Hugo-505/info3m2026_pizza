import os
import json
from flask import Flask, render_template, jsonify, redirect
from flask_login import current_user
from utils import db, lm
from flask_migrate import Migrate
from models import Usuario, Pizza
from controllers.Usuario import bp_usuarios

app = Flask(__name__)
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_usuario = os.getenv('DB_USERNAME')
db_senha = os.getenv('DB_PASSWORD')
db_mydb = os.getenv('DB_DATABASE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Conexão MySQL
conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}:{db_port}/{db_mydb}?unix_socket=/var/run/mysqld/mysqld.sock"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)


@app.route("/teste/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    lista_usuarios = [
        {"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios
    ]
    return jsonify(lista_usuarios), 200


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('index.html')


@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')


@app.route('/faleconosco')
def faleconosco():
    return render_template('faleconosco.html')


@app.route('/avaliacoes')
def avaliacoes():
    return render_template('avaliacoes.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/teste_insert')
def teste_insert():
    db.create_all()
    user = Usuario("Gabriel", "gabriel@ifrn.edu.br", "54321")
    db.session.add(user)
    db.session.commit()
    return 'Dados inseridos com sucesso!'


@app.route('/teste_select')
def teste_select():
    users = Usuario.query.all()
    for u in users:
        print(u.nome)

    user = Usuario.query.get(2)
    if user:
        print(f"O email do usuário de id 2 é {user.email}")

    return 'dados recuperados'


@app.route('/teste_update')
def teste_update():
    user = Usuario.query.get(1)
    if user:
        user.nome = "Alba L."
        user.senha = "753951"
        db.session.add(user)
        db.session.commit()
    return 'dados alterados com sucesso!'


@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 404


# O app.run DEVE estar protegido dentro deste bloco para não travar os comandos do terminal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)