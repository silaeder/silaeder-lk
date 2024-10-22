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
        return {"project_id": self.project_id, "title": self.title}