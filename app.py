from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Inicializando o aplicativo Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar modificações
db = SQLAlchemy(app)

# Modelo de dados (Tabela de Veículo)
class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(20), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.Text, nullable=True)

# Rota para a página inicial (home)
@app.route('/')
def home():
    return redirect('/cadastro')  # Redireciona para a página de cadastro de veículos

# Rota para cadastro de veículos
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Recebe os dados do formulário e cria um novo veículo
        nome = request.form['nome']
        marca = request.form['marca']
        ano = request.form['ano']
        placa = request.form['placa']
        cor = request.form['cor']
        observacao = request.form['observacao']
        veiculo = Veiculo(nome=nome, marca=marca, ano=ano, placa=placa, cor=cor, observacao=observacao)

        # Adiciona o novo veículo ao banco de dados
        db.session.add(veiculo)
        db.session.commit()

        # Redireciona para a página inicial após o cadastro
        return redirect('/')

    # Se for um GET, renderiza o formulário de cadastro
    return render_template('cadastro.html')

if __name__ == '__main__':
    # Criação do banco de dados (caso não exista)
    with app.app_context():
        db.create_all()

    # Rodando a aplicação na porta 5001 com SSL (caso tenha configurado)
    app.run(debug=True, host='0.0.0.0', port=5001, ssl_context=('flask.crt', 'flask.key'))  
