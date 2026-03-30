from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Jogo(db.Model):
    __tablename__ = 'jogos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "plataforma": self.plataforma,
            "preco": self.preco,
            "estoque": self.estoque
        }


with app.app_context():
    db.create_all()



@app.route('/jogos', methods=['GET'])
def listar_jogos():
    jogos = Jogo.query.all()
    return jsonify([j.to_dict() for j in jogos]), 200


@app.route('/jogos/<int:id>', methods=['GET'])
def buscar_jogo(id):
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404
    return jsonify(jogo.to_dict()), 200


@app.route('/jogos', methods=['POST'])
def criar_jogo():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    novo_jogo = Jogo(
        titulo=dados.get('titulo'),
        plataforma=dados.get('plataforma'),
        preco=dados.get('preco'),
        estoque=dados.get('estoque')
    )
    db.session.add(novo_jogo)
    db.session.commit()
    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201

# PUT atualizar jogo
@app.route('/jogos/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    dados = request.get_json()
    jogo.titulo = dados.get('titulo')
    jogo.plataforma = dados.get('plataforma')
    jogo.preco = dados.get('preco')
    jogo.estoque = dados.get('estoque')
    db.session.commit()
    return jsonify({"mensagem": "Jogo atualizado com sucesso!"}), 200

@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    db.session.delete(jogo)
    db.session.commit()
    return jsonify({"mensagem": f"Jogo '{jogo.titulo}' removido!"}), 200

if __name__ == '__main__':
    app.run(debug=True)