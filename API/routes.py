from API import app


@app.route("/")
def teste():
    return {"nome": "matheus"}
