from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Email, Length, DataRequired


class FormularioLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    botao_submit_login = SubmitField("Fazer login")


class FormularioCadastro(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("senha")])
    token = StringField("Token", validators=[DataRequired()])
    botao_submit_cadastro = SubmitField("Cadastrar")
