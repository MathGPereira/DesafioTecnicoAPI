from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import EqualTo, Email, Length, DataRequired, ValidationError
from API.models import Usuario
from API.token import chave_token


class FormularioFiltrar(FlaskForm):
    nome = StringField("Nome")
    email = StringField("E-mail")
    status = StringField("Status")
    valor = FloatField("Valor pago")
    forma_pagamento = StringField("Forma de pagamento")
    parcelas = IntegerField("Parcelas")


class FormularioLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    botao_submit_login = SubmitField("Fazer login")


class FormularioCadastro(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 20)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("senha")])
    token = StringField("Token", validators=[DataRequired()])
    botao_submit_cadastro = SubmitField("Cadastrar")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError("E-mail já cadastrado! Cadastre-se com outro e-mail ou realize o login!")

    def validate_token(self, token):
        if token.data != chave_token:
            raise ValidationError("Token de cadastro inválido!")
