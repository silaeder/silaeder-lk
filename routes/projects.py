from flask import Blueprint, request, jsonify, render_template
from database.projects import Project

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def index():
    return render_template("projects/index.html")