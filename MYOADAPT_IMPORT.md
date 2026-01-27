# Importing MyoAdapt Workout Data

This guide will help you import your workout data from MyoAdapt into your Life Logger app.

## Quick Start (3 Easy Steps)

1. **Request export from MyoAdapt app**
2. **Download the Excel file from your email**
3. **Upload it to Life Logger → Workouts → Import**

That's it! Your workouts will be automatically processed and added to your log.

---

## Detailed Instructions

### Step 1: Request Export from MyoAdapt

1. Open your MyoAdapt app
2. Go to Settings or Profile
3. Look for "Export Data" or "Download Data"
4. Request an email export
5. MyoAdapt will send you an email with an Excel file attached

### Step 2: Download the Excel File

1. Check your email for the MyoAdapt export
2. Open the email
3. Download the Excel attachment (.xlsx or .xls file)
4. Remember where you saved it (usually in Downloads folder)

### Step 3: Import to Life Logger

1. **Open Life Logger** (double-click `start.bat` or go to http://localhost:3000)

2. **Navigate to Workouts:**
   - Click on "Workout Data" from the dashboard
   - Or go directly to http://localhost:3000/workouts

3. **Click "Import from MyoAdapt"** button at the bottom of the page

4. **Upload your Excel file:**
   - Drag and drop the file onto the upload area
   - OR click "Select File" to browse for it

5. **Click "Import Workouts"**

6. **Wait for processing** (usually takes a few seconds)

7. **Done!** You'll see a success message showing how many workouts were imported

---

## What Gets Imported

When you import a MyoAdapt Excel file, the system automatically:

- **Groups exercises by date** - All exercises from the same day become one workout entry
- **Calculates total duration** - Adds up all set times, rest times, and warmup times
- **Creates summary notes** - Lists muscle groups and exercises performed
- **Sets workout type** - Automatically labeled as "Strength Training"
- **Detects duplicates** - Won't import the same date twice

### Example:

If your Excel has 30 sets from Monday's workout across multiple exercises (Abs, Calves, Hamstrings, etc.), it will create **one workout entry** for Monday with:
- **Duration:** 45 minutes (calculated from all sets)
- **Notes:** "Abs: Ab Roll Out, Calves: Single Leg, Hamstrings: Seated Ha, ..."
- **Date:** Monday's date

---

## Troubleshooting

### Import Failed: "No file uploaded"
**Solution:** Make sure you selected a file before clicking Import

### Import Failed: "Invalid file type"
**Solution:**
- Make sure you're uploading the Excel file from MyoAdapt
- File must be .xlsx or .xls format
- Don't convert to CSV or other formats

### Import Failed: "No workout data found"
**Solution:**
- Check that the Excel file has data in it
- Make sure it's the workout export, not a different MyoAdapt file
- Try requesting a new export from MyoAdapt

### Import Failed: "File too large"
**Solution:**
- Maximum file size is 5MB
- If your export is larger, try exporting a shorter time range
- Contact support if you need help

### Some Workouts Were Skipped
This is normal! If you've already imported workouts for certain dates, the system will skip duplicates to avoid double-logging.

**Example:**
- Import shows "Imported: 5 workouts, Skipped: 2 duplicates"
- This means 5 new workouts were added, and 2 dates were already in your log

---

## Tips & Best Practices

### How Often Should I Import?

Import as often as you like! Common patterns:
- **Weekly:** Request export once a week
- **Monthly:** Export at the end of each month
- **After each workout:** Export after each session (if MyoAdapt supports it)

The duplicate detection ensures you won't double-log workouts.

### What If I Make a Mistake?

If you accidentally import the wrong file:
1. Go to your Workouts page
2. Find the imported workouts (they'll be recent)
3. Click the trash icon to delete them

### Can I Import Multiple Files?

Yes! Import as many times as you want. The system will:
- Process each file independently
- Skip any duplicate dates automatically
- Add new workouts that don't exist yet

### File Size Limits

- **Maximum size:** 5MB per file
- **Typical size:** Most MyoAdapt exports are 50-500KB
- **If too large:** Export shorter date ranges

---

## Data Privacy & Security

- Excel files are **temporarily stored** on the server during processing
- Files are **automatically deleted** after import completes
- Only **you** can see your imported workouts (protected by your user ID)
- Excel data is **never stored permanently** - only the transformed workout data

---

## What If I Don't Use MyoAdapt?

This importer is designed for MyoAdapt's Excel format, but it might work with similar fitness apps if they export data in a compatible format.

**Required columns:**
- Date
- Exercise
- Set time

**Optional columns:**
- Target muscle
- Reps
- Weight
- Rest time
- Warmup time

If your app exports Excel files with these columns, try importing! It might work.

---

## Need Help?

If you're having trouble importing:

1. Check this troubleshooting guide first
2. Make sure your Excel file is from MyoAdapt
3. Try with a small export (just a few days) to test
4. Open a GitHub issue if problems persist

---

## Future Enhancements

Coming soon:
- Automatic email import (no manual download needed)
- Support for more fitness apps
- Custom column mapping
- Import history and logs

---

**Last Updated:** January 2026
