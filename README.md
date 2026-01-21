# Life Logger

A simple web app to track your mood, sleep, notes, photos, and fitness data. Includes Oura Ring integration for health tracking.

## ✨ Features

- **Mood Tracking** - Log your daily mood with notes
- **Sleep Tracking** - Track sleep duration and quality
- **Notes** - Create and manage personal notes
- **Photos** - Upload and organize photos with captions
- **Oura Ring Integration** - Sync sleep, activity, and readiness data
- **Workout Data** - Log workouts with duration, calories, and distance
- **Cloud Storage** - All data stored securely in Firebase
- **User Authentication** - Secure sign up and login

## 🚀 Quick Start

**Never set up an app before? No problem!**

### For Beginners (Windows):

1. Open **`GETTING_STARTED.md`** and follow the step-by-step guide
2. It takes about 15 minutes total
3. Everything is automated - just double-click a few files!

### For Developers:

See the detailed technical documentation below.

---

## 💻 Tech Stack

- **Frontend:** React 18, Vite, Tailwind CSS, React Router, Firebase SDK
- **Backend:** Node.js, Express, Firebase Admin SDK
- **Database:** Firebase Firestore
- **Storage:** Firebase Storage
- **APIs:** Oura Ring API v2

## 📁 Project Files

- **`GETTING_STARTED.md`** - Complete setup guide for beginners
- **`FIREBASE_CONSOLE_SETUP.md`** - How to enable Firebase services
- **`INSTALL_NODEJS.md`** - How to install Node.js
- **`setup.bat`** - Automated setup script (Windows)
- **`firebase-init.bat`** - Connect to Firebase (Windows)
- **`deploy-rules.bat`** - Deploy security rules (Windows)
- **`start.bat`** - Start the app (Windows)
- **`client/`** - React frontend
- **`server/`** - Express backend

## 📋 Setup Instructions

### Option A: Automated Setup (Windows - Recommended for Beginners)

**Perfect if you've never set up an app before!**

1. **Read** `GETTING_STARTED.md` - Complete walkthrough
2. **Double-click** `setup.bat` - Installs everything automatically
3. **Follow** `FIREBASE_CONSOLE_SETUP.md` - Enable Firebase services (5 min)
4. **Double-click** `firebase-init.bat` - Connect to Firebase
5. **Double-click** `deploy-rules.bat` - Deploy security rules
6. **Double-click** `start.bat` - Launch the app!

**Total time:** ~15 minutes

### Option B: Manual Setup (All Platforms)

<details>
<summary>Click to expand manual setup instructions</summary>

#### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Firebase account

#### 1. Install Dependencies

```bash
npm run install:all
```

#### 2. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Authentication (Email/Password)
4. Create Firestore Database
5. Enable Cloud Storage
6. Get your Firebase configuration from Project Settings

#### 3. Configure Environment Variables

Create `client/.env`:

```bash
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

#### 4. Deploy Firebase Security Rules

```bash
firebase login
firebase use --add
firebase init firestore
firebase init storage
firebase deploy --only firestore:rules,storage
```

#### 5. Run the Application

```bash
npm run dev
```

Open http://localhost:3000

</details>

### Option C: Using Firebase CLI Only

<details>
<summary>Click to expand Firebase CLI instructions</summary>

```bash
# Install dependencies
npm run install:all

# Setup Firebase
firebase login
firebase use --add  # Select your project
firebase init firestore
firebase init storage
firebase deploy --only firestore:rules,storage

# Start the app
npm run dev
```

</details>

## 📱 Using the App

1. **Start the app** (double-click `start.bat` or run `npm run dev`)
2. **Open** http://localhost:3000 in your browser
3. **Sign up** with email and password
4. **Start logging** your mood, sleep, notes, photos, and workouts!

### Optional: Connect Oura Ring

1. Get your Personal Access Token from [Oura Cloud](https://cloud.ouraring.com/personal-access-tokens)
2. In the app, go to "Oura Integration"
3. Enter your token
4. View your sleep, activity, and readiness scores!

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

## ❓ Troubleshooting

**App won't start?**
- Check Node.js is installed: `node --version`
- Run `setup.bat` again

**Can't create an account?**
- Make sure Authentication is enabled in Firebase Console
- See `FIREBASE_CONSOLE_SETUP.md`

**Photos won't upload?**
- Make sure Storage is enabled in Firebase Console
- Run `deploy-rules.bat`

**More help?** Open `GETTING_STARTED.md` for detailed troubleshooting.

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
