from flask import Blueprint, request, jsonify
from database.guild import Guild

guild_bp = Blueprint("guild", __name__)

@guild_bp.route("/")
def index():
    return "Guild"