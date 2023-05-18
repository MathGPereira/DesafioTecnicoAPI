from API import app, render_template, url_for, flash, redirect, database, bcrypt
from API.forms import FormularioCadastro, FormularioLogin
from API.models import Usuario
from flask_login import login_user, current_user


@app.route("/", methods=["GET", "POST"])
def home():
    formulario_login = FormularioLogin()

    if formulario_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formulario_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formulario_login.senha.data):
            login_user(usuario)
            flash(f"Login feito com sucesso no e-mail {formulario_login.email.data}.", "alert-success")

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
        database.session.add(usuario)
        database.session.commit()

        flash("Cadastro realizado com sucesso! Realize o Login!", "alert-success")

        return redirect(url_for("home"))

    return render_template("cadastro.html", formulario_cadastro=formulario_cadastro)


@app.route("/sair")
def sair():
    login_user()
    flash("Logout realizado com sucesso!", "alert-success")

    return redirect(url_for("home"))


@app.route("/tratativas")
def tratativas():
    pass
