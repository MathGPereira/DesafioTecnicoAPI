from API import database, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id):
    return Usuario.query.get(int(id))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    token =  database.Column(database.String, nullable=False)
