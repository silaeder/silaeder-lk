from flask import Blueprint, request, render_template, redirect, url_for
import jwt
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = request.form
        for i in form.keys():
            if form[i] == "":
                return "Empty field: " + i
        if 1==1:
            response = redirect(url_for("portfolio.index"))
            response.set_cookie("token", jwt.encode({"user": form["username"]}, os.getenv("JWT_SECRET"), algorithm="HS256"))
            return response

@auth_bp.route("/logout")
def logout():
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = request.form
        for i in form.keys():
            if form[i] == "":
                return "Empty field: " + i
        if 1==1:
            response = redirect(url_for("portfolio.index"))
            response.set_cookie("token", jwt.encode({"user": form["username"]}, os.getenv("JWT_SECRET"), algorithm="HS256"))
            return response

@auth_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        if request.cookies.get("token"):
            try:
                if jwt.decode(request.cookies.get("token"), os.getenv("JWT_SECRET"), algorithms=["HS256"]):
                    return render_template("change-password.html")
                else:
                    return redirect(url_for("auth.login"))
            except:
                return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("auth.login"))
    else:
        form = request.form
        for i in form.keys():
            if form[i] == "":
                return "Empty field: " + i
        if 1==1:    
            return redirect(url_for("portfolio.index"))
