# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Compute the absolute paths for your shared templates/ and static/ folders
    basedir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(basedir, '..', 'templates')
    static_dir   = os.path.join(basedir, '..', 'static')

    # Tell Flask to use those folders
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register your blueprint
    from .routes import polls_bp
    app.register_blueprint(polls_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
