from flask import Blueprint, jsonify, request
from extensions import db
from models.user import User
from flask_cors import CORS  # ✅ Import CORS
import jwt
from config import Config

user_bp = Blueprint('user', __name__)
CORS(user_bp, supports_credentials=True)  # ✅ Enable CORS for this route

def get_user_from_token():
    """ Function to extract user from the token in request headers """
    token = request.headers.get("Authorization")

    if not token:
        print("🚨 No Authorization header found!")  # ✅ Debug log
        return None

    try:
        token = token.split(" ")[1]  # ✅ Ensure 'Bearer' is removed correctly
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        print("✅ Decoded Token:", decoded)  # ✅ Debug log

        user = User.query.get(decoded["user_id"])
        if not user:
            print("🚨 User not found for ID:", decoded["user_id"])
        return user
    except jwt.ExpiredSignatureError:
        print("🚨 Token expired!")
        return None
    except jwt.InvalidTokenError:
        print("🚨 Invalid token!")
        return None
    except Exception as e:
        print("🚨 Error decoding token:", str(e))
        return None
    
@user_bp.route('/profile', methods=['GET'])
def get_profile():
    print("🔍 Received Request Headers:", request.headers)  # ✅ Log request headers
    user = get_user_from_token()

    if not user:
        print("🚨 Unauthorized access: No valid user found.")  # ✅ Debug log
        return jsonify({"error": "Unauthorized"}), 401

    try:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "credits": user.credits,
            "last_reset": user.last_reset.isoformat() if user.last_reset else None
        }
        print("✅ User Data:", user_data)  # ✅ Log user data
        return jsonify(user_data), 200
    except Exception as e:
        print("🚨 Error fetching profile:", str(e))
        return jsonify({"error": "An error occurred while fetching the profile"}), 500
