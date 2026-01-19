# Life Logger

A simple life logging web application that helps you track your mood, sleep, notes, photos, and fitness data. Includes integration with Oura Ring for health tracking.

## Features

- **Mood Tracking** - Log your daily mood with notes
- **Sleep Tracking** - Track sleep duration and quality
- **Notes** - Create and manage personal notes
- **Photos** - Upload and organize photos with captions
- **Oura Ring Integration** - Sync sleep, activity, and readiness data from your Oura Ring
- **Workout Data** - Log workouts with duration, calories, and distance
- **Cloud Storage** - All data stored securely in Firebase
- **User Authentication** - Secure sign up and login

## Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Firebase SDK (Authentication, Firestore, Storage)
- Axios
- Lucide React (icons)
- date-fns

### Backend
- Node.js
- Express
- Firebase Admin SDK
- Axios (for Oura API integration)

## Project Structure

```
life-logging-app/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── firebase.js    # Firebase configuration
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── index.html
│   └── package.json
├── server/                # Express backend
│   ├── server.js         # API server
│   └── package.json
├── package.json          # Root package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Firebase account
- Oura Ring account (optional, for Oura integration)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd life-logging-app
```

### 2. Install Dependencies

```bash
npm run install:all
```

This will install dependencies for the root, client, and server.

### 3. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Authentication:
   - Go to Authentication > Sign-in method
   - Enable "Email/Password"
4. Create a Firestore database:
   - Go to Firestore Database
   - Create database (start in production mode)
5. Enable Storage:
   - Go to Storage
   - Get started
6. Get your Firebase configuration:
   - Go to Project Settings > General
   - Scroll to "Your apps" and click the web icon (</>)
   - Copy the configuration object

### 4. Configure Environment Variables

#### Client (.env)

Create a `client/.env` file:

```bash
cd client
cp .env.example .env
```

Edit `client/.env` and add your Firebase configuration:

```
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

#### Server (.env)

Create a `server/.env` file:

```bash
cd server
cp .env.example .env
```

Edit if needed (defaults should work):

```
PORT=5000
```

### 5. Configure Firebase Security Rules

#### Firestore Rules

Go to Firestore Database > Rules and set:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null;
    }
  }
}
```

#### Storage Rules

Go to Storage > Rules and set:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 6. Run the Application

#### Development Mode

Run both client and server concurrently:

```bash
npm run dev
```

Or run them separately:

```bash
# Terminal 1 - Client
npm run dev:client

# Terminal 2 - Server
npm run dev:server
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### 7. Set Up Oura Integration (Optional)

1. Go to [Oura Cloud](https://cloud.ouraring.com/personal-access-tokens)
2. Create a Personal Access Token
3. In the app, navigate to "Oura Integration"
4. Click "Connect Oura Ring" and paste your token

## Usage

### First Time Setup

1. Open http://localhost:3000
2. Click "Sign Up" to create an account
3. Log in with your credentials
4. Start tracking your life!

### Features Guide

- **Mood Tracker**: Select your mood and add optional notes
- **Sleep Tracker**: Enter hours slept and rate your sleep quality
- **Notes**: Create personal notes with titles and content
- **Photos**: Upload images with optional captions
- **Oura Integration**: Connect your Oura Ring to automatically sync health data
- **Workout Data**: Log workouts manually or integrate with fitness apps

## Building for Production

### Build the Client

```bash
cd client
npm run build
```

The built files will be in `client/dist/`.

### Deploy

You can deploy the client to:
- Firebase Hosting
- Vercel
- Netlify
- Any static hosting service

Deploy the server to:
- Railway
- Render
- Heroku
- Any Node.js hosting service

## API Endpoints

### Oura Integration

- `GET /api/oura/sleep?token=TOKEN&date=YYYY-MM-DD` - Get sleep data
- `GET /api/oura/activity?token=TOKEN&date=YYYY-MM-DD` - Get activity data
- `GET /api/oura/readiness?token=TOKEN&date=YYYY-MM-DD` - Get readiness data

### Health Check

- `GET /api/health` - Check if the API is running

## Firestore Collections

- `moods` - Mood tracking entries
- `sleep` - Sleep tracking entries
- `notes` - Personal notes
- `photos` - Photo metadata (actual images in Storage)
- `workouts` - Workout entries

## Troubleshooting

### Firebase Authentication Error

Make sure you've enabled Email/Password authentication in Firebase Console.

### Images Not Uploading

Check that Firebase Storage is enabled and security rules are configured correctly.

### Oura Data Not Loading

Verify your Personal Access Token is valid and hasn't expired. Get a new one from the Oura Cloud portal.

### CORS Errors

Make sure the backend server is running on port 5000 and the proxy is configured in `client/vite.config.js`.

## Future Enhancements

- Strava integration for workout data
- Apple Health / Google Fit integration
- Data visualization and charts
- Export data to CSV/PDF
- Habit tracking
- Goal setting and tracking
- Dark mode
- Mobile app version

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT

## Support

For questions or issues, please open a GitHub issue.
