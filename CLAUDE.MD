# CLAUDE.MD

## Project Overview

This document provides context and guidance for Claude AI when working with this codebase.

### Purpose

Life Logger is a web application designed to help users track various aspects of their daily life including mood, sleep, notes, photos, and fitness data. It integrates with the Oura Ring API to pull health metrics and provides a simple, cloud-based solution for personal life logging.

### Technology Stack

- **Languages**: JavaScript (ES6+)
- **Frontend**: React 18, Vite, Tailwind CSS, React Router
- **Backend**: Node.js, Express
- **Database**: Firebase Firestore (NoSQL)
- **Storage**: Firebase Storage (for photos)
- **Authentication**: Firebase Auth
- **External APIs**: Oura Ring API v2
- **Tools**: npm, Firebase CLI

## Project Structure

```
life-logging-app/
├── client/                      # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Login.jsx       # Authentication component
│   │   │   ├── Dashboard.jsx   # Main dashboard
│   │   │   ├── MoodTracker.jsx # Mood tracking
│   │   │   ├── SleepTracker.jsx # Sleep logging
│   │   │   ├── Notes.jsx       # Notes management
│   │   │   ├── Photos.jsx      # Photo uploads
│   │   │   ├── OuraIntegration.jsx # Oura Ring sync
│   │   │   └── WorkoutData.jsx # Workout logging
│   │   ├── firebase.js         # Firebase configuration
│   │   ├── App.jsx             # Main app with routing
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Tailwind styles
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── server/                      # Express backend
│   ├── server.js               # API server with Oura endpoints
│   └── package.json
├── package.json                # Root package.json
├── README.md                   # User documentation
├── CLAUDE.MD                   # This file
└── .gitignore
```

## Development Setup

### Prerequisites

- Node.js v18 or higher
- npm or yarn
- Firebase account (free tier is sufficient)
- Oura Ring account with Personal Access Token (optional)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd life-logging-app

# Install all dependencies (root, client, and server)
npm run install:all

# Or install individually
npm install          # Root
cd client && npm install
cd ../server && npm install
```

### Environment Setup

1. Create Firebase project at https://console.firebase.google.com/
2. Enable Authentication (Email/Password), Firestore, and Storage
3. Copy `client/.env.example` to `client/.env` and add Firebase config
4. Copy `server/.env.example` to `server/.env` (defaults should work)

### Running Locally

```bash
# Run both client and server concurrently
npm run dev

# Or run separately
npm run dev:client    # Runs on http://localhost:3000
npm run dev:server    # Runs on http://localhost:5000
```

### Testing

Currently no automated tests. Manual testing checklist:
- Sign up / Login functionality
- Create mood, sleep, note, photo, workout entries
- View and delete entries
- Oura integration (with valid token)
- Photo upload and display

## Key Files and Components

### Core Files

- `client/src/firebase.js`: Firebase initialization and exports for auth, db, and storage
- `client/src/App.jsx`: Main app with routing and authentication state management
- `server/server.js`: Express API server with Oura integration endpoints
- `client/src/components/Dashboard.jsx`: Main landing page after login
- `client/src/components/*Tracker.jsx`: Individual feature components

### Important Patterns

- **Authentication Flow**: Uses Firebase Auth with email/password. `onAuthStateChanged` in App.jsx manages auth state globally
- **Data Structure**: All Firestore documents include `userId` field for user isolation
- **File Organization**: Each feature is a self-contained component with its own state management
- **API Proxy**: Vite dev server proxies `/api` requests to Express backend (port 5000)
- **Cloud Storage**: Photos stored in Firebase Storage with path pattern `{userId}/{timestamp}_{filename}`
- **Oura Integration**: Backend acts as proxy to avoid exposing API tokens in frontend

## Development Guidelines

### Code Style

- [Formatting preferences, linting rules, etc.]
- [Naming conventions]

### Git Workflow

- **Main Branch**: `main` or `master`
- **Feature Branches**: `feature/<name>` or `claude/<name>`
- **Commit Messages**: [Convention for commit messages]

### Testing Requirements

- [When tests are required]
- [Coverage expectations]

## Common Tasks

### Adding a New Feature

1. [Step-by-step process]
2. [Files typically involved]
3. [Testing approach]

### Debugging

- [Common debugging approaches]
- [Useful commands]
- [Log locations]

## Dependencies

### Key Dependencies

- `[package-name]`: [Why it's used, version constraints]
- `[package-name]`: [Why it's used, version constraints]

### Updating Dependencies

```bash
[commands to update dependencies]
```

## API Documentation

[If applicable: API endpoints, authentication, request/response formats]

## Configuration

### Environment Variables

Client (`client/.env`):
- `VITE_FIREBASE_API_KEY`: Firebase API key from project settings
- `VITE_FIREBASE_AUTH_DOMAIN`: Firebase auth domain
- `VITE_FIREBASE_PROJECT_ID`: Firebase project ID
- `VITE_FIREBASE_STORAGE_BUCKET`: Firebase storage bucket
- `VITE_FIREBASE_MESSAGING_SENDER_ID`: Firebase messaging sender ID
- `VITE_FIREBASE_APP_ID`: Firebase app ID

Server (`server/.env`):
- `PORT`: Server port (default: 5000)

### Configuration Files

- `client/vite.config.js`: Vite configuration with proxy to backend
- `client/tailwind.config.js`: Tailwind CSS configuration
- `client/postcss.config.js`: PostCSS configuration for Tailwind
- Firebase Console: Firestore security rules and Storage rules must be configured

## Deployment

### Production Deployment

[Steps or commands for deploying to production]

### Staging/Testing Environments

[Information about non-production environments]

## Troubleshooting

### Common Issues

**Issue**: [Problem description]
- **Solution**: [How to fix it]

**Issue**: [Problem description]
- **Solution**: [How to fix it]

## Additional Resources

- [Links to external documentation]
- [Related repositories]
- [Team contacts or resources]

## Notes for Claude AI

### Project-Specific Guidance

- **Firebase Configuration**: Never commit `.env` files or Firebase credentials. Always use environment variables
- **Security Rules**: When modifying data structure, ensure Firestore and Storage security rules are updated accordingly
- **Oura API**: Personal Access Tokens are sensitive. They're stored in localStorage on client and passed to backend as query params
- **Component State**: Each component manages its own local state. No global state management (Redux/Context) is used for simplicity
- **Styling**: Uses Tailwind utility classes. Avoid adding custom CSS unless absolutely necessary
- **File Uploads**: Photos are uploaded directly to Firebase Storage from the client, not through the backend

### Areas Requiring Extra Care

- **Authentication State**: Modifying auth flow could break protected routes
- **Firestore Security Rules**: Rules enforce that users can only access their own data via `userId` field
- **API Endpoints**: Backend Oura endpoints expect specific query parameters (`token`, `date`)
- **Environment Variables**: Vite requires `VITE_` prefix for client-side env vars

### Known Limitations

- No automated tests currently implemented
- No data export functionality
- Oura integration requires manual token input (no OAuth flow)
- Photo uploads limited by Firebase Storage quota
- No pagination on data lists (may become slow with many entries)
- No data visualization or charts
- Workout data is manual entry only (no Strava/Apple Health integration yet)

### Testing Strategy

Manual testing workflow:
1. Test authentication (sign up, login, logout, protected routes)
2. Test each feature component (create, view, delete)
3. Test photo uploads and display
4. Test Oura integration with valid token
5. Verify Firebase security rules prevent unauthorized access
6. Test with multiple user accounts to ensure data isolation

### Code Review Checklist

- [ ] No Firebase credentials or API keys committed
- [ ] All Firestore documents include `userId` field
- [ ] Security rules updated if data structure changes
- [ ] Component follows existing patterns (hooks, state management)
- [ ] Tailwind classes used for styling
- [ ] Error handling included for async operations
- [ ] README updated if setup process changes
- [ ] `.env.example` files updated if new variables added

---

**Last Updated**: 2026-01-19
**Maintained By**: Claude AI
