from datetime import datetime
from flask import Flask, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import mysql.connector
from functools import wraps

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'mp,86'

# Configuração do banco de dados
minha_conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='projeto_grao'
)


# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = minha_conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE email = %s", (email,))
        result = cursor.fetchall()
        cursor.close()

        print(f'email: {email}')
        print(f'senha: {senha}')
        print(f'result: {result}')

        if result:
            session['email'] = email  # Adiciona o email na sessão
            return redirect('/')
        else:
            return render_template('login.html', error='Email ou senha incorretos')

    return render_template('login.html')


# Exige login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return decorated_function


# Pagina Inicial
@app.route('/', methods=['GET', 'POST'])
@login_required
def inicio():
    return render_template('inicio.html')


# Página de cadastros
@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def homepage():
    form_type = request.form['form_type'] if request.method == 'POST' else ''

    if request.method == 'POST':
        if form_type == 'produtores':
            nome_prod = request.form['nome_prod']
            endereco = request.form['endereco']
            cpf = request.form['cpf']
            telefone = request.form['telefone']
            email = request.form['email']

            cur = minha_conexao.cursor()
            cur.execute(
                "INSERT INTO produtores (nome_prod, endereco, cpf, telefone, email) VALUES (%s, %s, %s, %s, %s)",
                (nome_prod, endereco, cpf, telefone, email))
            minha_conexao.commit()
            cur.close()
            return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Cadastro ' \
                   'efetuado com sucesso! <a href="/homepage">Novo cadastro</a> </br><a ' \
                   'href="/gerenciar_cadastros">Gerenciar cadastros</a></p</body> '

        elif form_type == 'motoristas':
            nome_motorista = request.form['nome_motorista']
            cpf_motorista = request.form['cpf_motorista']
            telefone_motorista = request.form['telefone_motorista']

            cur = minha_conexao.cursor()
            cur.execute(
                "INSERT INTO motoristas (nome_motorista, cpf_motorista, telefone_motorista) VALUES (%s, %s, %s)",
                (nome_motorista, cpf_motorista, telefone_motorista))
            minha_conexao.commit()
            cur.close()
            return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Cadastro ' \
                   'efetuado com sucesso! <a href="/homepage">Novo cadastro</a> </br><a ' \
                   'href="/gerenciar_cadastros">Gerenciar cadastros</a></p</body> '

        elif form_type == 'culturas':
            nome_cult = request.form['nome_cult']
            especie = request.form['especie']
            preco_saca = request.form['preco_saca']

            cur = minha_conexao.cursor()
            cur.execute("INSERT INTO culturas (nome_cult, especie, preco_saca) VALUES (%s, %s, %s)",
                        (nome_cult, especie, preco_saca))
            minha_conexao.commit()
            cur.close()
            return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Cadastro ' \
                   'efetuado com sucesso! <a href="/homepage">Novo cadastro</a> </br><a ' \
                   'href="/gerenciar_cadastros">Gerenciar cadastros</a></p</body> '

    return render_template('homepage.html', form_type=form_type)


@app.route('/gerenciar_cadastros/')
@login_required
def lista_cadastros():
    cursor = minha_conexao.cursor()
    cursor.execute("SELECT * FROM produtores")
    result_prod = cursor.fetchall()

    cursor.execute("SELECT * FROM motoristas")
    result_mot = cursor.fetchall()

    cursor.execute("SELECT * FROM culturas")
    result_cult = cursor.fetchall()
    cursor.close()

    return render_template('gerencia_cad.html', produtores=result_prod, motoristas=result_mot, culturas=result_cult)


@app.route('/excluir_produtor/<int:id>')
@login_required
def excluir_produtor(id):
    cursor = minha_conexao.cursor()

    # Verifica qual tabela deve ser excluída com base no ID fornecido
    cursor.execute("SELECT * FROM produtores WHERE id = %s", (id,))
    produtor = cursor.fetchone()
    if produtor is not None:
        cursor.execute("DELETE FROM produtores WHERE id = %s", (id,))
        minha_conexao.commit()
        cursor.close()
        print('Produtor excluído com sucesso.')
        return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Produtor excluído ' \
               'com sucesso! </br><a href="/homepage">Novo cadastro</a></br><a ' \
               'href="/gerenciar_cadastros">Mostrar cadastros</a></p </body> '


@app.route('/excluir_mot/<int:id>')
@login_required
def excluir_mot(id):
    cursor = minha_conexao.cursor()
    cursor.execute("SELECT * FROM motoristas WHERE id = %s", (id,))
    motorista = cursor.fetchone()
    if motorista is not None:
        cursor.execute("DELETE FROM motoristas WHERE id = %s", (id,))
        minha_conexao.commit()
        cursor.close()
        print('Motorista excluído com sucesso.')
        return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Motorista excluído ' \
               'com sucesso! </br><a href="/homepage">Novo cadastro</a></br><a ' \
               'href="/gerenciar_cadastros">Mostrar cadastros</a></p </body> '


@app.route('/excluir_cult/<int:id>')
@login_required
def excluir_cult(id):
    cursor = minha_conexao.cursor()
    cursor.execute("SELECT * FROM culturas WHERE id_cult = %s", (id,))
    cultura = cursor.fetchone()
    if cultura is not None:
        cursor.execute("DELETE FROM culturas WHERE id_cult = %s", (id,))
        minha_conexao.commit()
        cursor.close()
        print('Cultura excluída com sucesso.')
        return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Cultura excluída ' \
               'com sucesso! </br><a href="/homepage">Novo cadastro</a></br><a ' \
               'href="/gerenciar_cadastros">Mostrar cadastros</a></p </body> '

@app.route('/gerenciar_cadastros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produtor(id):
    cursor = minha_conexao.cursor()
    cursor.execute("SELECT * FROM produtores WHERE id=%s", (id,))
    result = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        nome_prod = request.form['nome_prod']
        endereco = request.form['endereco']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']

        cursor = minha_conexao.cursor()
        cursor.execute("UPDATE produtores SET nome_prod=%s, endereco=%s, cpf=%s, telefone=%s, email=%s WHERE id=%s",
                       (nome_prod, endereco, cpf, telefone, email, id))
        minha_conexao.commit()
        cursor.close()

        return redirect(url_for('gerenciar_cadastros'))

    return render_template('editar_prod.html', produtor=result)


@app.route('/entradas', methods=['GET', 'POST'])
@login_required
def select():
    cur = minha_conexao.cursor()
    cur.execute('SELECT id,nome_prod FROM produtores group by nome_prod')
    produtores_list = cur.fetchall()

    cur.execute('SELECT id,nome_motorista FROM motoristas group by nome_motorista')
    motorista_list = cur.fetchall()

    cur.execute('SELECT id_cult, nome_cult FROM culturas group by nome_cult')
    culturas_list = cur.fetchall()

    if request.method == 'POST':
        return cad_en()

    return render_template('cadastro_entrada.html', produtores_list=produtores_list, motorista_list=motorista_list,
                           culturas_list=culturas_list)


def cad_en():
    form_type = request.form['form_type'] if request.method == 'POST' else ''

    if request.method == 'POST':
        if form_type == 'entradas':
            data = datetime.strptime(request.form['data'], '%Y-%m-%d')
            quantidade = request.form['quantidade']
            produtor_id = request.form['produtor_id']
            motorista_id = request.form['motorista_id']
            cultura_id = request.form['cultura_id']

            cur = minha_conexao.cursor()
            cur.execute(
                "INSERT INTO entradas (data, quantidade, produtor_id, motorista_id, cultura_id) VALUES (%s, %s, %s, %s, %s)",
                (data, quantidade, produtor_id, motorista_id, cultura_id))
            minha_conexao.commit()
            cur.close()
            return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Cadastro efetuado com sucesso! <a href="/entradas">Novo cadastro</a> </br><a href="/lista_entrada">Mostrar entradas</a></p</body></html>'
        return render_template('homepage.html', form_type=form_type)


@app.route('/lista_entrada', methods=['GET', 'POST'])
@login_required
def listar_entradas():
    cursor = minha_conexao.cursor()
    cursor.execute(
        "SELECT entradas.id, entradas.data, entradas.quantidade, produtores.nome_prod AS nome_prod, motoristas.nome_motorista AS nome_motorista, culturas.nome_cult AS nome_cultura FROM entradas JOIN produtores ON entradas.produtor_id = produtores.id JOIN motoristas ON entradas.motorista_id = motoristas.id JOIN culturas ON entradas.cultura_id = culturas.id_cult")
    entradas = cursor.fetchall()
    cursor.close()

    return render_template('lista_entrada.html', entradas=entradas)


@app.route('/excluir_entrada/<int:id>')
@login_required
def excluir_entrada(id):
    # Conecta ao banco de dados
    cursor = minha_conexao.cursor()

    # Deleta a entrada com o ID especificado
    cursor.execute("DELETE FROM entradas WHERE id=%s", (id,))
    minha_conexao.commit()

    # Redireciona para a página que lista as entradas
    return '<html><head><link rel="stylesheet" href="/static/css/estilo.css"></head><body><p>Registro excluído com sucesso! <a href="/lista_entrada">Mostrar entradas</a></body></html></p'


@app.route('/cadastro_func', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        cursor = minha_conexao.cursor()
        cursor.execute("INSERT INTO funcionarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        minha_conexao.commit()
        cursor.close()

        return '<p>Cadastro efetuado com sucesso! <a href="/">Login</a></p'
    else:
        return render_template('cadastro_func.html')


@app.route('/logout')
def logout():
    # Remove a chave 'email' da sessão
    session.pop('email', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
