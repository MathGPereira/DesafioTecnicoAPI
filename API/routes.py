from API import app, render_template, url_for
from API.forms import FormularioCadastro, FormularioLogin


@app.route("/", methods=["GET", "POST"])
def home():
    formulario_login = FormularioLogin()

    return render_template("login.html", formulario_login=formulario_login)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    formulario_cadastro = FormularioCadastro()

    return render_template("cadastro.html", formulario_cadastro=formulario_cadastro)
