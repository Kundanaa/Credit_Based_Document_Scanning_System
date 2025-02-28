
# models/user.py - User Model
from datetime import datetime
from extensions import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(60), nullable=False)
    credits = db.Column(db.Integer, default=20)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def reset_credits(self):
        """Reset credits to 20 if the last reset was not today."""
        if self.last_reset.date() < datetime.utcnow().date():
            self.credits = 20
            self.last_reset = datetime.utcnow()
            db.session.commit()