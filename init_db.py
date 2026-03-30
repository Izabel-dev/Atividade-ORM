from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Jogo(db.Model):
    id = db.Column(db.Integer, primapipry_key=True)
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
    db.create_all()  # Cria a tabela automaticamente

