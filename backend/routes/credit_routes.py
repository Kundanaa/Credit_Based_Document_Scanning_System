# routes/credit_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_cors import CORS
from models.credit import CreditRequest
from flask_login import current_user, login_required

credit_bp = Blueprint('credits', __name__)
CORS(credit_bp, supports_credentials=True)

# Request Additional Credits
@credit_bp.route('/request', methods=['POST'])
@login_required
def request_credits():
    data = request.json
    credits_requested = data.get("credits", 10)  # Default to 10 if not provided
    
    if credits_requested <= 0:
        return jsonify({"error": "Invalid credit amount"}), 400

    credit_request = CreditRequest(user_id=current_user.id, credits_requested=credits_requested)
    db.session.add(credit_request)
    db.session.commit()

    return jsonify({"message": "Credit request submitted"}), 200
