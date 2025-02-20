import pytest
from app import app, db, User, Job
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/solar_cleaning_test'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create test user
            test_user = User(
                email='test@example.com',
                password=generate_password_hash('password123'),
                role='technician'
            )
            db.session.add(test_user)
            db.session.commit()
            
            # Create test jobs
            today = datetime.utcnow().date()
            jobs = [
                Job(
                    customer_name='Test Customer 1',
                    address='123 Test St',
                    scheduled_date=datetime.combine(today, datetime.strptime('10:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                ),
                Job(
                    customer_name='Test Customer 2',
                    address='456 Test Ave',
                    scheduled_date=datetime.combine(today + timedelta(days=1), datetime.strptime('14:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                )
            ]
            for job in jobs:
                db.session.add(job)
            db.session.commit()
            
        yield client
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

def get_auth_token(client):
    response = client.post('/api/auth/login',
        json={'email': 'test@example.com', 'password': 'password123'}
    )
    return json.loads(response.data)['access_token']

def test_get_today_jobs(client):
    token = get_auth_token(client)
    response = client.get('/api/jobs/today',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['customer_name'] == 'Test Customer 1'

def test_complete_job(client):
    token = get_auth_token(client)
    
    # Get the first job
    response = client.get('/api/jobs/today',
        headers={'Authorization': f'Bearer {token}'}
    )
    job = json.loads(response.data)[0]
    
    # Complete the job
    response = client.post(f'/api/jobs/{job["id"]}/complete',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    
    # Verify job is completed
    response = client.get('/api/jobs/today',
        headers={'Authorization': f'Bearer {token}'}
    )
    updated_job = json.loads(response.data)[0]
    assert updated_job['status'] == 'completed'

def test_unauthorized_access(client):
    response = client.get('/api/jobs/today')
    assert response.status_code == 401
    
    response = client.post('/api/jobs/1/complete')
    assert response.status_code == 401 