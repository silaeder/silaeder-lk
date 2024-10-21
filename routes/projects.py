from flask import Blueprint, request, jsonify, render_template
from database.user import UserManager

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def index():
    return render_template("projects/index.html")


"""
Немного gpt кода для проверки работоспособности бд
"""


@projects_bp.route("/add_user", methods=["POST"])
def add_user():
    real_name = request.json.get('real_name')
    if not real_name:
        return jsonify({"error": "Real name is required"}), 400
    UserManager.add_user(real_name)
    return jsonify({"success": True, "message": "User added successfully"}), 201

@projects_bp.route("/get_user", methods=["GET"])
def get_user():
    email_or_login = request.args.get('email_or_login')
    user = UserManager.get_user_by_email(email_or_login)
    if user:
        return jsonify({"user": str(user)}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@projects_bp.route("/update_user", methods=["POST"])
def update_user():
    email_or_login = request.json.get('email_or_login')
    updates = request.json.get('updates', {})
    success = UserManager.update_user(email_or_login, **updates)
    if success:
        return jsonify({"success": True, "message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404

@projects_bp.route("/delete_user", methods=["DELETE"])
def delete_user():
    email_or_login = request.args.get('email_or_login')
    success = UserManager.delete_user(email_or_login)
    if success:
        return jsonify({"success": True, "message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404