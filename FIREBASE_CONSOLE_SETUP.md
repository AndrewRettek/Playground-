# Firebase Console Setup

This guide will help you enable the required Firebase services. You'll just need to click a few buttons in your web browser.

**Time Required: 5 minutes**

---

## Part 1: Enable Authentication (Email/Password)

This allows users to create accounts and log in to your app.

### Steps:

1. **Open this link:** (it will open directly to the Authentication page)

   **https://console.firebase.google.com/project/lifelogger-e6ecd/authentication**

2. You should see a page that says **"Authentication"** at the top

3. Look for a button that says **"Get started"** - click it
   - If you don't see "Get started", it might already be enabled - skip to step 7

4. You'll see a list of sign-in methods (Google, Facebook, Email/Password, etc.)

5. **Find "Email/Password"** in the list (it's usually near the top)
   - Click on the row that says "Email/Password"

6. A panel will slide in from the right side:
   - Toggle the **first switch** to **"Enabled"** (it will turn blue)
   - **Do NOT** enable "Email link (passwordless sign-in)"
   - Click **"Save"** at the bottom

7. **Verify it worked:**
   - You should see "Email/Password" in the list with status "Enabled"

✅ **Done!** Authentication is now enabled.

---

## Part 2: Create Firestore Database

This is where your app stores data (moods, sleep logs, notes, etc.).

### Steps:

1. **Open this link:**

   **https://console.firebase.google.com/project/lifelogger-e6ecd/firestore**

2. You should see a page that says **"Cloud Firestore"** at the top

3. Click the button that says **"Create database"**

4. **Choose mode:**
   - Select **"Start in production mode"**
   - Click **"Next"**
   - (Don't worry, we'll add security rules automatically later!)

5. **Choose location:**
   - Select a location closest to you:
     - `us-central` (United States - Iowa)
     - `us-east1` (United States - South Carolina)
     - `europe-west1` (Belgium)
     - Or any other region you prefer
   - Click **"Enable"**

6. **Wait for it to finish** (takes about 30 seconds)
   - You'll see a loading spinner
   - When it's done, you'll see a page that says "Start collection"

7. **Verify it worked:**
   - You should see "Cloud Firestore" with tabs like "Data", "Rules", "Indexes"

✅ **Done!** Firestore Database is now created.

---

## Part 3: Enable Cloud Storage

This is where your app stores photos.

### Steps:

1. **Open this link:**

   **https://console.firebase.google.com/project/lifelogger-e6ecd/storage**

2. You should see a page that says **"Storage"** at the top

3. Click the button that says **"Get started"**

4. **Security rules dialog:**
   - You'll see a popup about security rules
   - Keep the default selection (production mode)
   - Click **"Next"**

5. **Choose location:**
   - It should automatically suggest the same location you chose for Firestore
   - Click **"Done"**

6. **Wait for it to finish** (takes about 10 seconds)
   - You'll see a loading spinner
   - When it's done, you'll see a page showing "Files" and folders

7. **Verify it worked:**
   - You should see a "Files" tab with an empty file browser

✅ **Done!** Cloud Storage is now enabled.

---

## ✅ All Done!

Great job! You've successfully enabled all three Firebase services:
- ✅ Authentication (Email/Password)
- ✅ Firestore Database
- ✅ Cloud Storage

### What's Next?

Go back to your Life Logger project folder and:
1. **Double-click `firebase-init.bat`** to connect your local project to Firebase
2. Follow the prompts in the command window

---

## Troubleshooting

### Problem: Links don't open the Firebase Console

**Solution:**
1. Make sure you're logged into Google with the account you used to create the Firebase project
2. Manually go to: https://console.firebase.google.com/
3. Click on the "lifelogger-e6ecd" project
4. Then navigate to each service using the left sidebar

### Problem: "Get started" button is greyed out

**Solution:**
- The service might already be enabled!
- Check if it says "Enabled" or shows existing data

### Problem: Can't find the project "lifelogger-e6ecd"

**Solution:**
1. Go to: https://console.firebase.google.com/
2. Look at the list of projects
3. Make sure you see "lifelogger-e6ecd"
4. If not, you may have created it with a different Google account

---

**You're almost there!** The hard part is done - now just run the batch files to finish setup.
