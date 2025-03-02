from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    
    resource_usages = db.relationship('ResourceUsage', backref='user', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)

class ResourceUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    disk_percent = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(20), nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
