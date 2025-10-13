from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
import os
import secrets

app = Flask(__name__)

# =============================================================
# CONFIGURAÇÕES
# =============================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =============================================================
# MODELOS
# =============================================================

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)  # token dinâmico

class Contato(db.Model):
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100))
    apelido = db.Column(db.String(50))
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    ddd = db.Column(db.String(3), nullable=False)

    historico = db.relationship(
        "HistoricoLigacao",
        backref="contato",
        lazy=True,
        cascade="all, delete-orphan"
    )

class HistoricoLigacao(db.Model):
    __tablename__ = "historico_ligacoes"

    id = db.Column(db.Integer, primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey("contatos.id"), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    duracao_segundos = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "entrada" ou "saida"

# =============================================================
# DECORATOR DE AUTENTICAÇÃO (Bearer Token)
# =============================================================

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"erro": "Token não fornecido"}), 401
        
        partes = auth.split()
        if len(partes) != 2 or partes[0] != "Bearer":
            return jsonify({"erro": "Cabeçalho Authorization inválido"}), 401
        
        token = partes[1]
        usuario = Usuario.query.filter_by(token=token).first()
        if not usuario:
            return jsonify({"erro": "Token inválido"}), 403
        
        return f(usuario, *args, **kwargs)
    return decorated

# =============================================================
# ROTAS DE USUÁRIO
# =============================================================

@app.route("/registrar", methods=["POST"])
def registrar_usuario():
    dados = request.json

    if Usuario.query.filter_by(email=dados["email"]).first():
        return jsonify({"erro": "Email já cadastrado"}), 400

    token = secrets.token_hex(32)  # Gera token aleatório
    novo_usuario = Usuario(nome=dados["nome"], email=dados["email"], token=token)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "mensagem": "Usuário criado com sucesso!",
        "token": token
    }), 201

@app.route("/login", methods=["POST"])
def login_usuario():
    dados = request.json
    usuario = Usuario.query.filter_by(email=dados.get("email")).first()

    if usuario:
        return jsonify({
            "mensagem": f"Bem-vindo {usuario.nome}!",
            "token": usuario.token
        }), 200

    return jsonify({"erro": "Email não encontrado"}), 401

# =============================================================
# ROTAS DE CONTATOS
# =============================================================

@app.route("/contatos", methods=["POST"])
@token_obrigatorio
def criar_contato(usuario):
    dados = request.json
    novo = Contato(
        nome=dados["nome"],
        sobrenome=dados.get("sobrenome"),
        apelido=dados.get("apelido"),
        telefone=dados["telefone"],
        email=dados.get("email"),
        ddd=dados["ddd"]
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": f"Contato criado por {usuario.nome} com sucesso!"}), 201

@app.route("/contatos", methods=["GET"])
@token_obrigatorio
def listar_contatos(usuario):
    contatos = Contato.query.all()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "sobrenome": c.sobrenome,
            "apelido": c.apelido,
            "telefone": c.telefone,
            "email": c.email,
            "ddd": c.ddd
        } for c in contatos
    ])

@app.route("/contatos/<int:id>", methods=["GET"])
@token_obrigatorio
def listar_contato(usuario, id):
    contato = Contato.query.get_or_404(id)
    return jsonify({
        "id": contato.id,
        "nome": contato.nome,
        "sobrenome": contato.sobrenome,
        "apelido": contato.apelido,
        "telefone": contato.telefone,
        "email": contato.email,
        "ddd": contato.ddd
    })

@app.route("/contatos/<int:id>", methods=["PUT"])
@token_obrigatorio
def editar_contato(usuario, id):
    contato = Contato.query.get_or_404(id)
    dados = request.json

    contato.nome = dados.get("nome", contato.nome)
    contato.sobrenome = dados.get("sobrenome", contato.sobrenome)
    contato.apelido = dados.get("apelido", contato.apelido)
    contato.telefone = dados.get("telefone", contato.telefone)
    contato.email = dados.get("email", contato.email)
    contato.ddd = dados.get("ddd", contato.ddd)

    db.session.commit()
    return jsonify({"mensagem": f"Contato {id} atualizado com sucesso!"})

@app.route("/contatos/<int:id>", methods=["DELETE"])
@token_obrigatorio
def apagar_contato(usuario, id):
    contato = Contato.query.get_or_404(id)
    db.session.delete(contato)
    db.session.commit()
    return jsonify({"mensagem": f"Contato {id} apagado com sucesso!"})

# =============================================================
# ROTAS DE LIGAÇÕES
# =============================================================

@app.route("/ligacoes", methods=["POST"])
@token_obrigatorio
def registrar_ligacao(usuario):
    dados = request.json
    ligacao = HistoricoLigacao(
        contato_id=dados["contato_id"],
        duracao_segundos=dados["duracao_segundos"],
        tipo=dados["tipo"]
    )
    db.session.add(ligacao)
    db.session.commit()
    return jsonify({"mensagem": f"Ligação registrada por {usuario.nome} com sucesso!"}), 201

@app.route("/ligacoes/<int:contato_id>", methods=["GET"])
@token_obrigatorio
def listar_ligacoes_id(usuario, contato_id):
    ligacoes = HistoricoLigacao.query.filter_by(contato_id=contato_id).all()
    return jsonify([
        {
            "id": l.id,
            "contato_id": l.contato_id,
            "data_hora": l.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "duracao_segundos": l.duracao_segundos,
            "tipo": l.tipo
        } for l in ligacoes
    ])

@app.route("/ligacoes", methods=["GET"])
@token_obrigatorio
def listar_ligacoes(usuario):
    ligacoes = HistoricoLigacao.query.all()
    return jsonify([
        {
            "id": l.id,
            "contato_id": l.contato_id,
            "data_hora": l.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "duracao_segundos": l.duracao_segundos,
            "tipo": l.tipo
        } for l in ligacoes
    ])

@app.route("/ligacoes/<int:id>", methods=["PUT"])
@token_obrigatorio
def editar_ligacao(usuario, id):
    ligacao = HistoricoLigacao.query.get_or_404(id)
    dados = request.json

    ligacao.duracao_segundos = dados.get("duracao_segundos", ligacao.duracao_segundos)
    ligacao.tipo = dados.get("tipo", ligacao.tipo)

    db.session.commit()
    return jsonify({"mensagem": f"Ligação {id} atualizada com sucesso!"})

@app.route("/ligacoes/<int:id>", methods=["DELETE"])
@token_obrigatorio
def apagar_ligacao(usuario, id):
    ligacao = HistoricoLigacao.query.get_or_404(id)
    db.session.delete(ligacao)
    db.session.commit()
    return jsonify({"mensagem": f"Ligação {id} apagada com sucesso!"})

# =============================================================
# ERROS
# =============================================================

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return jsonify({"erro": "Página não encontrada"}), 404

@app.errorhandler(400)
def erro_requisicao_invalida(e):
    return jsonify({"erro": "Requisição inválida"}), 400

@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"erro": "Erro interno do servidor"}), 500

# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
