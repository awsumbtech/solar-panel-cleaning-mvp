from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/solar_cleaning')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    jobs = db.relationship('Job', backref='technician', lazy=True)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    photos = db.relationship('JobPhoto', backref='job', lazy=True)

class JobPhoto(db.Model):
    __tablename__ = 'job_photos'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    photo_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/jobs/today', methods=['GET'])
@jwt_required()
def get_today_jobs():
    user_id = get_jwt_identity()
    today = datetime.utcnow().date()
    jobs = Job.query.filter(
        Job.technician_id == user_id,
        db.func.date(Job.scheduled_date) == today
    ).all()
    
    return jsonify([{
        'id': job.id,
        'address': job.address,
        'customer_name': job.customer_name,
        'scheduled_date': job.scheduled_date.isoformat(),
        'status': job.status
    } for job in jobs]), 200

@app.route('/api/jobs/<int:job_id>/complete', methods=['POST'])
@jwt_required()
def complete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.technician_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    
    job.status = 'completed'
    db.session.commit()
    return jsonify({'message': 'Job marked as complete'}), 200

@app.route('/api/jobs/<int:job_id>/photos', methods=['POST'])
@jwt_required()
def upload_job_photo(job_id):
    if 'photo' not in request.files:
        return jsonify({'message': 'No photo provided'}), 400
    
    job = Job.query.get_or_404(job_id)
    if job.technician_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403
    
    photo = request.files['photo']
    if photo:
        filename = f"{job_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jpg"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        
        job_photo = JobPhoto(job_id=job_id, photo_path=filename)
        db.session.add(job_photo)
        db.session.commit()
        
        return jsonify({'message': 'Photo uploaded successfully'}), 201
    
    return jsonify({'message': 'Invalid photo'}), 400

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True) 