from flask import Blueprint, request, jsonify
from database.user import UserManager

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
    return "User"

@user_bp.route("/add_user", methods=["POST"])
def add_user():
    real_name = request.json.get('real_name')
    if not real_name:
        return jsonify({"error": "Real name is required"}), 400
    user = UserManager.add_user(real_name)
    return jsonify({"success": True, "username": str(user.login)}), 201

@user_bp.route("/get_user", methods=["GET"])
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
def update_user():
    email_or_login = request.json.get('email_or_login')
    updates = request.json.get('updates', {})
    success = UserManager.update_user(email_or_login, **updates)
    if success:
        return jsonify({"success": True, "message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404

@user_bp.route("/delete_user", methods=["DELETE"])
def delete_user():
    email_or_login = request.args.get('email_or_login')
    success = UserManager.delete_user(email_or_login)
    if success:
        return jsonify({"success": True, "message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404