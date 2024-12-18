from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from transliterate import translit
import random
import string
from . import db
import hashlib

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    #user_type = db.Column(db.String(100), nullable=False) #возможные значения: user, student, teacher, admin, root
    email = db.Column(db.String(120), unique=True)
    full_name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date)
    photo_path = db.Column(db.String(300))
    password = db.Column(db.String(100), nullable=False)
    contacts = db.Column(db.String(100))
    interests = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    #projects = db.relationship('Project', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.login}>"

class UserManager:
    @staticmethod
    def add_user(real_name, is_admin=False, password=None):
        """Добавляет нового пользователя в базу данных."""
        full_name = re.sub(r'[^a-zA-Z ]', '', translit(real_name, language_code='ru', reversed=True).lower())
        base_username = full_name.split()[0] + "." + full_name.split()[1][0] + full_name.split()[2][0]
        
        username = base_username
        counter = 1
        while User.query.filter_by(login=username).first():
            username = f"{base_username}{counter}"
            counter += 1
        
        characters = string.ascii_letters + string.digits
        if not password:
            password = ''.join(random.choice(characters) for i in range(8))

        password_hash = hashlib.md5(password.encode()).hexdigest()
        new_user = User(login=username, full_name=real_name, password=password_hash, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return new_user, password
        
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
    
    @staticmethod
    def check_credentials(email_or_login, password_hash):
        """Проверяет учетные данные пользователя."""
        user = UserManager.get_user_by_email(email_or_login)
        if user and user.password == password_hash:
            return True
        return False
    
    @staticmethod
    def get_all_users():
        return User.query.all()