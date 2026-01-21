# Installing Node.js on Windows

Node.js is required to run your Life Logger app. This guide will walk you through installing it.

## Time Required: 5 minutes

---

## Step 1: Download Node.js

1. **Open this link in your browser:**

   **https://nodejs.org/**

2. You'll see two big green buttons. Click the one that says **"LTS"** (Long Term Support)
   - LTS means it's the most stable version
   - The button might say something like "20.11.0 LTS" or similar

3. The installer file will download (it's about 30MB)
   - Look for it in your Downloads folder
   - File name will be like: `node-v20.11.0-x64.msi`

---

## Step 2: Run the Installer

1. **Double-click** the downloaded file to run it

2. Click **"Next"** on the welcome screen

3. **Accept the license agreement**
   - Check the box "I accept the terms in the License Agreement"
   - Click **"Next"**

4. **Installation location** (default is fine)
   - Keep the default: `C:\Program Files\nodejs\`
   - Click **"Next"**

5. **Custom Setup** screen
   - Don't change anything here
   - Just click **"Next"**

6. **Tools for Native Modules** screen
   - You can leave this unchecked (not needed for this app)
   - Click **"Next"**

7. Click **"Install"**
   - Windows may ask for administrator permission - click **"Yes"**
   - Wait for the installation (takes about 1-2 minutes)

8. Click **"Finish"**

---

## Step 3: Verify Installation

1. **Open Command Prompt:**
   - Press `Windows Key` + `R` on your keyboard
   - Type: `cmd`
   - Press `Enter`

2. **Check Node.js version:**
   - In the black window that opens, type:
     ```
     node --version
     ```
   - Press `Enter`

3. **You should see something like:**
   ```
   v20.11.0
   ```

4. **Check npm version** (npm is installed with Node.js):
   - Type:
     ```
     npm --version
     ```
   - Press `Enter`
   - You should see something like: `10.2.4`

5. **If you see version numbers:** ✅ Success! Node.js is installed!

6. You can close the Command Prompt window now

---

## Troubleshooting

### Problem: "node is not recognized as an internal or external command"

**Solution:**
1. Close Command Prompt completely
2. Open a NEW Command Prompt window
3. Try `node --version` again
4. If it still doesn't work, restart your computer

### Problem: The installer won't run

**Solution:**
- Make sure you downloaded the Windows installer (.msi file)
- Right-click the file and select "Run as administrator"

### Problem: "Access denied" during installation

**Solution:**
- Right-click the installer
- Select "Run as administrator"
- Click "Yes" when Windows asks for permission

---

## What's Next?

Once Node.js is installed:

1. Go back to your Life Logger project folder
2. Double-click `setup.bat` to continue setup

---

## Need Help?

If you're still having trouble:
1. Try restarting your computer after installation
2. Make sure you downloaded from the official site: https://nodejs.org/
3. Try uninstalling and reinstalling Node.js

---

**You're doing great!** Once Node.js is installed, the rest of the setup is automated.
