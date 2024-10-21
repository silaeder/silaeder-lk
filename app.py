from flask import Flask, Blueprint
from database import init_db, db
from routes.projects import projects_bp

app = Flask(__name__)

init_db(app)

app.register_blueprint(projects_bp, url_prefix="/projects")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)