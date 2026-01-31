# Health Data Collection System - Setup Guide

## Overview

This system automatically collects, stores, and analyzes your health data from:
- **Oura Ring** - Sleep, HRV, readiness, activity
- **Google Fit** - Weight, steps, calories
- **MyoAdapt** - Workout exercises with sets/reps/weight
- **Conversations** - Health notes and observations you share with Claude

**No web interface needed** - All data is queried conversationally through Claude Code.

---

## Prerequisites

1. **Firebase Project** - Already set up with Firestore
2. **Firebase Admin Service Account Key** - Download from Firebase Console
3. **Oura Personal Access Token** - From cloud.ouraring.com
4. **Google Fit OAuth Credentials** - Follow GOOGLE_FIT_SETUP.md
5. **Node.js** - Version 18 or higher

---

## One-Time Setup

### Step 1: Install Dependencies

```bash
# Install server dependencies (if not already done)
cd server
npm install

# Install scripts dependencies
cd ../scripts
npm install
```

### Step 2: Get Your Firebase User ID

1. Go to Firebase Console → Authentication
2. Find your user account
3. Copy the UID (looks like: `abc123xyz456...`)
4. Save this - you'll need it for scripts

### Step 3: Download Firebase Admin Key

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Save the JSON file as `firebase-admin-key.json` in the project root
4. **Important:** This file is gitignored - never commit it

### Step 4: Set Environment Variables

Create a `.env` file in the project root:

```bash
# Your Firebase User ID
USER_ID=your-firebase-uid-here

# Google Fit OAuth (from GOOGLE_FIT_SETUP.md)
GOOGLE_FIT_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_FIT_CLIENT_SECRET=your-client-secret
GOOGLE_FIT_REDIRECT_URI=http://localhost:3000/googlefit/callback

# Optional: Custom watch folder for MyoAdapt files
MYOADAPT_WATCH_FOLDER=C:\Users\andre\Downloads
```

**Or** edit the scripts directly and replace `YOUR_USER_ID_HERE` with your actual user ID.

### Step 5: Authorize Oura Ring

```bash
cd scripts
node setup-oura.js
```

Follow the prompts:
1. Enter your Firebase User ID
2. Get your Oura token from: https://cloud.ouraring.com/personal-access-tokens
3. Paste the token

This saves your token to Firestore for automatic syncing.

### Step 6: Authorize Google Fit

First, complete the Google Cloud setup (see GOOGLE_FIT_SETUP.md), then:

```bash
node auth-googlefit.js
```

Follow the prompts:
1. Enter your Firebase User ID
2. Browser opens to Google OAuth
3. Grant permissions
4. Copy the authorization code from the redirect URL
5. Paste it back into the terminal

This saves your refresh token to Firestore for automatic syncing.

---

## Daily Automation Setup

### Option 1: Windows Task Scheduler (Recommended for Windows)

1. Open Task Scheduler
2. Create new task:
   - **Name:** Health Data Daily Sync
   - **Trigger:** Daily at 6:00 AM
   - **Action:** Start a program
     - Program: `node`
     - Arguments: `C:\path\to\Playground-\scripts\daily-sync.js`
     - Start in: `C:\path\to\Playground-\scripts`
   - **Settings:**
     - Run whether user is logged in or not
     - Wake computer to run

### Option 2: Cron (Mac/Linux)

```bash
# Edit crontab
crontab -e

# Add this line (runs at 6 AM daily)
0 6 * * * cd /path/to/Playground-/scripts && node daily-sync.js
```

### Manual Daily Sync (For Testing)

```bash
cd scripts
node daily-sync.js
```

This fetches yesterday's data from Oura and Google Fit and saves it to Firestore.

---

## MyoAdapt Auto-Import Setup

### Start the File Watcher

```bash
cd scripts
node myoadapt-watcher.js
```

This runs continuously, watching your Downloads folder for new CSV files.

**What it does:**
- Monitors `C:\Users\andre\Downloads` (or custom folder)
- Detects new `.csv` files
- Automatically parses and imports workout data
- Saves to `exercises` and `workouts` collections
- Moves processed files to `MyoAdapt_Processed` subfolder

### Run on Startup (Windows)

1. Create a shortcut to `myoadapt-watcher.js`
2. Press `Win+R`, type `shell:startup`
3. Place the shortcut in the Startup folder
4. The watcher will start automatically when you log in

### Run on Startup (Mac)

Use launchd or create a startup script with cron:

```bash
@reboot cd /path/to/Playground-/scripts && node myoadapt-watcher.js
```

---

## Usage

### Querying Your Data (Conversational)

Just ask Claude about your health data:

**Examples:**
- "What's my HRV trend for the last 2 weeks?"
- "Show my bench press progression over 3 months"
- "How's my weight trending?"
- "Did my readiness drop after heavy squat days?"
- "Compare my sleep quality to workout performance"

Claude will:
1. Query Firestore for the relevant data
2. Analyze patterns and trends
3. Generate charts if requested
4. Provide insights

### Logging Health Notes

When you tell Claude something like:
- "I felt really strong today"
- "Bad sleep last night"
- "Legs still sore from Monday"

Claude can log it:

```javascript
// I'll run internally:
await logHealthNote("Felt really strong today", "workout", ["energy", "performance"]);
```

Or you can log manually:

```bash
cd scripts
node log-health-note.js "Felt great after workout" workout
```

### Manual Data Sync

If you want to sync data on-demand (not just daily):

```bash
cd scripts
node daily-sync.js
```

### Check Sync Logs

```bash
# View recent sync activity
cat logs/daily-sync.log

# Or on Windows
type logs\daily-sync.log
```

---

## Firestore Collections

Your data is stored in these collections:

1. **ouraHistory** - Daily Oura Ring data
   - `userId`, `date`, `sleep`, `activity`, `readiness`

2. **bodyMetrics** - Weight tracking
   - `userId`, `date`, `weight`, `source` (googlefit/manual)

3. **dailyActivity** - Steps, calories
   - `userId`, `date`, `steps`, `totalCalories`, `activeMinutes`

4. **exercises** - Individual exercise records
   - `userId`, `date`, `exercise`, `sets`, `totalVolume`, `estimated1RM`

5. **workouts** - Daily workout summaries
   - `userId`, `workoutType`, `duration`, `notes`

6. **healthNotes** - Observations from conversations
   - `userId`, `note`, `category`, `tags`, `date`

7. **userTokens** - OAuth tokens (encrypted)
   - `userId`, `provider`, `accessToken`, `refreshToken`

---

## Firestore Indexes (Required)

Create these composite indexes in Firebase Console:

**Go to:** Firestore Database → Indexes → Composite

1. **exercises**
   - userId (Ascending)
   - exercise (Ascending)
   - date (Descending)

2. **ouraHistory**
   - userId (Ascending)
   - date (Descending)

3. **bodyMetrics**
   - userId (Ascending)
   - date (Descending)

4. **dailyActivity**
   - userId (Ascending)
   - date (Descending)

5. **healthNotes**
   - userId (Ascending)
   - date (Descending)

**Tip:** Firestore will prompt you with index creation links when you first query. Just click the link!

---

## Troubleshooting

### "USER_ID not set" Error

**Solution:** Set the USER_ID environment variable or edit the scripts directly.

### Daily Sync Not Running

**Check:**
1. Task Scheduler task is enabled (Windows)
2. Cron job is set correctly (Mac/Linux)
3. Check logs: `logs/daily-sync.log`

### MyoAdapt Files Not Auto-Importing

**Check:**
1. File watcher is running: `node myoadapt-watcher.js`
2. Watch folder is correct (check MYOADAPT_WATCH_FOLDER)
3. Files are `.csv` format (not `.xlsx`)

### Google Fit Token Expired

The refresh token should auto-renew. If it fails:

```bash
cd scripts
node auth-googlefit.js
```

Re-authorize to get a fresh token.

### Oura API Errors

**Check:**
1. Token is valid: https://cloud.ouraring.com/personal-access-tokens
2. You haven't exceeded API limits (5000 requests/day)

### No Data Showing Up

**Check:**
1. Run `node daily-sync.js` manually to test
2. Check Firestore Console - do the collections exist?
3. Check logs for errors
4. Verify your USER_ID matches your Firebase UID

---

## Security Notes

- **firebase-admin-key.json** - Never commit this file!
- **Tokens** - Stored in Firestore, encrypted in transit
- **Your data** - Stays in YOUR Firebase, you own it
- **OAuth tokens** - Auto-refresh, no manual renewal needed

---

## Quick Reference Commands

```bash
# One-time setup
cd scripts
node setup-oura.js              # Authorize Oura
node auth-googlefit.js          # Authorize Google Fit

# Daily automation
node daily-sync.js              # Sync yesterday's data

# File watching
node myoadapt-watcher.js        # Watch for MyoAdapt CSVs

# Logging notes
node log-health-note.js "note text" category

# View logs
cat ../logs/daily-sync.log
```

---

## What's Next?

1. **Complete one-time setup** (Steps 1-6 above)
2. **Set up daily automation** (Task Scheduler or cron)
3. **Start file watcher** (optional, for MyoAdapt)
4. **Test by asking Claude about your data**

Example first query:
"Can you check if my Oura data is syncing? Show me the last few days."

Claude will query Firestore and show you what's been collected!
