from flask import request
from API import app, render_template, url_for, flash, redirect, database, bcrypt
from API.forms import FormularioCadastro, FormularioLogin, FormularioFiltrar
from API.models import Usuario, Cliente
from flask_login import logout_user, current_user, login_required, login_user


@app.route("/", methods=["GET", "POST"])
def home():
    formulario_login = FormularioLogin()

    if formulario_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formulario_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formulario_login.senha.data):
            login_user(usuario)
            flash(f"Login feito com sucesso no e-mail {formulario_login.email.data}.", "alert-success")

            parametro_next = request.args.get("next")

            if parametro_next:
                return redirect(url_for(parametro_next.replace("/", "")))
            else:
                return redirect(url_for("usuario"))
        else:
            flash("Email ou senha incorretos!", "alert-danger")

            return redirect(url_for("home"))

    return render_template("login.html", formulario_login=formulario_login)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    formulario_cadastro = FormularioCadastro()

    if formulario_cadastro.validate_on_submit():
        usuario = Usuario(
            username=formulario_cadastro.username.data,
            email=formulario_cadastro.email.data,
            senha=bcrypt.generate_password_hash(formulario_cadastro.senha.data),
            token=formulario_cadastro.token.data
        )

        with app.app_context():
            database.session.add(usuario)
            database.session.commit()

        flash("Cadastro realizado com sucesso! Realize o Login!", "alert-success")

        return redirect(url_for("home"))

    return render_template("cadastro.html", formulario_cadastro=formulario_cadastro)


@app.route("/usuario")
@login_required
def usuario():
    db = Cliente.query.all()

    return render_template("usuario.html", current_user=current_user, db=db)


@app.route("/tratativas", methods=["GET", "POST"])
@login_required
def tratativas():
    formulario_filtrar = FormularioFiltrar()
    clientes = []

    for pessoa in Cliente.query.filter_by(nome=formulario_filtrar.nome.data).all():
        clientes.append({
            "nome": pessoa.nome,
            "email": pessoa.email,
            "status": pessoa.status,
            "valor": pessoa.valor,
            "forma_pagamento": pessoa.forma_pagamento,
            "parcelas": pessoa.parcelas
        })

    return render_template("tratativas.html", formulario_filtrar=formulario_filtrar, clientes=clientes)


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout realizado com sucesso!", "alert-success")

    return redirect(url_for("home"))


@app.route("/hooks", methods=["GET", "POST"])
def hooks():
    bd = []
    web_hook = request.values.to_dict()

    if web_hook:
        if web_hook["status"] == "aprovado":
            resposta = f"Liberar acesso ao e-mail {web_hook['email']}"
        elif web_hook["status"] == "reembolsado":
            resposta = f"Retirar acesso dos cursos do e-mail {web_hook['email']}"
        else:
            resposta = f"Enviar mensagem de pagamento recusado"

        cliente = Cliente(
            nome=web_hook["nome"],
            email=web_hook["email"],
            status=web_hook["status"],
            valor=web_hook["valor"],
            forma_pagamento=web_hook["forma_pagamento"],
            parcelas=web_hook["parcelas"],
            resposta=resposta
        )

        with app.app_context():
            database.session.add(cliente)
            database.session.commit()

    for pessoa in Cliente.query.all():
        bd.append({
            "nome": pessoa.nome,
            "email": pessoa.email,
            "status": pessoa.status,
            "valor": pessoa.valor,
            "forma_pagamento": pessoa.forma_pagamento,
            "parcelas": pessoa.parcelas,
            "resposta": pessoa.resposta
        })

    return bd
