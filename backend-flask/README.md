Backend (Flask)

Requirements:
- Python 3.8+

Quick start (Windows PowerShell):

# Create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install flask flask_sqlalchemy flask_jwt_extended flask_cors werkzeug

# Run
python app.py

Notes:
- The app will create a `users.db` SQLite file on first run.
- Change `JWT_SECRET_KEY` to an environment variable before production.
