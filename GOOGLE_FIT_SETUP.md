# Google Fit Integration Setup Guide

This guide will walk you through setting up Google Fit API access for your Life Logger app.

**Time required:** ~15 minutes

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Click the project dropdown at the top (says "Select a project")

3. Click "NEW PROJECT"

4. **Project name:** `Life Logger`

5. Click "CREATE"

6. Wait for project creation (takes ~30 seconds)

7. **IMPORTANT:** Select your new "Life Logger" project from the dropdown

---

## Step 2: Enable Google Fitness API

1. In the left sidebar, click **"APIs & Services"** → **"Library"**

2. In the search bar, type: `Fitness API`

3. Click on **"Fitness API"**

4. Click the blue **"ENABLE"** button

5. Wait for it to enable (~10 seconds)

---

## Step 3: Configure OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"** → **"OAuth consent screen"**

2. **User Type:** Select **"External"**

3. Click **"CREATE"**

### OAuth Consent Screen - Page 1: App Information

- **App name:** `Life Logger`
- **User support email:** Select your email from dropdown
- **App logo:** (Optional - skip for now)
- **App domain:** (Leave blank for now)
- **Authorized domains:** (Leave blank for now)
- **Developer contact information:** Enter your email

Click **"SAVE AND CONTINUE"**

### OAuth Consent Screen - Page 2: Scopes

1. Click **"ADD OR REMOVE SCOPES"**

2. In the search/filter box, type: `fitness`

3. Check these 4 scopes:

   ✅ `.../auth/fitness.body.read` - See info about your body measurements

   ✅ `.../auth/fitness.activity.read` - See your activity data

   ✅ `.../auth/fitness.heart_rate.read` - See your heart rate data

   ✅ `.../auth/fitness.sleep.read` - See your sleep data

4. Click **"UPDATE"**

5. Verify you see all 4 scopes listed

6. Click **"SAVE AND CONTINUE"**

### OAuth Consent Screen - Page 3: Test Users

1. Click **"ADD USERS"**

2. Enter your Google account email (the one you use for Google Fit)

3. Click **"ADD"**

4. Click **"SAVE AND CONTINUE"**

### OAuth Consent Screen - Page 4: Summary

1. Review the summary

2. Click **"BACK TO DASHBOARD"**

---

## Step 4: Create OAuth 2.0 Credentials

1. In the left sidebar, click **"APIs & Services"** → **"Credentials"**

2. Click **"+ CREATE CREDENTIALS"** at the top

3. Select **"OAuth client ID"**

4. **Application type:** Select **"Web application"**

5. **Name:** `Life Logger Web Client`

6. **Authorized JavaScript origins:**
   - Click **"+ ADD URI"**
   - Enter: `http://localhost:3000`

7. **Authorized redirect URIs:**
   - Click **"+ ADD URI"**
   - Enter: `http://localhost:3000/googlefit/callback`

8. Click **"CREATE"**

9. A popup will appear with your credentials:

   **CLIENT ID:** (something like `123456789-abc123.apps.googleusercontent.com`)

   **CLIENT SECRET:** (something like `GOCSPX-abc123def456`)

10. **COPY BOTH OF THESE** - you'll need them in the next step

---

## Step 5: Configure Life Logger App

### Option A: Environment Variables (Recommended for Production)

1. Create a file: `server/.env` (if it doesn't exist)

2. Add these lines:
   ```
   GOOGLE_FIT_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
   GOOGLE_FIT_CLIENT_SECRET=your-client-secret-here
   GOOGLE_FIT_REDIRECT_URI=http://localhost:3000/googlefit/callback
   ```

3. Replace `your-client-id-here` with your actual Client ID

4. Replace `your-client-secret-here` with your actual Client Secret

5. Save the file

### Option B: Direct Configuration (For Testing)

If environment variables don't work, you can paste them directly in the code:

1. Open: `server/utils/googleFitService.js`

2. Find the OAuth2 client initialization

3. Replace the placeholder values

---

## Step 6: Restart the App

1. Stop your server (Ctrl+C in the command prompt)

2. Restart: `start.bat`

3. Open your browser: `http://localhost:3000`

4. Navigate to: **Google Fit** from the dashboard

5. Click **"Connect Google Fit"**

6. You should see the Google OAuth consent screen

7. Click **"Allow"**

8. You'll be redirected back to your app with a "Connected" status

---

## Step 7: Sync Your Weight Data

1. Click **"Sync Weight History"**

2. Select date range (e.g., "Last 2 years")

3. Click **"Sync"**

4. Wait for sync to complete

5. You should see a chart with all your weight data!

---

## Troubleshooting

### Error: "Access blocked: Life Logger has not completed the Google verification process"

**Solution:**
- Go back to OAuth consent screen
- Make sure you added YOUR email as a test user
- You can only use the app with test user accounts until you publish the app

### Error: "redirect_uri_mismatch"

**Solution:**
- Go to Google Cloud Console → Credentials
- Click on your OAuth client ID
- Check "Authorized redirect URIs"
- Make sure it exactly matches: `http://localhost:3000/googlefit/callback`
- No trailing slash, must be exact

### Error: "Invalid client"

**Solution:**
- Double-check your Client ID and Client Secret
- Make sure there are no extra spaces when you copy/pasted
- Verify the values in your `.env` file or config

### No weight data showing up

**Solution:**
- Make sure you've been logging weight in Google Fit app
- Check the date range you selected
- Try syncing again
- Check browser console for errors (F12 → Console tab)

---

## Privacy & Security Notes

- **Your data stays with you:** All weight data is stored in YOUR Firebase database, not on Google's servers
- **Tokens are encrypted:** OAuth tokens are encrypted before storage
- **Limited access:** The app only requests read-only access to fitness data
- **Revoke anytime:** You can disconnect Google Fit anytime from the app or from [Google Account Settings](https://myaccount.google.com/permissions)

---

## Need Help?

If you get stuck:
1. Check the Troubleshooting section above
2. Verify each step was completed exactly as written
3. Check your browser console for error messages (F12)
4. Open a GitHub issue with screenshots of any errors

---

## What's Next?

Once Google Fit is connected:
- Your weight data syncs automatically
- You can manually add weight entries too
- View weight trends over time
- Correlate weight with workout performance
- Track progress during cuts/bulks
