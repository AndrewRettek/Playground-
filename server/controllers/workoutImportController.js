import fs from 'fs';
import { parseMyoAdaptExcel, isValidExcelFile } from '../utils/excelParser.js';
import { transformToWorkouts, transformToExercises } from '../utils/workoutTransformer.js';

/**
 * Handles MyoAdapt Excel file import
 * Parses the file, transforms data, and returns workout objects
 */
export async function importWorkoutsFromExcel(req, res) {
  let filePath = null;

  try {
    // Check if file was uploaded
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: 'No file uploaded'
      });
    }

    // Get userId from request body (sent by client)
    const { userId } = req.body;

    if (!userId) {
      return res.status(400).json({
        success: false,
        error: 'userId is required'
      });
    }

    filePath = req.file.path;
    const filename = req.file.originalname;

    // Validate file extension
    if (!isValidExcelFile(filename)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid file type. Please upload an Excel file (.xlsx or .xls)'
      });
    }

    // Validate file size (5MB max)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (req.file.size > maxSize) {
      return res.status(400).json({
        success: false,
        error: 'File too large. Maximum size is 5MB'
      });
    }

    // Parse the Excel file
    console.log('Parsing Excel file:', filename);
    const rows = parseMyoAdaptExcel(filePath);

    if (!rows || rows.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'No workout data found in Excel file'
      });
    }

    console.log(`Parsed ${rows.length} rows from Excel`);

    // Transform rows into workout objects (daily summaries)
    const workouts = transformToWorkouts(rows, userId);

    // Transform rows into individual exercise records (detailed tracking)
    const exercises = transformToExercises(rows, userId);

    if (workouts.length === 0 && exercises.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'No valid workouts could be extracted from the file'
      });
    }

    console.log(`Transformed into ${workouts.length} workout(s) and ${exercises.length} exercise(s)`);

    // Return both workouts and exercises to the client
    // The client will handle writing to Firestore
    res.json({
      success: true,
      message: `Successfully processed ${workouts.length} workout(s) and ${exercises.length} exercise(s)`,
      workouts: workouts,
      exercises: exercises,
      importedCount: workouts.length
    });

  } catch (error) {
    console.error('Import error:', error);

    res.status(500).json({
      success: false,
      error: 'Failed to import workouts',
      details: error.message
    });

  } finally {
    // Clean up: delete the uploaded file
    if (filePath) {
      try {
        fs.unlinkSync(filePath);
        console.log('Cleaned up temp file:', filePath);
      } catch (cleanupError) {
        console.error('Error cleaning up file:', cleanupError);
      }
    }
  }
}
