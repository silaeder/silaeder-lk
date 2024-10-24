from flask import Flask, Blueprint
from flask_cors import CORS

from routes.projects import projects_bp
from routes.user import user_bp
from routes.guild import guild_bp
from routes.auth import auth_bp

from database import init_db, db
from database.user import UserManager

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": [
        "http://server.mrvasil.ru:*",
        "https://server.mrvasil.ru:*",
        "http://silaeder.mrvasil.ru",
        "https://silaeder.mrvasil.ru"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type", "X-Total-Count"],
    "supports_credentials": True
}})

init_db(app)

app.register_blueprint(projects_bp, url_prefix="/projects")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(guild_bp, url_prefix="/guild")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def index():
    return """<html><head><style>body{font-family:Arial,sans-serif;line-height:1.6;margin:20px}h1{color:#333;border-bottom:2px solid #333;padding-bottom:10px}a{color:#0066cc;text-decoration:none}a:hover{text-decoration:underline}</style></head><body><h1>Hello! It's Silaeder API server!</h1><p>Silaeder frontend: <a href="https://silaeder.mrvasil.ru/">https://silaeder.mrvasil.ru/</a></p><p>Documentation: <a href="https://api.silaeder.mrvasil.ru/docs">https://api.silaeder.mrvasil.ru/docs</a></p></body></html>"""

with app.app_context():
    db.create_all()
    user = UserManager.add_user("ADM I N", is_admin=True, password=os.getenv("ADMIN_PASSWORD"))
    print("Admin: ", user)

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)
