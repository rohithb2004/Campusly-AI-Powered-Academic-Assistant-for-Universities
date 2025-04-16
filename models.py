from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role=db.Column(db.String(20), nullable=False,default='user')

class Intent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80))
    response = db.Column(db.String(500), nullable=False)
    