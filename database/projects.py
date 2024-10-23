from flask_sqlalchemy import SQLAlchemy

from . import db
from .user import UserManager
class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    video_link = db.Column(db.String(200))
    presentation_path = db.Column(db.String(100))
    teacher = db.Column(db.String(100), nullable=False) #научный руководитель (его login)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Project {self.title}>"
    
class ProjectUser(db.Model):
    __tablename__ = 'project_users'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    login = db.Column(db.String(100), db.ForeignKey('users.login'), nullable=False)

    def __repr__(self):
        return f"<ProjectUser {self.project_id+" "+self.login}>"

class ProjectManager:
    @staticmethod
    def create_project(project):
        db.session.add(project)
        db.session.commit()
        return project
    
    @staticmethod
    def get_project_by_id(project_id):
        return Project.query.filter_by(project_id=project_id).first()
    
    @staticmethod
    def get_projects_by_user_id(login):
        projects = ProjectUser.query.filter_by(login=login).all()
        return [ProjectManager.get_project_by_id(project.project_id) for project in projects] if projects else []
    
    @staticmethod
    def add_user_to_project(project_id, login):
        if not ProjectManager.get_project_by_id(project_id):
            return -1
        if not UserManager.get_user_by_login(login):
            return -2
        project_user = ProjectUser(project_id=project_id, login=login)
        db.session.add(project_user)
        db.session.commit()
        return project_user
    
    @staticmethod
    def remove_user_from_project(project_id, login):
        if not ProjectManager.get_project_by_id(project_id):
            return -1
        if not UserManager.get_user_by_login(login):
            return -2
        project_user = ProjectUser.query.filter_by(project_id=project_id, login=login).first()
        if project_user:
            db.session.delete(project_user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_users_by_project_id(project_id):
        if not ProjectManager.get_project_by_id(project_id):
            return -1
        users = ProjectUser.query.filter_by(project_id=project_id).all()
        return [UserManager.get_user_by_email(user.login) for user in users] if users else []
    
    @staticmethod
    def delete_project(project_id):
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f"<ProjectManager {self.project_id} {self.user_id}>"