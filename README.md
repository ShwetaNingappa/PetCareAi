# PetCareAi

PetCare AI is an AI-powered chatbot for animal disease diagnosis and prescription recommendations. Using React, Node.js, and Python/Flask, it helps pet owners and vets by analyzing symptoms and providing timely advice to improve animal healthcare.

Project root

This repository contains a Flask backend and a React frontend.

Quick start (Windows PowerShell)

1) Backend (Flask)
   cd backend-flask
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt   # or pip install flask flask_sqlalchemy flask_jwt_extended flask_cors werkzeug
   python app.py

2) Frontend (React)
   cd frontend-react
   npm install
   npm start

3) Or run both from the root (requires Node/npm installed):
   npm install
   npm run dev

Notes
- The `npm run dev` script runs the React dev server and the Flask app in parallel. It does not create/activate the Python venv — activate the venv manually before using `npm run dev` if you prefer running Flask inside the venv.
- For production, use proper env vars for JWT secrets and a production-ready WSGI server.
