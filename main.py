from flask import Flask, render_template, request, redirect, url_for

app= Flask(__name__)  




@app.route("/")
def index():
  return render_template("index.html", carros=carros)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar()
  if request.method == 'POST'
    carro = {
        'placa': request.form['placa'],
        'renavan': request.form['renavan'],
        'cor': request.form['cor'],
        'valor_fip': request.form['valor_fip'],
        'valor_compra': request.form['valor_compra'],
        'despesas': request.form['despesas'],
        'local_compra': request.form['local_compra'],
        'vendedor': request.form['vendedor'],
        'telefone_vendedor': request.form['telefone_vendedor'],
        'venda': request.form['venda'],
        'comprador': request.form['comprador'],
        'valor_venda': request.form['valor_venda'],
        'tipo_venda': request.form['tipo_venda'],
        'cliente_nome': request.form['cliente_nome'],
        'cliente_cpf': request.form['cliente_cpf'],
        'cliente_endereco': request.form['cliente_endereco']
    }
    carros.append(carro)
    return redirect(url_for('index'))
  return render_template('cadastrar.html')

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8080)