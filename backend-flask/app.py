from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Use env var in production

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    text = db.Column(db.Text, nullable=True)
    meta = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    session = db.relationship('ChatSession', backref=db.backref('messages', lazy=True))


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify(message='Email and password required'), 400
    # check existing
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify(message='User already exists'), 409
    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    # create token so frontend can auto-login
    token = create_access_token(identity=email)
    return jsonify(message="User created successfully", access_token=token), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        token = create_access_token(identity=user.email)
        return jsonify(access_token=token)
    return jsonify(message="Invalid credentials"), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="You are viewing a protected route")


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json() or {}
    text = (data.get('text') or data.get('symptom') or '') or ''
    text = text.lower()

    suggestions = []

    # Simple keyword matching for demo purposes. Not medically accurate.
    if any(k in text for k in ['vomit', 'vomiting', 'throw up', 'puke']):
        suggestions.append({
            'disease': 'Gastroenteritis',
            'confidence': 0.85,
            'prescription': 'Keep hydrated, small frequent water; withhold food 12-24h. See a vet if persistent.'
        })
        suggestions.append({
            'disease': 'Food poisoning',
            'confidence': 0.6,
            'prescription': 'Remove access to suspected toxin, monitor closely and consult your vet immediately if severe.'
        })

    if any(k in text for k in ['diarrhea', 'poop', 'runny stool', 'loose stool']):
        suggestions.append({
            'disease': 'Acute diarrhea (viral/bacterial)',
            'confidence': 0.75,
            'prescription': 'Maintain hydration, consider electrolyte solution, consult vet if bloody stool or prolonged symptoms.'
        })

    if any(k in text for k in ['itch', 'scratching', 'flea', 'fleas', 'mange', 'rash', 'hot spot']):
        suggestions.append({
            'disease': 'Skin irritation / parasitic infestation',
            'confidence': 0.72,
            'prescription': 'Check for fleas/ticks and consult your vet for appropriate topical or systemic therapy.'
        })

    if any(k in text for k in ['ear', 'earache', 'head shaking', 'ear discharge', 'ear infection']):
        suggestions.append({
            'disease': 'Otitis (ear infection)',
            'confidence': 0.7,
            'prescription': 'Keep ear dry and see a vet for otic/topical treatment after examination.'
        })

    if any(k in text for k in ['cough', 'sneeze', 'nasal', 'wheeze', 'congest']):
        suggestions.append({
            'disease': 'Upper respiratory infection',
            'confidence': 0.65,
            'prescription': 'Provide warmth and humidity; seek vet care if breathing is labored.'
        })

    if any(k in text for k in ['pee blood', 'blood in urine', 'straining to pee', 'urinate often', 'uti']):
        suggestions.append({
            'disease': 'Urinary tract infection / cystitis',
            'confidence': 0.7,
            'prescription': 'Encourage water intake and seek veterinary testing/treatment.'
        })

    if any(k in text for k in ['limp', 'limping', 'lame', 'not putting weight']):
        suggestions.append({
            'disease': 'Musculoskeletal injury / arthritis',
            'confidence': 0.7,
            'prescription': 'Restrict activity and consult your vet for diagnosis and pain management.'
        })

    if any(k in text for k in ['allergy', 'allergic', 'hives', 'swelling', 'itchy eyes']):
        suggestions.append({
            'disease': 'Allergic reaction',
            'confidence': 0.6,
            'prescription': 'Remove allergen and seek urgent care if face swelling or difficulty breathing occurs.'
        })

    if any(k in text for k in ['heatstroke', 'overheat', 'hot', 'panting heavily', 'collapse']):
        suggestions.append({
            'disease': 'Heatstroke',
            'confidence': 0.9,
            'prescription': 'Move to cool area, apply cool (not cold) water, and get emergency veterinary care immediately.'
        })

    if any(k in text for k in ['poison', 'toxin', 'ingested', 'chocolate', 'grapes', 'xylitol']):
        suggestions.append({
            'disease': 'Possible poisoning',
            'confidence': 0.85,
            'prescription': 'Contact an emergency vet or poison control; do not induce vomiting without professional instruction.'
        })

    if any(k in text for k in ['dental', 'bad breath', 'tooth', 'gum', 'chew abnormal']):
        suggestions.append({
            'disease': 'Dental disease',
            'confidence': 0.6,
            'prescription': 'Schedule a vet dental check; severe cases may need cleaning or extractions.'
        })

    if any(k in text for k in ['eye', 'eye discharge', 'red eye', 'cloudy eye']):
        suggestions.append({
            'disease': 'Conjunctivitis / eye infection',
            'confidence': 0.6,
            'prescription': 'Keep the eye clean with saline and consult your vet for topical therapy.'
        })

    if any(k in text for k in ['tick', 'ticks', 'flea', 'fleas']):
        suggestions.append({
            'disease': 'Ticks / fleas',
            'confidence': 0.8,
            'prescription': 'Remove ticks carefully and treat with vet-approved products.'
        })

    if any(k in text for k in ['obese', 'overweight', 'weight gain', 'fat']):
        suggestions.append({
            'disease': 'Obesity / weight-related issues',
            'confidence': 0.65,
            'prescription': 'Discuss a weight-loss plan with your vet including diet and exercise.'
        })

    # fallback
    if not suggestions:
        suggestions = [
            {
                'disease': 'General checkup needed',
                'confidence': 0.3,
                'prescription': 'Symptoms unclear; consult a veterinarian for accurate diagnosis.'
            }
        ]

    return jsonify(suggestions=suggestions)


@app.route('/sessions', methods=['POST'])
def create_session():
    s = ChatSession()
    db.session.add(s)
    db.session.commit()
    return jsonify(session_id=s.id), 201


@app.route('/sessions/<int:session_id>/messages', methods=['GET', 'POST'])
def session_messages(session_id):
    session = ChatSession.query.get_or_404(session_id)
    if request.method == 'GET':
        msgs = [
            {
                'id': m.id,
                'sender': m.sender,
                'text': m.text,
                'meta': m.meta,
                'created_at': m.created_at.isoformat()
            }
            for m in session.messages
        ]
        return jsonify(messages=msgs)
    else:
        data = request.get_json() or {}
        sender = data.get('sender')
        text = data.get('text')
        meta = data.get('meta')
        if sender not in ('user', 'bot'):
            return jsonify(message='sender must be user or bot'), 400
        m = Message(session_id=session.id, sender=sender, text=text, meta=meta)
        db.session.add(m)
        db.session.commit()
        return jsonify(id=m.id, sender=m.sender, text=m.text, meta=m.meta), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run without the reloader so a single foreground process binds and is easier to manage on Windows
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)