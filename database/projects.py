from flask_sqlalchemy import SQLAlchemy

from . import db

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    video_link = db.Column(db.String(200))
    presentation_path = db.Column(db.String(300))
    teacher = db.Column(db.String(100), nullable=False) #научный руководитель (его login)
    team = db.Column(db.String(100), nullable=False) #список участников (логины)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def get_project_by_id(project_id):
        return Project.query.filter_by(project_id=project_id).first()
    
    def get_projects_by_user_id(user_id):
        return Project.query.filter_by(user_id=user_id).all()