import hashlib
import pymysql
from flask_login import UserMixin

from app.database import db


class User(UserMixin):
    def __init__(self, data):
        self.id = data[0]
        self.login = data[1]
        self.hashed_password = data[2]
        self.wins = data[3]
        self.played = data[4]
        self.about = data[5]
        self.cached_game = None

    def get_id(self):
        return self.id

    def change_password(self, new_password: str) -> str:
        self.hashed_password = hash_password(new_password)
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE users SET password = %s WHERE id = {self.id} LIMIT 1;
            """, new_password)
            conn.commit()
            return self.token

    def __str__(self):
        return f"<User #{self.id}(@{self.login})>"

    @property
    def token(self) -> str:
        return generate_token(self.login, self.hashed_password)

    def end_game(self, winner: bool):
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute(f"""
                UPDATE users SET played = played + 1, wins = wins + {int(winner)} WHERE id = {self.id} LIMIT 1;
            """)
            conn.commit()


class UserError(Exception):
    def __init__(self, message: str):
        self.message = message


def get_by_id(user_id: int) -> User or None:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT * FROM users WHERE id = {user_id} LIMIT 1;
        """)
        data = cursor.fetchone()
        return None if data is None else User(data)


def get_by_login(login: str) -> User or None:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM users WHERE login = %s LIMIT 1;
        """, [login])
        data = cursor.fetchone()
        return None if data is None else User(data)


def get_by_token(token: str) -> User or None:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM users WHERE MD5(CONCAT(LOWER(login), password)) = %s LIMIT 1;
        """, [token])
        data = cursor.fetchone()
        return None if data is None else User(data)


def register(login: str, password: str) -> User:
    try:
        with db.connect() as conn, conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (login, password) VALUES (%s, MD5(%s));
            """, (login, password))
            conn.commit()
            return get_by_login(login)
    except pymysql.IntegrityError:
        raise UserError("Пользователь с данным логином уже существует")


def auth(login: str, password: str) -> User or None:
    token = generate_token(login, hash_password(password))
    return get_by_token(token)


def get_top10() -> list:
    with db.connect() as conn, conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM users ORDER BY wins DESC LIMIT 10;
        """)
        return [User(data) for data in cursor.fetchall()]


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def generate_token(login: str, password: str) -> str:
    return hashlib.md5("{}{}".format(login.lower(), password).encode()).hexdigest()
