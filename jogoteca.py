from flask import Flask, flash, redirect, render_template, request, session, url_for
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL

from models import Jogo, Usuario


app = Flask(__name__)
app.secret_key = 'segredo'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'jogoteca'
app.config['MYSQL_PORT'] = 3307

db = MySQL(app)
jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos = lista)

@app.route('/novo')
def novo():
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect(url_for('login', proxima=url_for('novo')))
  return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar',methods = ['POST',])
def criar():
  nome = request.form['nome']
  categoria = request.form['categoria']
  console = request.form['console']
  jogo = Jogo(nome, categoria, console)
  jogo_dao.salvar(jogo)

  arquivo = request.files['arquivo']
  arquivo.save(f'uploads/{arquivo.filename}')
  return redirect(url_for('index'))

@app.route('/login')
def login():
  proxima = request.args.get('proxima')
  return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
  usuario = usuario_dao.buscar_por_id(request.form['usuario'])
  if usuario:
    if request.form['senha'] == usuario.senha:
      session['usuario_logado'] = usuario.nickname
      flash(usuario.nickname + ' Logado com Sucesso!')
      proxima_pagina = request.form['proxima']
      if proxima_pagina == 'None':
        return redirect(url_for('index'))
      return redirect(proxima_pagina)
    else:
      flash('Usuário ou senha incorretos')
    return redirect(url_for('login'))
  else:
    flash('Usuário não logado!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
  session['usuario_logado'] = None
  flash('Logout efetuado com sucesso!')
  return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    return redirect(url_for('login', proxima=url_for('editar')))
  jogo = jogo_dao.busca_por_id(id)
  return render_template('editar.html', titulo='Editando Jogo', jogo = jogo)

@app.route('/atualizar/<int:id>',methods = ['POST',])
def atualizar(id):
  nome = request.form['nome']
  categoria = request.form['categoria']
  console = request.form['console']
  jogo = Jogo(nome, categoria, console, id=id)
  jogo_dao.salvar(jogo)
  return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
  jogo_dao.deletar(id)
  flash('O jogo foi removido com sucesso!')
  return redirect(url_for('index'))



app.run(port=3001, debug=True)
