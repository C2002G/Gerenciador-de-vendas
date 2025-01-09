from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

# Função para criar conexão com o banco
def criar_conexao():
    try:
        conn = sqlite3.connect('carros.db')
        return conn
    except Error as e:
        print(e)
    return None

# Função para criar a tabela de carros
def criar_tabela():
    conn = criar_conexao()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS carros (
                    placa TEXT PRIMARY KEY,
                    renavan TEXT,
                    cor TEXT,
                    valor_fip REAL,
                    valor_compra REAL,
                    despesas REAL,
                    local_compra TEXT,
                    vendedor TEXT,
                    telefone_vendedor TEXT,
                    venda TEXT,
                    comprador TEXT,
                    valor_venda REAL,
                    tipo_venda TEXT,
                    cliente_nome TEXT,
                    cliente_cpf TEXT,
                    cliente_endereco TEXT,
                    dut_ok BOOLEAN DEFAULT 0
                )
            ''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

# Criar a tabela quando iniciar a aplicação
criar_tabela()

@app.route("/")
def index():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carros')
    carros_db = cursor.fetchall()
    conn.close()

    # Converter resultado do banco para lista de dicionários
    carros = []
    for carro in carros_db:
        carros.append({
            'placa': carro[0],
            'renavan': carro[1],
            'cor': carro[2],
            'valor_fip': carro[3],
            'valor_compra': carro[4],
            'despesas': carro[5],
            'local_compra': carro[6],
            'vendedor': carro[7],
            'telefone_vendedor': carro[8],
            'venda': carro[9],
            'comprador': carro[10],
            'valor_venda': carro[11],
            'tipo_venda': carro[12],
            'cliente_nome': carro[13],
            'cliente_cpf': carro[14],
            'cliente_endereco': carro[15],
            'dut_ok': bool(carro[16])
        })
    return render_template("index.html", carros=carros)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO carros (
                placa, renavan, cor, valor_fip, valor_compra, despesas,
                local_compra, vendedor, telefone_vendedor, venda,
                comprador, valor_venda, tipo_venda, cliente_nome,
                cliente_cpf, cliente_endereco, dut_ok
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['placa'],
            request.form['renavan'],
            request.form['cor'],
            request.form['valor_fip'],
            request.form['valor_compra'],
            request.form['despesas'],
            request.form['local_compra'],
            request.form['vendedor'],
            request.form['telefone_vendedor'],
            request.form['venda'],
            request.form['comprador'],
            request.form['valor_venda'],
            request.form['tipo_venda'],
            request.form['cliente_nome'],
            request.form['cliente_cpf'],
            request.form['cliente_endereco'],
            False
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastrar.html')

@app.route('/toggle_dut/<placa>', methods=['POST'])
def toggle_dut(placa):
    conn = criar_conexao()
    cursor = conn.cursor()
    # Primeiro, pegamos o valor atual
    cursor.execute('SELECT dut_ok FROM carros WHERE placa = ?', (placa,))
    atual = cursor.fetchone()
    if atual is not None:
        novo_valor = not bool(atual[0])
        cursor.execute('UPDATE carros SET dut_ok = ? WHERE placa = ?', 
                      (novo_valor, placa))
        conn.commit()
        conn.close()
        return {'status': 'success', 'dut_ok': novo_valor}
    conn.close()
    return {'status': 'error'}, 404
@app.route('/carro/<placa>')
def detalhes_carro(placa):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carros WHERE placa = ?', (placa,))
    carro_db = cursor.fetchone()
    conn.close()

    if carro_db is None:
        return redirect(url_for('index'))

    carro = {
        'placa': carro_db[0],
        'renavan': carro_db[1],
        'cor': carro_db[2],
        'valor_fip': carro_db[3],
        'valor_compra': carro_db[4],
        'despesas': carro_db[5],
        'local_compra': carro_db[6],
        'vendedor': carro_db[7],
        'telefone_vendedor': carro_db[8],
        'venda': carro_db[9],
        'comprador': carro_db[10],
        'valor_venda': carro_db[11],
        'tipo_venda': carro_db[12],
        'cliente_nome': carro_db[13],
        'cliente_cpf': carro_db[14],
        'cliente_endereco': carro_db[15],
        'dut_ok': bool(carro_db[16])
    }

    return render_template('detalhes_carro.html', carro=carro)

@app.route('/carro/<placa>/editar', methods=['GET', 'POST'])
def editar_carro(placa):
    conn = criar_conexao()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            UPDATE carros SET 
                placa = ?, renavan = ?, cor = ?, valor_fip = ?, 
                valor_compra = ?, despesas = ?, local_compra = ?,
                vendedor = ?, telefone_vendedor = ?, venda = ?,
                comprador = ?, valor_venda = ?, tipo_venda = ?,
                cliente_nome = ?, cliente_cpf = ?, cliente_endereco = ?
            WHERE placa = ?
        ''', (
            request.form['placa'],
            request.form['renavan'],
            request.form['cor'],
            request.form['valor_fip'],
            request.form['valor_compra'],
            request.form['despesas'],
            request.form['local_compra'],
            request.form['vendedor'],
            request.form['telefone_vendedor'],
            request.form['venda'],
            request.form['comprador'],
            request.form['valor_venda'],
            request.form['tipo_venda'],
            request.form['cliente_nome'],
            request.form['cliente_cpf'],
            request.form['cliente_endereco'],
            placa
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('detalhes_carro', placa=request.form['placa']))

    cursor.execute('SELECT * FROM carros WHERE placa = ?', (placa,))
    carro_db = cursor.fetchone()
    conn.close()

    if carro_db is None:
        return redirect(url_for('index'))

    carro = {
        'placa': carro_db[0],
        'renavan': carro_db[1],
        'cor': carro_db[2],
        'valor_fip': carro_db[3],
        'valor_compra': carro_db[4],
        'despesas': carro_db[5],
        'local_compra': carro_db[6],
        'vendedor': carro_db[7],
        'telefone_vendedor': carro_db[8],
        'venda': carro_db[9],
        'comprador': carro_db[10],
        'valor_venda': carro_db[11],
        'tipo_venda': carro_db[12],
        'cliente_nome': carro_db[13],
        'cliente_cpf': carro_db[14],
        'cliente_endereco': carro_db[15],
        'dut_ok': bool(carro_db[16])
    }

    return render_template('editar_carro.html', carro=carro)

@app.route('/carro/<placa>/apagar', methods=['POST'])
def apagar_carro(placa):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carros WHERE placa = ?', (placa,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)