from flask import Blueprint

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/")
def index():
    return "Portfolio"
