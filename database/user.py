from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from transliterate import translit
import random
import string
from . import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    full_name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date)
    photo_path = db.Column(db.String(300))
    password = db.Column(db.String(100), nullable=False)
    contacts = db.Column(db.String(100))
    interests = db.Column(db.String(100))

    def __repr__(self):
        return f"<User {self.login}>"

#Набросок функций для бд
class UserManager:
    @staticmethod
    def add_user(real_name):
        """Добавляет нового пользователя в базу данных."""
        full_name = re.sub(r'[^a-zA-Z ]', '', translit(real_name, language_code='ru', reversed=True).lower())
        username = full_name.split()[0] + "." + full_name.split()[1][0] + full_name.split()[2][0]
        
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(8))

        new_user = User(login=username, full_name=real_name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    @staticmethod
    def get_user_by_email(email_or_login):
        """Возвращает пользователя по его email или логину."""
        return User.query.filter_by(email=email_or_login).first() or User.query.filter_by(login=email_or_login).first()

    @staticmethod
    def update_user(email_or_login, **kwargs):
        """Обновляет данные пользователя по его email или логину."""
        user = User.query.filter_by(email=email_or_login).first() or User.query.filter_by(login=email_or_login).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_user(email_or_login):
        """Удаляет пользователя по его email или логину."""
        user = User.query.filter_by(email=email_or_login).first() or User.query.filter_by(login=email_or_login).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False