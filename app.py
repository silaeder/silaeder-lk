from flask import Flask, Blueprint
from database import init_db, db
from routes.projects import projects_bp
from routes.user import user_bp
from routes.guild import guild_bp
from routes.auth import auth_bp
from database.user import UserManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

init_db(app)

app.register_blueprint(projects_bp, url_prefix="/projects")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(guild_bp, url_prefix="/guild")
app.register_blueprint(auth_bp, url_prefix="/auth")

with app.app_context():
    db.create_all()
    UserManager.add_user("ADM I N", is_admin=True, password=os.getenv("ADMIN_PASSWORD"))

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)
