# reset_db.py

from app import create_app, db

# Create the Flask application (so we get the correct app context)
app = create_app()

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()
    print("Database has been reset and created fresh.")
