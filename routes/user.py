from flask import Blueprint, request, jsonify
from database.user import UserManager
from routes.auth import auth_required, is_admin
from dotenv import load_dotenv

load_dotenv()

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
    return "User"

@user_bp.route("/add_user", methods=["POST"])
@auth_required
@is_admin
def add_user():
    real_name = request.json.get('real_name')
    if not real_name:
        return jsonify({"error": "Real name is required"}), 400
    user, password = UserManager.add_user(real_name)
    return jsonify({"success": True, "username": str(user.login), "password": password}), 201

@user_bp.route("/get_user", methods=["GET"])
@auth_required
def get_user():
    if not request.args.get('email_or_login'):
        return jsonify({"error": "Email or login is required"}), 400
    email_or_login = request.args.get('email_or_login')
    user = UserManager.get_user_by_email(email_or_login)
    if user:
        return jsonify({
            "user": {
                "user_id": user.user_id,
                "login": user.login,
                "email": user.email,
                "full_name": user.full_name,
                "birth_date": user.birth_date,
                "photo_path": user.photo_path,
                "contacts": user.contacts,
                "interests": user.interests,
                "is_admin": user.is_admin
            }
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route("/update_user", methods=["POST"])
@auth_required
def update_user():
    if not request.json.get('email_or_login') or not request.json.get('updates'):
        return jsonify({"error": "Email or login and updates are required"}), 400
    email_or_login = request.json.get('email_or_login')
    updates = request.json.get('updates', {})
    success = UserManager.update_user(email_or_login, **updates)
    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404

@user_bp.route("/delete_user", methods=["DELETE"])
@auth_required
@is_admin
def delete_user():
    if not request.args.get('email_or_login'):
        return jsonify({"error": "Email or login is required"}), 400
    email_or_login = request.args.get('email_or_login')
    success = UserManager.delete_user(email_or_login)
    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_bp.route("/add_class", methods=["POST"])
@auth_required
@is_admin
def add_users():
    if not request.json.get('users'):
        return jsonify({"error": "Users data is required"}), 400
    users_data = request.json.get('users')
    if not isinstance(users_data, list):
        return jsonify({"error": "Invalid users data. Expected a list of user information."}), 400
    
    added_users = []
    for user_info in users_data:
        real_name = user_info.get('real_name')
        if not real_name:
            return jsonify({"error": f"Real name is required for all users. Missing for: {user_info}"}), 400
        user, password = UserManager.add_user(real_name)
        added_users.append({
            "username": str(user.login),
            "password": password
        })
        
    return jsonify({"success": True, "added_users": added_users}), 201

@user_bp.route("/get_all_users", methods=["GET"])
@auth_required
@is_admin
def get_all_users():
    users = UserManager.get_all_users()
    d = {}
    for i in users:
        d[i.user_id] = {
            "user_id": i.user_id,
            "login": i.login,
            "email": i.email,
            "full_name": i.full_name,
            "birth_date": i.birth_date,
            "photo_path": i.photo_path,
            "contacts": i.contacts,
            "interests": i.interests,
            "is_admin": i.is_admin
        }
    return jsonify(d), 200