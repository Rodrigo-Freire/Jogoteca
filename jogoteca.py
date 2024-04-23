from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo(nome="Tetris", categoria="Puzzle", console="Nintendinho")
jogo2 = Jogo(nome="Prince of Persia", categoria="Aventura", console="Playstation 1")
jogo3 = Jogo(nome="Drive", categoria="Corrida",console="Playstation 2")
lista_jogos = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self._nome = nome
        self._nickname = nickname
        self.senha = senha

usuario1 = Usuario(nome="Fernanda", nickname="FF", senha="321654")
usuario2 = Usuario(nome="Rodrigo", nickname="RF", senha="987654")
usuario3 = Usuario(nome="Morgana", nickname="MOMO", senha="123456")

usuarios = {usuario1._nickname : usuario1, usuario2._nickname : usuario2, usuario3._nickname : usuario3}

app = Flask(__name__)
app.secret_key = "flask_alura"

@app.route('/')
def index():
    return render_template("lista.html", titulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo='Novo Jogo')

@app.route('/criar', methods=["POST",])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)
    return redirect(url_for("index"))

@app.route('/login')
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route('/autenticar', methods=["POST",])
def autenticar():
    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]]
        if request.form["senha"] == usuario.senha:
            session['usuario_logado'] = usuario._nickname
            flash(f"Usuário {usuario._nickname} logado com sucesso!")
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    # if 'kaspersky' == request.form["senha"]:
    #     session['usuario_logado'] = request.form["usuario"]
    else:
        flash(f"Usuário não logado!")
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash(f"Logout efetuado com sucesso!")
    return redirect(url_for("index"))

# trecho da app
app.run(debug=True, host='0.0.0.0', port=8080)