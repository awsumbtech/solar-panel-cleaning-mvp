from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()

        # Check if test user exists
        if not User.query.filter_by(email='test@example.com').first():
            # Create test user
            test_user = User(
                email='test@example.com',
                password=generate_password_hash('password123'),
                role='technician'
            )
            db.session.add(test_user)
            
            # Create test admin
            admin_user = User(
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)

            # Create some test jobs
            from app import Job
            today = datetime.now().date()
            
            jobs = [
                Job(
                    customer_name='John Smith',
                    address='123 Main St, City',
                    scheduled_date=datetime.combine(today, datetime.strptime('09:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                ),
                Job(
                    customer_name='Jane Doe',
                    address='456 Oak Ave, Town',
                    scheduled_date=datetime.combine(today, datetime.strptime('11:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                ),
                Job(
                    customer_name='Bob Wilson',
                    address='789 Pine Rd, Village',
                    scheduled_date=datetime.combine(today, datetime.strptime('14:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                ),
                # Add a job for tomorrow
                Job(
                    customer_name='Alice Brown',
                    address='321 Elm St, City',
                    scheduled_date=datetime.combine(today + timedelta(days=1), datetime.strptime('10:00', '%H:%M').time()),
                    technician_id=test_user.id,
                    status='pending'
                )
            ]
            
            for job in jobs:
                db.session.add(job)

            db.session.commit()
            print("Database initialized with test data")
        else:
            print("Test data already exists")

if __name__ == '__main__':
    init_db() 