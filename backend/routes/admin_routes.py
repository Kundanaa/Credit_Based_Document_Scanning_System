from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from flask_login import login_user
from flask_cors import CORS
from models.user import  User
from models.admin import Admin
from models.credit import CreditRequest

admin_bp = Blueprint('admin', __name__)
CORS(admin_bp, supports_credentials=True)

# Admin Login Route
@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(username=data['username']).first()
    if admin and bcrypt.check_password_hash(admin.password_hash, data['password']):
        return jsonify({"message": "Admin logged in successfully"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Approve/Deny Credit Requests
@admin_bp.route('/credits/approve', methods=['POST'])
def approve_credits():
    data = request.json
    request_id = data.get('request_id')
    action = data.get('action')  # 'approve' or 'reject'

    credit_request = CreditRequest.query.get(request_id)
    if not credit_request or credit_request.status != 'pending':
        return jsonify({"error": "Invalid or already processed request"}), 400

    if action == 'approve':
        user = User.query.get(credit_request.user_id)
        user.credits += credit_request.credits_requested
        credit_request.status = 'approved'
    else:
        credit_request.status = 'rejected'

    db.session.commit()
    return jsonify({"message": f"Request {action}d successfully"}), 200

# Admin Dashboard - Analytics
@admin_bp.route('/analytics', methods=['GET'])
def admin_analytics():
    user_scans = db.session.query(User.username, User.credits).all()
    pending_requests = CreditRequest.query.filter_by(status="pending").count()
    
    return jsonify({
        "total_users": len(user_scans),
        "user_credits": [{"username": u[0], "credits": u[1]} for u in user_scans],
        "pending_credit_requests": pending_requests
    })
