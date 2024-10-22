from flask_sqlalchemy import SQLAlchemy

from . import db

class Guild(db.Model):
    __tablename__ = 'guilds'
    guild_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    guild_team = db.Column(db.String(100), nullable=False) #список участников (логины)

    def __repr__(self):
        return f"<Guild {self.title}>"

class GuildManager:
    @staticmethod
    def add_guild(title, guild_team):
        new_guild = Guild(title=title, guild_team=guild_team)
        db.session.add(new_guild)
        db.session.commit()
        return new_guild