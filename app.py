from flask import Flask, Blueprint
from routes.projects import projects_bp

app = Flask(__name__)

app.register_blueprint(projects_bp, url_prefix="/projects")

if __name__ == "__main__":
    app.run("0.0.0.0", 3750)

