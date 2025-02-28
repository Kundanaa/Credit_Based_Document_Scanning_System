# app.py - Main Flask App
from flask import Flask
from extensions import db, bcrypt
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from models.admin import Admin

# Initialize extensions (Do NOT bind them to app yet)
login_manager = LoginManager()
#login_manager.login_view = 'auth.login'
@login_manager.user_loader

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # ✅ Allow all origins
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    # Import and register Blueprints inside the function
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.scan_routes import scan_bp
    from routes.credit_routes import credit_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(scan_bp, url_prefix='/scan')
    app.register_blueprint(credit_bp, url_prefix='/credits')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        Admin.create_admin()  
    app.run(host='0.0.0.0', port=5000, debug=True)


