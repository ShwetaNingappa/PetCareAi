import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app, db

with app.app_context():
    db.create_all()
    print('Database tables created')
from app import db, app
with app.app_context():
    db.create_all()
    print('created')
