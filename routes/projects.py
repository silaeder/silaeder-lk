from flask import Blueprint, request, jsonify, render_template
from database.projects import Project
from routes.auth import auth_required

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/get_user", methods=["GET"])
@auth_required
def get_user_projects():
    user_id = request.args.get("user_id")
    projects = Project.get_projects_by_user_id(user_id)
    return jsonify({"projects": [project.to_dict() for project in projects]})