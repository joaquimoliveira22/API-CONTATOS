from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CRIAÇÃO DA TABELA DE CONTATOS.

class Contato(db.Model):
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100))
    apelido = db.Column(db.String(50))
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    ddd = db.Column(db.String(3), nullable=False)

    # Relacionamento com cascade delete
    historico = db.relationship(
        "HistoricoLigacao",
        backref="contato",
        lazy=True,
        cascade="all, delete-orphan"
    )


# CRIAÇÃO DA TABELA DE HISTORICO DE LIGAÇÕES.

class HistoricoLigacao(db.Model):
    __tablename__ = "historico_ligacoes"

    id = db.Column(db.Integer, primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey("contatos.id"), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    duracao_segundos = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "entrada" ou "saida"

# CONTATOS ===================================================================================================================
# CADASTRO DE CONTATOS.

@app.route("/contatos", methods=["POST"])
def criar_contato():
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
    return jsonify({"mensagem": "Contato criado com sucesso!"}), 201

# LISTAR CONTATOS.

@app.route("/contatos", methods=["GET"])
def listar_contatos():
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

# listar contatos por id

@app.route("/contatos/<int:id>", methods=["GET"])
def listar_contato(id):
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

# EDITAR CONTATO

@app.route("/contatos/<int:id>", methods=["PUT"])
def editar_contato(id):
    contato = Contato.query.get_or_404(id)  # 404 se nao existir
    dados = request.json

    contato.nome = dados.get("nome", contato.nome)
    contato.sobrenome = dados.get("sobrenome", contato.sobrenome)
    contato.apelido = dados.get("apelido", contato.apelido)
    contato.telefone = dados.get("telefone", contato.telefone)
    contato.email = dados.get("email", contato.email)
    contato.ddd = dados.get("ddd", contato.ddd)

    db.session.commit()
    return jsonify({"mensagem": f"Contato {id} atualizado com sucesso!"})

# DELETAR CONTATO

@app.route("/contatos/<int:id>", methods=["DELETE"])
def apagar_contato(id):
    contato = Contato.query.get_or_404(id)  # 404 se não existir
    db.session.delete(contato)
    db.session.commit()
    return jsonify({"mensagem": f"Contato {id} apagado com sucesso!"})

# LIGAÇÕES ==========================================================================================================
# CRIAR LIGAÇÕES.

@app.route("/ligacoes", methods=["POST"])
def registrar_ligacao():
    dados = request.json
    ligacao = HistoricoLigacao(
        contato_id=dados["contato_id"],
        duracao_segundos=dados["duracao_segundos"],
        tipo=dados["tipo"]
    )
    db.session.add(ligacao)
    db.session.commit()
    return jsonify({"mensagem": "Ligação registrada com sucesso!"}), 201

# LISTAR LIGAÇÕES + ID.
# Necessario o id do contato para pesquisa especifica do contato

@app.route("/ligacoes/<int:contato_id>", methods=["GET"])
def listar_ligacoes_id(contato_id):
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

# LISTAR TODAS AS LIGAÇÕES

@app.route("/ligacoes", methods=["GET"])
def listar_ligacoes():
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


# EDITAR LIGAÇÕES + ID

@app.route("/ligacoes/<int:id>", methods=["PUT"])
def editar_ligacao(id):
    ligacao = HistoricoLigacao.query.get_or_404(id)
    dados = request.json

    ligacao.duracao_segundos = dados.get("duracao_segundos", ligacao.duracao_segundos)
    ligacao.tipo = dados.get("tipo", ligacao.tipo)

    db.session.commit()
    return jsonify({"mensagem": f"Ligação {id} atualizada com sucesso!"})


# DELETAR LIGAÇÕES + ID

@app.route("/ligacoes/<int:id>", methods=["DELETE"])
def apagar_ligacao(id):
    ligacao = HistoricoLigacao.query.get_or_404(id)
    db.session.delete(ligacao)
    db.session.commit()
    return jsonify({"mensagem": f"Ligação {id} apagada com sucesso!"})


import os
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
