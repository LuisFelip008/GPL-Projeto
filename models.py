from flask_sqlalchemy import SQLAlchemy

# Inicializando o banco de dados
db = SQLAlchemy()

# Modelo de dados (Tabela de Veículo)
class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(20), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.Text, nullable=True)
