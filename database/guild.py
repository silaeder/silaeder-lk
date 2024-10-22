from flask_sqlalchemy import SQLAlchemy

from . import db

class Guild(db.Model):
    __tablename__ = 'guilds'
    guild_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    guild_team = db.Column(db.String(100), nullable=False) #список участников (логины)

    def __repr__(self):
        return f"<Guild {self.title}>"

class GuildUser(db.Model):
    __tablename__ = 'guild_users'
    guild_id = db.Column(db.Integer, db.ForeignKey('guilds.guild_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return f"<GuildUser {self.guild_id} {self.user_id}>"

class GuildManager:
    @staticmethod
    def add_guild(title, guild_team):
        new_guild = Guild(title=title, guild_team=guild_team)
        db.session.add(new_guild)
        db.session.commit()
        return new_guild
    
    @staticmethod
    def delete_guild(guild_id):
        guild = Guild.query.get(guild_id)
        db.session.delete(guild)
        db.session.commit()
        return True

    @staticmethod
    def add_user_to_guild(guild_id, user_id):
        new_guild_user = GuildUser(guild_id=guild_id, user_id=user_id)
        db.session.add(new_guild_user)
        db.session.commit()
        return new_guild_user
    
    @staticmethod
    def remove_user_from_guild(guild_id, user_id):
        guild_user = GuildUser.query.filter_by(guild_id=guild_id, user_id=user_id).first()
        db.session.delete(guild_user)
        db.session.commit()
        return True
    
    @staticmethod
    def get_guild_users(guild_id):
        return [gu.user_id for gu in GuildUser.query.filter_by(guild_id=guild_id).all()]
    