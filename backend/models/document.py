# models/document.py - Document Model
from extensions import db
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ❌ Requires user_id
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, filename, content):  # ✅ Accept user_id
        self.user_id = user_id
        self.filename = filename
        self.content = content
