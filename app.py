from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os  # para criar a pasta static

# Inicializando o aplicativo Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veiculos.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar notificações de modificação
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

# Rota para a página inicial
@app.route('/')
def home():
    return redirect('/listar')  # Redireciona para a listagem de veículos

# Rota para listagem de veículos
@app.route('/listar')
def listar():
    veiculos = Veiculo.query.all()
    return render_template('listar.html', veiculos=veiculos)

# Rota para cadastro de veículos
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        ano = request.form['ano']
        placa = request.form['placa']
        cor = request.form['cor']
        observacao = request.form['observacao']
        veiculo = Veiculo(nome=nome, marca=marca, ano=ano, placa=placa, cor=cor, observacao=observacao)
        db.session.add(veiculo)
        db.session.commit()
        return redirect('/listar')
    return render_template('cadastro.html')

# Rota para editar um veículo
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    veiculo = Veiculo.query.get_or_404(id)
    if request.method == 'POST':
        veiculo.nome = request.form['nome']
        veiculo.marca = request.form['marca']
        veiculo.ano = request.form['ano']
        veiculo.placa = request.form['placa']
        veiculo.cor = request.form['cor']
        veiculo.observacao = request.form['observacao']
        db.session.commit()
        return redirect('/listar')
    return render_template('cadastro.html', veiculo=veiculo)

# Rota para excluir um veículo
@app.route('/excluir/<int:id>')
def excluir(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect('/listar')

# Rota para importar dados
@app.route('/importar', methods=['GET', 'POST'])
def importar():
    if request.method == 'POST':
        file = request.files['arquivo']
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
            for _, row in data.iterrows():
                veiculo = Veiculo(
                    nome=row['Nome'],
                    marca=row['Marca'],
                    ano=row['Ano'],
                    placa=row['Placa'],
                    cor=row['Cor'],
                    observacao=row.get('Observação', '')
                )
                db.session.add(veiculo)
            db.session.commit()
            return redirect('/listar')
    return render_template('importar.html')

# Rota para exportar dados
@app.route('/exportar')
def exportar():
    veiculos = Veiculo.query.all()
    data = [{'Nome': v.nome, 'Marca': v.marca, 'Ano': v.ano, 'Placa': v.placa, 'Cor': v.cor, 'Observação': v.observacao} for v in veiculos]
    df = pd.DataFrame(data)
    
    # Definindo o caminho para salvar o arquivo Excel
    file_path = 'static/veiculos.xlsx'
    
    # Criar a pasta 'static' se não existir
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Salvando o arquivo Excel na pasta static
    df.to_excel(file_path, index=False)
    
    # Redirecionando para o arquivo Excel na pasta 'static'
    return redirect(f'/{file_path}')

# Inicialização do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criação das tabelas do banco de dados
    app.run(debug=True, host='0.0.0.0', port=5001)
