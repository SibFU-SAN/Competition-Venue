from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
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


class SettingsForm(FlaskForm):
    about = TextAreaField("О себе", [Length(max=256)])
    submit = SubmitField("Сохранить")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Пароль", validators=[DataRequired()])
    new_password = PasswordField("Новый пароль", validators=[DataRequired(), Length(5)])
    confirmation = PasswordField("Подтверждение пароля", validators=[DataRequired(), Length(5)])
    submit = SubmitField("Изменить")


class FindDemoForm(FlaskForm):
    demo = StringField("ID игры", validators=[DataRequired(), Regexp("^[\\d]+$")])
    submit = SubmitField("Найти")
