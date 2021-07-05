from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length
from app.user.constants import LOGIN_REGEX


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired(), Regexp(LOGIN_REGEX), Length(3, 24)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(5)])
    confirmation = PasswordField("Подтверждение пароля", validators=[DataRequired(), Length(5)])
    submit = SubmitField("Зарегистрироваться")
