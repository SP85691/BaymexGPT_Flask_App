from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Create the database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gpt.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "this_is_my_secret_key"
    app.permanent_session_lifetime = timedelta(minutes=10)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from .blueprints.auth import auth
    from .blueprints.main import main
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User, Chat

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def make_session_permanent():
        session.permanent = False

    # Create Flask-Admin panel
    admin = Admin(app, name='Control Panel')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Chat, db.session))
    
    with app.app_context():
        db.create_all()

    return app
