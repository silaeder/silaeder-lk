from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    #Да, я знаю что здесь пароль, потом уберу
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://developer:eto_silaeder_parol_zzz@pgdb:5432/pgdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

from .user import User
from .guild import Guild
from .projects import Project
