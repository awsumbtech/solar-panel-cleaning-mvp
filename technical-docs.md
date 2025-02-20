# Solar Panel Cleaning MVP - Technical Documentation

## Project Structure
```
solar-cleaning-mvp/
├── backend/
│   ├── venv/
│   ├── app.py                 # Main Flask application
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   └── uploads/             # Photo storage directory
├── mobile/
│   ├── android/             # Android native files
│   ├── ios/                 # iOS native files
│   ├── src/
│   │   ├── screens/         # React Native screens
│   │   ├── components/      # Reusable components
│   │   └── services/        # API services
│   ├── App.js              # Main React Native app
│   └── package.json        # JavaScript dependencies
└── README.md
```

## Current Implementation

### Backend (Flask)

#### Dependencies
```
flask==2.3.3
flask-sqlalchemy==3.1.1
flask-jwt-extended==4.5.2
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    scheduled_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    technician_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Implemented API Endpoints
```
POST /api/auth/login           # User authentication
GET  /api/jobs/today          # Fetch today's jobs
POST /api/jobs/{id}/complete  # Mark job as complete
```

### Mobile App (React Native)

#### Dependencies
```json
{
  "@react-navigation/native": "^6.1.9",
  "@react-navigation/native-stack": "^6.9.17",
  "@react-native-async-storage/async-storage": "^1.21.0",
  "react-native": "0.73.2"
}
```

#### Implemented Screens
- LoginScreen
- JobsScreen

#### Features
- JWT Authentication
- Job listing
- Basic navigation to job sites
- Offline data storage
- Job completion marking

## Immediate Next Steps

### 1. Photo Capture Implementation
```
backend/
├── app.py
    # Add new endpoint:
    POST /api/jobs/{id}/photos
    
mobile/
├── src/
    ├── components/
    │   └── CameraComponent.js     # Camera functionality
    └── screens/
        └── JobDetailScreen.js     # Photo capture UI
```

### 2. Customer Management
```
backend/
├── app.py
    # Add new endpoints:
    POST /api/customers
    GET  /api/customers
    GET  /api/customers/{id}
    
mobile/
├── src/
    └── screens/
        └── CustomersScreen.js    # Customer management UI
```

### 3. Admin Dashboard
```
backend/
├── app.py
    # Add new endpoints:
    GET  /api/jobs/all
    POST /api/jobs
    PUT  /api/jobs/{id}
    
mobile/
├── src/
    └── screens/
        ├── AdminDashboard.js    # Admin overview
        └── JobScheduling.js     # Job creation/editing
```

## Development Roadmap

### Phase 1: Core Features (Current MVP)
- [x] Basic authentication
- [x] Job listing
- [x] Job completion
- [x] Navigation integration

### Phase 2: Enhanced Features
- [ ] Photo capture and storage
- [ ] Customer management
- [ ] Admin dashboard
- [ ] Job scheduling
- [ ] Basic reporting

### Phase 3: Advanced Features
- [ ] Offline sync
- [ ] Push notifications
- [ ] Weather integration
- [ ] Route optimization
- [ ] Payment processing

## Testing Setup

### Backend Tests
```
backend/
├── tests/
    ├── test_auth.py       # Authentication tests
    ├── test_jobs.py       # Job management tests
    └── conftest.py        # Test configurations
```

### Mobile Tests
```
mobile/
├── __tests__/
    ├── App.test.js        # App component tests
    ├── Login.test.js      # Login screen tests
    └── Jobs.test.js       # Jobs screen tests
```

## Environment Setup

### Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
flask db upgrade
```

### Mobile
```bash
# Install dependencies
npm install

# Run on Android
npx react-native run-android

# Run on iOS
cd ios && pod install
cd .. && npx react-native run-ios
```

## Configuration Files

### Backend (.env)
```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/solar_cleaning
JWT_SECRET_KEY=your-secret-key
```

### Mobile (config.js)
```javascript
export const config = {
  API_URL: 'http://localhost:5000/api',
  STORAGE_KEY: '@solar_cleaning_app',
  PHOTO_QUALITY: 0.8,
  MAX_OFFLINE_DAYS: 7
};
```

## Security Considerations
- JWT token expiration
- Password hashing
- Role-based access control
- Secure file uploads
- API rate limiting

## Known Issues
1. Need to handle token refresh
2. Offline sync conflicts
3. Photo upload size limitations
4. GPS accuracy improvements needed

## Next Development Sprint
1. Implement photo capture
2. Add customer management
3. Create admin dashboard
4. Enhance offline capabilities
5. Add basic analytics

Would you like me to detail any specific part of this technical breakdown further?