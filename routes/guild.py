from flask import Blueprint, request, jsonify
from database.guild import Guild, GuildManager
from routes.auth import auth_required, is_user_in_guild, is_admin
from database import db

GUILD_FIELDS = ["title", "guild_team"]
GUILD_REQUIRED_FIELDS = ["title", "guild_team"]

guild_bp = Blueprint("guild", __name__)

@guild_bp.route("/")
def index():
    return "Guild"
    
@guild_bp.route("/create", methods=["POST"])
@auth_required
@is_admin
def create_guild():
    for field in GUILD_REQUIRED_FIELDS:
        if field not in request.json:
            return jsonify({"message": f"Field {field} is required"}), 400
    
    title = request.json["title"]
    guild_team = request.json["guild_team"]
    
    if not isinstance(guild_team, list):
        return jsonify({"message": "guild_team must be a list of user logins"}), 400
    
    new_guild, missing_users, error_message = GuildManager.add_guild(title, guild_team)
    
    if missing_users:
        return jsonify({
            "message": "Some users do not exist",
            "missing_users": missing_users
        }), 400
    
    if error_message:
        return jsonify({"message": error_message}), 400
    
    return jsonify({
        "message": "Guild created",
        "guild_id": new_guild.guild_id,
        "title": new_guild.title,
        "members": new_guild.guild_team.split(',') if new_guild.guild_team else []
    }), 201


@guild_bp.route("/get_guild", methods=["GET"])
@auth_required
def get_guild():
    @is_user_in_guild(request.args.get("guild_id"))
    def get_guild_decorated():
        if not request.args.get("guild_id"):
            return jsonify({"message": "Guild ID is required"}), 400
        guild_id = request.args.get("guild_id")
        guild, error = GuildManager.get_guild(guild_id)
        if error:
            return jsonify({"message": error}), 404
        return jsonify({
            "guild_id": guild.guild_id,
        "title": guild.title,
            "guild_team": guild.guild_team
        })
    return get_guild_decorated()

@guild_bp.route("/add_user/<int:guild_id>", methods=["POST"])
@auth_required
def add_user_to_guild(guild_id):
    @is_user_in_guild(guild_id)
    def add_user_to_guild_decorated():
        if not request.json.get("login"):
            return jsonify({"message": "User login is required"}), 400
        
        login = request.json["login"]
        result, error = GuildManager.add_user_to_guild(guild_id, login)
        
        if error:
            return jsonify({"message": error}), 404 if "not found" in error else 400
        
        return jsonify({"message": "User added to guild"}), 200
    return add_user_to_guild_decorated()

@guild_bp.route("/update/<int:guild_id>", methods=["POST"])
@auth_required
def update_guild(guild_id):
    @is_user_in_guild(guild_id)
    def update_guild_decorated():
        title = request.json.get("title")
        guild_team = request.json.get("guild_team")

        if title is None and guild_team is None:
            return jsonify({"message": "No fields to update"}), 400

        updated_guild, error = GuildManager.update_guild(guild_id, title, guild_team)

        if error:
            return jsonify({"message": error}), 404 if "not found" in error else 400

        return jsonify({
            "message": "Guild updated successfully",
            "guild_id": updated_guild.guild_id,
            "title": updated_guild.title,
            "members": updated_guild.guild_team.split(',') if updated_guild.guild_team else []
        }), 200
    return update_guild_decorated()

@guild_bp.route("/remove_user/<int:guild_id>", methods=["POST"])
@auth_required
def remove_user_from_guild(guild_id):
    @is_user_in_guild(guild_id)
    def remove_user_from_guild_decorated():
        if not request.json.get("login"):
            return jsonify({"message": "User login is required"}), 400
        
        login = request.json["login"]
        result, error = GuildManager.remove_user_from_guild(guild_id, login)
        
        if error:
            return jsonify({"message": error}), 404 if "not found" in error else 400
        
        return jsonify({"message": "User removed from guild"}), 200
    return remove_user_from_guild_decorated()

@guild_bp.route("/get_guilds_names_by_user", methods=["GET"])
@auth_required
def get_guilds_by_user():
    guilds = GuildManager.get_guilds_by_user(request.args.get("login"))
    return jsonify({"guilds": [guild.title for guild in guilds]}), 200

@guild_bp.route("/delete/<int:guild_id>", methods=["DELETE"])
@auth_required
@is_admin
def delete_guild(guild_id):
    success, error = GuildManager.delete_guild(guild_id)
    if not success:
        return jsonify({"message": error}), 404 if error == "Guild not found" else 500
    return jsonify({"message": "Guild deleted successfully"}), 200
