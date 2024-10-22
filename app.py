from flask import Flask, Blueprint
from database import init_db, db
from routes.projects import projects_bp
from routes.user import user_bp
from routes.guild import guild_bp

app = Flask(__name__)

init_db(app)

app.register_blueprint(projects_bp, url_prefix="/projects")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(guild_bp, url_prefix="/guild")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)