
from Leave import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    detail = db.Column(db.String(500), nullable=True)
    date_request = db.Column(db.String(100), nullable=True)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    remark = db.Column(db.String(500), nullable=True)

    def __repr__ (self):
        return '<Leave %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username
    def verify_password(self, pwd):
        return (self.password, pwd)