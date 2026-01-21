# Getting Started with Life Logger

Welcome! This guide will help you set up and run your Life Logger app. Don't worry if you've never done this before - we'll walk through every step together.

## Total Time: ~15 minutes

---

## What You'll Need

- [ ] Windows 10 or 11
- [ ] Internet connection
- [ ] The Life Logger project folder (you should already have this!)

---

## Overview: What We'll Do

1. **Install Node.js** (5 min) - Software needed to run the app
2. **Run automated setup** (2 min) - Installs everything automatically
3. **Enable Firebase services** (5 min) - Click a few buttons in your browser
4. **Connect to Firebase** (1 min) - Link your project
5. **Deploy security rules** (30 sec) - Automated
6. **Start the app** (30 sec) - Launch and test!

Let's get started!

---

## Step 1: Install Node.js

Node.js is the software that runs your app. You only need to do this once.

### Do you already have Node.js?

**To check:**
1. Press `Windows Key` + `R`
2. Type `cmd` and press Enter
3. Type `node --version` and press Enter

**If you see a version number** (like `v20.11.0`):
- ✅ Great! Skip to Step 2

**If you see an error** (like "node is not recognized"):
- You need to install Node.js

### Installing Node.js:

**Option 1: Follow the detailed guide**
- Open `INSTALL_NODEJS.md` (in this same folder)
- Follow the step-by-step instructions

**Option 2: Quick install**
1. Go to: **https://nodejs.org/**
2. Click the big green **"LTS"** button
3. Run the downloaded installer
4. Click "Next" through all the screens
5. Restart your computer after installation

---

## Step 2: Run Automated Setup

Now we'll install all the app's dependencies automatically!

### Steps:

1. **Open your Life Logger project folder** (the folder containing this file)

2. **Find the file called `setup.bat`**
   - It looks like a white icon with a gear/cog symbol

3. **Double-click `setup.bat`**
   - A black window will open (Command Prompt)
   - You'll see text scrolling as it installs things

4. **Wait for it to finish** (takes 1-3 minutes)
   - You'll see "Installing Firebase CLI..."
   - Then "Installing project dependencies..."
   - Lots of text will scroll by - this is normal!

5. **Look for "[SUCCESS] Setup complete!"**
   - When you see this, the setup worked!

6. **Press any key** to close the window

### What if it fails?

**Error: "Node.js is not installed!"**
- Go back to Step 1 and install Node.js
- Then try again

**Error: "Failed to install..."**
- Make sure you have internet connection
- Try running `setup.bat` again
- The problem might be temporary

---

## Step 3: Enable Firebase Services

Now we need to enable 3 services in the Firebase Console (your database in the cloud).

### Steps:

1. **Open the file `FIREBASE_CONSOLE_SETUP.md`**
   - You can open it in your browser or any text editor

2. **Follow all three parts:**
   - Part 1: Enable Authentication (2 min)
   - Part 2: Create Firestore Database (2 min)
   - Part 3: Enable Cloud Storage (1 min)

3. **Don't skip this step!** The app won't work without it

4. **Mark each part done:**
   - [ ] Authentication enabled
   - [ ] Firestore Database created
   - [ ] Cloud Storage enabled

---

## Step 4: Connect to Firebase

Now we'll link your local project to your Firebase project in the cloud.

### Steps:

1. **Find the file called `firebase-init.bat`**

2. **Double-click it**
   - A black window will open

3. **Follow the prompts:**

   **a) Press any key to start**

   **b) Firebase Login:**
   - A browser window will open
   - Sign in with your Google account (the same one you used for Firebase)
   - Click "Allow" to give permissions
   - You'll see "Success! You're logged in."
   - Close the browser tab and go back to the black window

   **c) Select project:**
   - Use arrow keys to navigate
   - Select: **"Use an existing project"**
   - Press Enter
   - Select: **"lifelogger-e6ecd"**
   - Press Enter

   **d) Initialize Firestore:**
   - It will ask about the rules file
   - Just press **Enter** (accept default)
   - It will ask about the indexes file
   - Press **Enter** again
   - If it asks to overwrite: Type **N** and press Enter

   **e) Initialize Storage:**
   - It will ask about the rules file
   - Press **Enter** (accept default)
   - If it asks to overwrite: Type **N** and press Enter

4. **Look for "[SUCCESS] Firebase initialized!"**

5. **Press any key** to close

---

## Step 5: Deploy Security Rules

This step makes sure only you can access your own data.

### Steps:

1. **Find the file called `deploy-rules.bat`**

2. **Double-click it**

3. **Wait for it to finish** (takes about 10 seconds)
   - You'll see "Deploying Firestore rules..."
   - Then "Deploying Storage rules..."

4. **Look for "[SUCCESS] All rules deployed!"**

5. **Press any key** to close

---

## Step 6: Start Your App!

This is it - time to launch your Life Logger app!

### Steps:

1. **Find the file called `start.bat`**

2. **Double-click it**
   - A black window will open
   - You'll see "Starting servers..."
   - Text will scroll as the app starts

3. **Wait until you see:**
   ```
   VITE v5.x.x ready in xxx ms
   Local: http://localhost:3000
   ```

4. **Open your web browser**
   - Type in the address bar: `http://localhost:3000`
   - Press Enter

5. **You should see the Life Logger login page!**

6. **Create an account:**
   - Click "Sign Up"
   - Enter an email and password (min 6 characters)
   - Click "Sign Up"

7. **Test the app:**
   - Try logging a mood
   - Try creating a note
   - Try uploading a photo
   - Everything should work!

### Important:

**Keep the black window (Command Prompt) open while using the app!**
- If you close it, the app will stop
- To stop the app: Press `Ctrl+C` in the black window

---

## You're Done! 🎉

Your Life Logger app is now running!

### What's Next?

- **To use the app:** Just open http://localhost:3000 in your browser
- **To stop the app:** Press `Ctrl+C` in the Command Prompt window
- **To start again:** Just double-click `start.bat`

### Optional: Connect Your Oura Ring

If you have an Oura Ring:
1. Log into your app
2. Click "Oura Integration"
3. Follow the instructions to get your API token

---

## Troubleshooting

### Problem: "Cannot GET /" error in browser

**Solution:**
- Make sure the Command Prompt window is still open
- Make sure you see "ready in xxx ms" in the window
- Try refreshing the browser

### Problem: Can't create an account

**Solution:**
- Make sure you completed Step 3 (Firebase Console Setup)
- Check that Authentication is enabled in Firebase Console
- Try a different email address

### Problem: Photos won't upload

**Solution:**
- Make sure you completed Part 3 of Firebase Console Setup (Cloud Storage)
- Make sure you deployed the security rules (Step 5)

### Problem: App is slow to start

**Solution:**
- This is normal the first time! It can take 30-60 seconds
- Subsequent starts will be faster

---

## Daily Usage

After the initial setup, using your app is easy:

**To start the app:**
1. Double-click `start.bat`
2. Open http://localhost:3000

**To stop the app:**
- Press `Ctrl+C` in the Command Prompt window

That's it!

---

## Need Help?

If something isn't working:
1. Make sure you followed all steps in order
2. Check that Node.js is installed (`node --version` in Command Prompt)
3. Check that Firebase services are enabled (Firebase Console)
4. Try restarting your computer and running `start.bat` again

---

**Congratulations!** You've successfully set up your first web application! 🚀
