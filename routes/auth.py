from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import jwt
import os
import hashlib
from database.user import UserManager
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from database.guild import GuildManager
from database.projects import ProjectManager

load_dotenv()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if not request.args.get("login") or not request.args.get("password"):
        return jsonify({"error": "Login and password are required"}), 400
    login = request.args.get("login")
    password = hashlib.md5(request.args.get("password").encode()).hexdigest()
    if UserManager.check_credentials(login, password):
        token = jwt.encode({"login": login, "exp": datetime.now(timezone.utc) + timedelta(days=7)}, os.getenv("JWT_SECRET"), algorithm="HS256")
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False})

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            exp_datetime = datetime.fromtimestamp(data["exp"], timezone.utc)
            if exp_datetime < datetime.now(timezone.utc):
                return jsonify({'message': 'Token is expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            exp_datetime = datetime.fromtimestamp(data["exp"], timezone.utc)
            if exp_datetime < datetime.now(timezone.utc):
                return jsonify({'message': 'Token is expired!'}), 401
            user = UserManager.get_user_by_email(data["login"])
            if not user.is_admin:
                return jsonify({'message': 'User is not admin!'}), 403
            else:
                return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
    return decorated

def is_user_in_guild(guild_id):
    def decorated(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
                exp_datetime = datetime.fromtimestamp(data["exp"], timezone.utc)
                if exp_datetime < datetime.now(timezone.utc):
                    return jsonify({'message': 'Token is expired!'}), 401
            except Exception as e:
                return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            guild_users = GuildManager.get_guild(guild_id)[0].guild_team.split(',')
            if data["login"] not in guild_users:
                return jsonify({'message': 'User is not in guild!'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorated

def is_user_in_project(project_id):
    def decorated(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
                exp_datetime = datetime.fromtimestamp(data["exp"], timezone.utc)
                if exp_datetime < datetime.now(timezone.utc):
                    return jsonify({'message': 'Token is expired!'}), 401
            except Exception as e:
                return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            project_users = ProjectManager.get_users_by_project_id(project_id)
            if data["login"] not in project_users:
                return jsonify({'message': 'User is not in project!'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorated

@auth_bp.route("/get_username", methods=["GET"])
@auth_required
def get_username():
    token = request.headers.get('Authorization')
    try:
        data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_email = data["login"]
        user = UserManager.get_user_by_email(user_email)
        if user:
            return jsonify({"username": user.login})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e: 
        return jsonify({'error': 'Invalid token', 'message': str(e)}), 401
