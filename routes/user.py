from flask import Blueprint, request, jsonify
from database.user import UserManager
from routes.auth import auth_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
    return "User"

@user_bp.route("/add_user", methods=["POST"])
@auth_required
def add_user():
    real_name = request.json.get('real_name')
    user_type = request.json.get('user_type')
    if not real_name:
        return jsonify({"error": "Real name is required"}), 400
    user, password = UserManager.add_user(real_name, user_type)
    return jsonify({"success": True, "username": str(user.login), "password": password}), 201

@user_bp.route("/get_user", methods=["GET"])
@auth_required
def get_user():
    email_or_login = request.args.get('email_or_login')
    user = UserManager.get_user_by_email(email_or_login)
    if user:
        return jsonify({
            "user": {
                "login": user.login,
                "email": user.email,
                "full_name": user.full_name
            }
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route("/update_user", methods=["POST"])
@auth_required
def update_user():
    email_or_login = request.json.get('email_or_login')
    updates = request.json.get('updates', {})
    success = UserManager.update_user(email_or_login, **updates)
    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404

@user_bp.route("/delete_user", methods=["DELETE"])
@auth_required
def delete_user():
    email_or_login = request.args.get('email_or_login')
    success = UserManager.delete_user(email_or_login)
    if success:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_bp.route("/add_class", methods=["POST"])
@auth_required
def add_users():
    users_data = request.json.get('users')
    if not users_data or not isinstance(users_data, list):
        return jsonify({"error": "Invalid users data. Expected a list of user information."}), 400
    
    added_users = []
    for user_info in users_data:
        real_name = user_info.get('real_name')
        user_type = user_info.get('user_type')
        if not real_name:
            return jsonify({"error": f"Real name is required for all users. Missing for: {user_info}"}), 400
        user, password = UserManager.add_user(real_name, user_type)
        added_users.append({
            "username": str(user.login),
            "password": password,
            "real_name": real_name
        })
        
    return jsonify({"success": True, "added_users": added_users}), 201
