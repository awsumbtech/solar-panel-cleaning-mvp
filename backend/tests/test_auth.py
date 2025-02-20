import pytest
from app import app, db, User
from werkzeug.security import generate_password_hash
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
        yield client
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_login_success(client):
    response = client.post('/api/auth/login',
        json={'email': 'test@example.com', 'password': 'password123'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'
    assert data['user']['role'] == 'technician'

def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login',
        json={'email': 'test@example.com', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials' 