from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import jwt
import os
import hashlib
from database import user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login():
    login = request.args.get("login")
    password = hashlib.md5(request.args.get("password").encode()).hexdigest()
    if user.User.check_credentials(login, password):
        token = jwt.encode({"login": login}, os.getenv("SECRET_KEY"), algorithm="HS256")
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False})
