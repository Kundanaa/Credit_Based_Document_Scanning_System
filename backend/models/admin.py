from extensions import db, bcrypt
from flask_login import UserMixin



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @classmethod
    def create_admin(cls):
        if not cls.query.first():  # Ensure only one admin
            admin = cls(username="admin", password_hash=bcrypt.generate_password_hash("admin123").decode('utf-8'))
            db.session.add(admin)
            db.session.commit()

