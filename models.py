import imp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

class notes(db.Model):
    notes_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable = False)
    heading = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, nullable = False)
    user = db.relationship(users, backref=backref("notes", cascade="all, delete, delete-orphan"))