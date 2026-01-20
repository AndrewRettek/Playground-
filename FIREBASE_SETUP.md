# Firebase Setup Checklist

Your Firebase config is now in `client/.env` ✓

## Complete These Steps in Firebase Console

Go to: https://console.firebase.google.com/project/lifelogger-e6ecd

### 1. Enable Authentication ✓ or ✗

1. Click "**Authentication**" in left sidebar (under "Build")
2. Click "**Get started**" button
3. Click "**Sign-in method**" tab
4. Click on "**Email/Password**"
5. Toggle "**Enable**" to ON
6. Click "**Save**"

### 2. Create Firestore Database ✓ or ✗

1. Click "**Firestore Database**" in left sidebar
2. Click "**Create database**"
3. Choose "**Start in production mode**"
4. Click "**Next**"
5. Select a location (e.g., us-central)
6. Click "**Enable**"
7. Go to "**Rules**" tab
8. Replace with these rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{collection}/{document} {
      allow read, write: if request.auth != null &&
                          request.auth.uid == resource.data.userId;
      allow create: if request.auth != null &&
                       request.auth.uid == request.resource.data.userId;
    }
  }
}
```

9. Click "**Publish**"

### 3. Enable Storage ✓ or ✗

1. Click "**Storage**" in left sidebar
2. Click "**Get started**"
3. Click "**Next**" (accept default rules for now)
4. Choose same location as Firestore
5. Click "**Done**"
6. Go to "**Rules**" tab
7. Replace with these rules:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{userId}/{allPaths=**} {
      allow read, write: if request.auth != null &&
                          request.auth.uid == userId;
    }
  }
}
```

8. Click "**Publish**"

## After Completing All Steps

Run these commands:

```bash
# Install dependencies (if you haven't already)
npm run install:all

# Start the app
npm run dev
```

Then open http://localhost:3000 and test:
1. Sign up with email/password
2. Try logging a mood
3. Try uploading a photo

---

**Mark each section with ✓ when complete!**
