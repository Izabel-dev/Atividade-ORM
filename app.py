from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Inicializa o Flask
app = Flask(__name__)

# Configurações do banco de dados SQLite via SQLAlchemy (ORM)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogos.db'  # caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False           # desativa warnings
db = SQLAlchemy(app)  # cria o objeto ORM

# Definição da tabela 'jogos' como classe Python (ORM)
class Jogo(db.Model):
    __tablename__ = 'jogos'                 # nome da tabela
    id = db.Column(db.Integer, primary_key=True)  # chave primária
    titulo = db.Column(db.String(100), nullable=False)  # título do jogo
    plataforma = db.Column(db.String(50), nullable=False)  # plataforma do jogo
    preco = db.Column(db.Float, nullable=False)           # preço
    estoque = db.Column(db.Integer, nullable=False)      # quantidade em estoque

    # Método para transformar objeto em dicionário JSON
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "plataforma": self.plataforma,
            "preco": self.preco,
            "estoque": self.estoque
        }

# Cria as tabelas no banco automaticamente se não existirem
with app.app_context():
    db.create_all()

# ------------------- ROTAS -------------------

# GET /jogos - Lista todos os jogos
@app.route('/jogos', methods=['GET'])
def listar_jogos():
    # ORM: busca todos os registros da tabela
    jogos = Jogo.query.all()
    # Retorna JSON com todos os jogos
    return jsonify([j.to_dict() for j in jogos]), 200

# GET /jogos/<id> - Busca um jogo específico pelo ID
@app.route('/jogos/<int:id>', methods=['GET'])
def buscar_jogo(id):
    # ORM: busca pelo ID
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404
    return jsonify(jogo.to_dict()), 200

# POST /jogos - Cria um novo jogo
@app.route('/jogos', methods=['POST'])
def criar_jogo():
    dados = request.get_json()
    # Validação de JSON
    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    # ORM: cria objeto Python e adiciona ao banco
    novo_jogo = Jogo(
        titulo=dados.get('titulo'),
        plataforma=dados.get('plataforma'),
        preco=dados.get('preco'),
        estoque=dados.get('estoque')
    )
    db.session.add(novo_jogo)  # adiciona à sessão
    db.session.commit()         # salva alterações
    return jsonify({"mensagem": "Jogo criado com sucesso!"}), 201

# PUT /jogos/<id> - Atualiza um jogo existente
@app.route('/jogos/<int:id>', methods=['PUT'])
def atualizar_jogo(id):
    # ORM: busca pelo ID
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    dados = request.get_json()
    # Atualiza os atributos do objeto
    jogo.titulo = dados.get('titulo')
    jogo.plataforma = dados.get('plataforma')
    jogo.preco = dados.get('preco')
    jogo.estoque = dados.get('estoque')
    db.session.commit()  # salva alterações
    return jsonify({"mensagem": "Jogo atualizado com sucesso!"}), 200

# DELETE /jogos/<id> - Deleta um jogo
@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletar_jogo(id):
    # ORM: busca pelo ID
    jogo = Jogo.query.get(id)
    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    db.session.delete(jogo)  # remove da sessão
    db.session.commit()       # salva alterações
    return jsonify({"mensagem": f"Jogo '{jogo.titulo}' removido!"}), 200

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

