from API import app, render_template, url_for


@app.route("/")
def home():
    return render_template("login.html")
