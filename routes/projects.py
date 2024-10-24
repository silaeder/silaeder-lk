from flask import Blueprint, request, jsonify, render_template
from database.projects import Project
from routes.auth import auth_required, is_user_in_project, is_user_in_guild, is_admin
from database.projects import ProjectManager
from database import db

PROJECT_FIELDS = ["title", "description", "teacher", "team", "status", "video_link", "presentation_path", "short_description"]
PROJECT_REQUIRED_FIELDS = ["title", "description", "teacher", "team", "status", "short_description"]

projects_bp = Blueprint("projects", __name__)

@projects_bp.route("/")
def index():
    return "Projects"

@projects_bp.route("/get_project_members", methods=["GET"])
@auth_required
def get_project_members():
    if not request.args.get("project_id"):
        return jsonify({"message": "Project ID is required"}), 400
    project_id = request.args.get("project_id")
    projects = ProjectManager.get_users_by_project_id(project_id)
    return jsonify({"projects": [project.to_dict() for project in projects]})

@projects_bp.route("/get_project", methods=["GET"])
@auth_required
def get_project():
    if not request.args.get("project_id"):
        return jsonify({"message": "Project ID is required"}), 400
    project_id = request.args.get("project_id")
    project = ProjectManager.get_project_by_id(project_id)
    return jsonify(project.to_dict())

@projects_bp.route("/get_projects_by_user", methods=["GET"])
@auth_required
def get_projects_by_user():
    if not request.args.get("login"):
        return jsonify({"message": "Login is required"}), 400
    login = request.args.get("login")
    projects = ProjectManager.get_projects_by_user_login(login)
    return jsonify([project.to_dict() for project in projects])

@projects_bp.route("/create", methods=["POST"])
@auth_required
def create_project():
    for i in PROJECT_REQUIRED_FIELDS:
        if i not in request.json:
            return jsonify({"message": f"Field {i} is required"}), 400
    project = Project()
    for i in PROJECT_FIELDS:
        if i in request.json:
            setattr(project, i, request.json[i])
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created"}), 201

@projects_bp.route("/add_user/<int:project_id>", methods=["POST"])
@auth_required
def add_user_to_project(project_id):
    @is_user_in_project(project_id)
    def add_user_to_project_decorated():
        login = request.json.get("login")
        st = ProjectManager.add_user_to_project(project_id, login)
        if st == -1:
            return jsonify({"message": f"Project {project_id}` not found"}), 404
        elif st == -2:
            return jsonify({"message": f"User {login} not found"}), 404
        return jsonify({"message": "User added to project"}), 200
    return add_user_to_project_decorated()

@projects_bp.route("/remove_user/<int:project_id>", methods=["POST"])
@auth_required
def remove_user_from_project(project_id):
    @is_user_in_project(project_id)
    def remove_user_from_project_decorated():
        login = request.json.get("login")
        st = ProjectManager.remove_user_from_project(project_id, login)
        if st == -1:
            return jsonify({"message": f"Project {project_id}` not found"}), 404
        elif st == -2:
            return jsonify({"message": f"User {login} not found"}), 404
        return jsonify({"message": "User removed from project"}), 200
    return remove_user_from_project_decorated()

@projects_bp.route("/get_all_projects", methods=["GET"])
def get_all_projects():
    projects = ProjectManager.get_all_projects()
    d = {}
    for i in projects:
        d[i.project_id] = {
            "title": i.title,
            "description": i.description,
            "teacher": i.teacher,
            "team": ProjectManager.get_users_by_project_id(i.project_id),
            "status": i.status,
            "short_description": i.short_description,
            "video_link": i.video_link,
            "presentation_path": i.presentation_path
        }
    return d

@projects_bp.route("/update/<int:project_id>", methods=["POST"])
@auth_required
def update_project_by_id(project_id):
    @is_user_in_project(project_id)
    def update_project_by_id_decorated():
        args = {}
        for i in PROJECT_FIELDS:
            if i in request.json:
                if i == "team":
                    for login in request.json[i]:
                        st = ProjectManager.add_user_to_project(project_id, login)
                        if st == -2:
                            return jsonify({"message": f"User {login} not found"}), 404
                else:
                    args[i] = request.json[i]
        ProjectManager.update_project(project_id, **args)
        return jsonify({"message": "Project updated"}), 200
    return update_project_by_id_decorated()

@projects_bp.route("/delete/<int:project_id>", methods=["POST"])
@auth_required
def delete_project(project_id):
    @is_user_in_project(project_id)
    def delete_project_decorated():
        if ProjectManager.delete_project(project_id):
            return jsonify({"message": "Project deleted"}), 200
        else:
            return jsonify({"message": "Project not found"}), 404
    return delete_project_decorated()