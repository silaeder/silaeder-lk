from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from . import db
from .user import User

class Guild(db.Model):
    __tablename__ = 'guilds'
    guild_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    guild_team = db.Column(db.String(100), nullable=False)  # We'll store this as a comma-separated string

    def __repr__(self):
        return f"<Guild {self.title}>"

class GuildUser(db.Model):
    __tablename__ = 'guild_users'
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer, db.ForeignKey('guilds.guild_id'), nullable=False)
    login = db.Column(db.String(100), db.ForeignKey('users.login'), nullable=False)

    def __repr__(self):
        return f"<GuildUser {self.guild_id+" "+self.login}>"

class GuildManager:
    @staticmethod
    def add_guild(title, guild_team):
        existing_users = User.query.filter(User.login.in_(guild_team)).all()
        if len(existing_users) != len(guild_team):
            existing_logins = {user.login for user in existing_users}
            missing_users = set(guild_team) - existing_logins
            return None, list(missing_users), None

        existing_guild = Guild.query.filter_by(title=title).first()
        if existing_guild:
            return None, None, "Guild with this name already exists"

        guild_team_str = ",".join(guild_team)
        new_guild = Guild(title=title, guild_team=guild_team_str)
        db.session.add(new_guild)
        
        try:
            db.session.flush()

            for login in guild_team:
                guild_user = GuildUser(guild_id=new_guild.guild_id, login=login)
                db.session.add(guild_user)

            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None, None, "Guild with this name already exists"

        return new_guild, None, None

    @staticmethod
    def get_guild(guild_id):
        guild = Guild.query.get(guild_id)
        if not guild:
            return None, "Guild not found"
        return guild, None

    @staticmethod
    def add_user_to_guild(guild_id, login):
        guild = Guild.query.get(guild_id)
        if not guild:
            return None, "Guild not found"
        
        user = User.query.filter_by(login=login).first()
        if not user:
            return None, "User not found"
        
        existing_guild_user = GuildUser.query.filter_by(guild_id=guild_id, login=login).first()
        if existing_guild_user:
            return None, "User is already in the guild"
        
        new_guild_user = GuildUser(guild_id=guild_id, login=login)
        db.session.add(new_guild_user)
        db.session.commit()
        guild.guild_team = ",".join([user.login for user in GuildUser.query.filter_by(guild_id=guild_id).all()])
        db.session.commit()
        return new_guild_user, None

    @staticmethod
    def remove_user_from_guild(guild_id, login):
        guild = Guild.query.get(guild_id)
        if not guild:
            return False, "Guild not found"

        guild_user = GuildUser.query.filter_by(guild_id=guild_id, login=login).first()
        if not guild_user:
            return False, "User not in guild"

        db.session.delete(guild_user)
        db.session.commit()
        
        guild_users = GuildUser.query.filter_by(guild_id=guild_id).all()
        guild.guild_team = ",".join([user.login for user in guild_users])
        db.session.commit()
        
        return True, None

    @staticmethod
    def update_guild(guild_id, title=None, guild_team=None):
        guild = Guild.query.get(guild_id)
        if not guild:
            return None, "Guild not found"

        try:
            if title is not None and title != guild.title:
                existing_guild = Guild.query.filter_by(title=title).first()
                if existing_guild and existing_guild.guild_id != guild_id:
                    return None, "Guild with this name already exists"
                guild.title = title

            if guild_team is not None:
                if not isinstance(guild_team, list):
                    return None, "guild_team must be a list of user logins"

                existing_users = User.query.filter(User.login.in_(guild_team)).all()
                if len(existing_users) != len(guild_team):
                    existing_logins = {user.login for user in existing_users}
                    missing_users = set(guild_team) - existing_logins
                    return None, f"Some users do not exist: {', '.join(missing_users)}"

                GuildUser.query.filter_by(guild_id=guild_id).delete()

                for login in guild_team:
                    new_guild_user = GuildUser(guild_id=guild_id, login=login)
                    db.session.add(new_guild_user)

                guild.guild_team = ",".join(guild_team)

            db.session.commit()
            return guild, None
        except Exception as e:
            db.session.rollback()
            return None, f"Error updating guild: {str(e)}"


 #это пока не работает(
    @staticmethod
    def delete_guild(guild_id):
        guild = Guild.query.get(guild_id)
        if not guild:
            return False, "Guild not found"
        try:
            db.session.delete(guild)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting guild: {str(e)}"