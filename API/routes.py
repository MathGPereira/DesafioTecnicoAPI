from API import app, render_template, url_for


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")
