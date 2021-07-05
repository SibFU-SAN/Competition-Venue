from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired(), Regexp("^[aA-zZ\\d_]+$"), Length(3, 24)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(5)])
    confirmation = PasswordField("Подтверждение пароля", validators=[DataRequired(), Length(5)])
    submit = SubmitField("Зарегистрироваться")
