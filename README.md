# Solar Panel Cleaning Service MVP

A full-stack application for managing solar panel cleaning services, consisting of a Flask backend API and a React Native mobile app.

## Project Structure

```
solar-cleaning-mvp/
├── backend/               # Flask backend
│   ├── app.py            # Main application file
│   ├── config.py         # Configuration settings
│   ├── requirements.txt  # Python dependencies
│   └── tests/            # Backend tests
├── mobile/               # React Native mobile app
│   ├── src/
│   │   ├── screens/      # App screens
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API services
│   │   └── navigation/   # Navigation setup
│   ├── App.tsx          # Root component
│   └── package.json     # JavaScript dependencies
```

## Backend Setup

1. Create and activate virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other settings
   ```

4. Initialize database:
   ```bash
   flask db upgrade
   ```

5. Run the development server:
   ```bash
   flask run
   ```

## Mobile App Setup

1. Install dependencies:
   ```bash
   cd mobile
   npm install
   ```

2. iOS setup:
   ```bash
   cd ios
   pod install
   cd ..
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Run on iOS:
   ```bash
   npm run ios
   ```

5. Run on Android:
   ```bash
   npm run android
   ```

## Features

- User authentication
- Job management
- Photo capture and storage
- GPS location tracking
- Offline data synchronization
- Job completion workflow

## API Endpoints

### Authentication
- POST /api/auth/login - User login

### Jobs
- GET /api/jobs/today - Get today's jobs
- POST /api/jobs/{id}/complete - Mark job as complete
- POST /api/jobs/{id}/photos - Upload job photos

## Mobile App Screens

1. Login Screen
   - Email/password authentication
   - Secure token storage

2. Jobs Screen
   - List of today's jobs
   - Job status indicators
   - Pull-to-refresh

3. Job Detail Screen
   - Job information
   - Photo capture
   - Job completion
   - GPS location tracking

## Development Guidelines

1. Code Style
   - Follow PEP 8 for Python code
   - Use ESLint rules for JavaScript/TypeScript
   - Include type hints and TypeScript types

2. Testing
   - Write unit tests for core functionality
   - Test offline capabilities
   - Test error scenarios

3. Security
   - Implement proper authentication
   - Secure file uploads
   - Validate all inputs
   - Handle sensitive data properly

4. Performance
   - Optimize database queries
   - Implement proper caching
   - Handle offline data efficiently

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 