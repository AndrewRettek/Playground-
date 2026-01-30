# Health Data Collection + AI Query System

## Architecture Overview

**What this does:**
- Automatically collects health data daily from Oura Ring and Google Fit
- Auto-imports MyoAdapt workout files when you download them
- Logs health observations from our conversations
- Lets you ask me questions about your data anytime
- Generates charts on demand when you want visual analysis

**What this doesn't do:**
- No web app
- No login/authentication UI
- No manual clicking around

---

## Components

### 1. Daily Data Sync (Automated)
**File:** `scripts/daily-sync.js`

Runs automatically every day at 6 AM:
- Fetches yesterday's Oura Ring data (sleep, activity, readiness)
- Fetches yesterday's Google Fit data (weight, steps, calories)
- Saves everything to Firestore
- Logs results to `logs/daily-sync.log`

**Setup:** Windows Task Scheduler runs this daily

### 2. MyoAdapt Auto-Import (File Watcher)
**File:** `scripts/myoadapt-watcher.js`

Watches your Downloads folder (or wherever you save MyoAdapt exports):
- Detects new `.csv` files
- Automatically parses and imports workout data
- Saves to `exercises` and `workouts` collections
- Moves processed files to `MyoAdapt/processed/` folder

**Setup:** Runs continuously in background

### 3. Conversation Health Logger
**How it works:**
- When you tell me things like "I felt great today" or "bad workout, felt weak"
- I save it to Firestore `healthNotes` collection with:
  - Date
  - Your note text
  - Category (mood, recovery, workout quality, etc.)
  - Any relevant tags

### 4. Data Query & Analysis
**How it works:**
- You ask me: "Show my HRV trend for the last month"
- I query Firestore
- Analyze the data
- Generate a chart if you want one
- Explain patterns and insights

**Example queries you can ask:**
- "What's my average sleep score this week?"
- "Show bench press progression over 3 months"
- "Did my HRV drop after high-volume workouts?"
- "How's my weight trending during this cut?"
- "Compare my readiness scores to workout performance"

---

## Data Storage (Firestore Collections)

All data stored in your Firebase:

1. **ouraHistory** - Daily Oura Ring data
2. **exercises** - Individual exercise records from MyoAdapt
3. **workouts** - Daily workout summaries
4. **bodyMetrics** - Weight from Google Fit
5. **dailyActivity** - Steps/calories from Google Fit
6. **healthNotes** - Observations from our conversations

---

## Setup Steps

### One-Time Setup

1. **Google Fit OAuth:**
   - Follow `GOOGLE_FIT_SETUP.md` to get credentials
   - Run initial auth: `node scripts/auth-googlefit.js`
   - Stores tokens in Firestore (never expires with refresh token)

2. **Oura Token:**
   - Get Personal Access Token from Oura
   - Save to Firestore: `node scripts/setup-oura.js`

3. **Schedule Daily Sync:**
   - Windows: Use Task Scheduler
   - Mac/Linux: Use cron
   - Runs `node scripts/daily-sync.js` at 6 AM

4. **Start MyoAdapt Watcher:**
   - Run: `node scripts/myoadapt-watcher.js`
   - Leave running in background
   - Or set to start on boot

### Usage

**Normal day:**
1. Oura syncs automatically at 6 AM (you do nothing)
2. Google Fit syncs automatically at 6 AM (you do nothing)
3. Export MyoAdapt workout → Download → Auto-imports (you do nothing)
4. Tell me about your health during our conversations (I log it)

**When you want insights:**
- Open Claude Code
- Ask me questions about your data
- Request charts/analysis
- I query Firestore and show results

---

## Example Conversation Flow

**You:** "How am I doing this week?"

**Me:** *queries Firestore for last 7 days*

"Here's your week at a glance:
- Sleep: Average 7.2 hours, score 78/100
- HRV: Trending up (58 → 62 ms)
- Workouts: 4 sessions, volume up 12% from last week
- Weight: Down 1.2 lbs (on track for your cut)
- Readiness: 3 days green, 2 yellow, 2 red
- Note: Your HRV dropped after Tuesday's heavy squats but recovered by Thursday"

**You:** "Chart my bench press progression"

**Me:** *generates chart image showing weight/reps over time*

[Shows chart with trend line and PRs marked]

"Your bench is up 15 lbs over 12 weeks. Nice linear progression! Your estimated 1RM went from 185 to 200. Last PR was 3 days ago: 3x5 @ 165 lbs."

---

## What Gets Removed

We'll clean up the web app components:
- Delete `client/` folder (React app)
- Remove Express web routes from `server/server.js`
- Keep only the data collection services
- No more "login and browse" - just conversation-based queries

---

## File Structure (New)

```
Playground-/
├── scripts/
│   ├── daily-sync.js           # Runs at 6 AM daily
│   ├── myoadapt-watcher.js     # Watches for new CSVs
│   ├── auth-googlefit.js       # One-time Google Fit auth
│   ├── setup-oura.js           # One-time Oura token setup
│   ├── query-data.js           # Helper for me to query your data
│   └── generate-chart.js       # Chart generation utility
├── server/
│   └── utils/
│       ├── ouraSyncService.js  # Kept
│       ├── googleFitService.js # Kept
│       ├── excelParser.js      # Kept
│       └── workoutTransformer.js # Kept
├── logs/
│   └── daily-sync.log          # Sync logs
├── firebase-admin-key.json     # Firebase credentials
└── README.md                   # New usage guide
```

---

## Benefits of This Approach

✅ **Zero maintenance** - Runs automatically
✅ **Conversational** - Just ask me questions naturally
✅ **Flexible analysis** - I can combine data in creative ways
✅ **Always up to date** - Daily sync happens while you sleep
✅ **Simple** - No UI to navigate, no clicking, no logging in
✅ **Powerful** - I can analyze patterns you'd never notice manually

---

## Ready to Build?

I'll now:
1. Create the daily sync script
2. Create the MyoAdapt file watcher
3. Create the Google Fit auth flow
4. Create health notes logging tools
5. Set up the scheduler configuration
6. Clean up unused web app code
7. Document how to use it

This will turn your setup into an automated health data collection + AI analysis system.

Proceed with implementation?
