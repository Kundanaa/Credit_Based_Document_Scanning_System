# routes/auth_routes.py - Authentication Routes
from flask import Blueprint, request, jsonify, current_app, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from extensions import db ,bcrypt  # Now we import db and login_manager correctly
from app import login_manager
from flask_cors import CORS
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)
CORS(auth_bp, supports_credentials=True)  # ✅ Enable CORS for this route
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['POST'])
def register():
    # if request.method=='POST':
    #     username=request.form.get('username')
    #     email=request.form.get('email')
    #     password1=request.form.get('password1')
    #     password2=request.form.get('password2')
    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         flash('Email already exists.',category='error')
    #     elif len(username)<2:
    #         flash('Username must be greater than 1 character.',category='error')
    #     elif len(email)<4:
    #         flash('Email must be greater than 3 characters.',category='error')
    #     elif password1!=password2:
    #         flash('Passwords don\'t match.',category='error')
    #     elif len(password1)<5:
    #         flash('Password must be at least 5 characters.',category='error')
    #     else:
    #         new_user = User(username=username, email=email, password=generate_password_hash(password1, method='sha256'))
    #         db.session.add(new_user)
    #         db.session.commit()
    #         login_user(new_user, remember=True)
    #         flash('Account Created Succesfully!', category='success')
    #         return redirect(url_for('user.profile'))
    # return render_template("register.html",user=current_user)
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # if request.method=='POST':
    #     email=request.form.get('email')
    #     password=request.form.get('password')
    #     user=User.query.filter_by(email=email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             flash('Logged In Successfully!', category='success')
    #             login_user(user,remember=True)
    #             return redirect(url_for('user.profile'))
    #         else:
    #             flash('Incorrect Password, Try Again!', category='error')
    #     else:
    #         flash('Email doesn\'t exist',category='error')
    # return render_template("login.html", user=current_user)

    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        # ✅ Generate JWT Token
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expire in 24 hours
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'message': 'Login successful', 'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

