from API import app, render_template, url_for, flash, redirect
from API.forms import FormularioCadastro, FormularioLogin


@app.route("/", methods=["GET", "POST"])
def home():
    formulario_login = FormularioLogin()

    if formulario_login.validate_on_submit():
        flash(f"Login feito com sucesso no e-mail {formulario_login.email.data}.", "alert-success")
        return redirect(url_for("usuario"))

    return render_template("login.html", formulario_login=formulario_login)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    formulario_cadastro = FormularioCadastro()

    if formulario_cadastro.validate_on_submit():
        flash("Cadastro realizado com sucesso! Realize o Login!", "alert-success")
        return redirect(url_for("home"))

    return render_template("cadastro.html", formulario_cadastro=formulario_cadastro)


@app.route("/usuario")
def usuario():
    return render_template("usuario.html")
