import { parse, isValid } from 'date-fns';

/**
 * Converts time string to seconds
 * @param {string} timeStr - Time in format "H:MM:SS" or "M:SS"
 * @returns {number} Time in seconds
 */
function parseTimeToSeconds(timeStr) {
  if (!timeStr || timeStr === 'N/A') return 0;

  const parts = timeStr.split(':').map(p => parseInt(p, 10));

  if (parts.length === 3) {
    // H:MM:SS format
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  } else if (parts.length === 2) {
    // M:SS format
    return parts[0] * 60 + parts[1];
  }

  return 0;
}

/**
 * Parses a date string from MyoAdapt format
 * @param {string} dateStr - Date string (e.g., "1/26/2026")
 * @returns {Date} JavaScript Date object
 */
function parseDateString(dateStr) {
  // Try multiple date formats
  const formats = ['M/d/yyyy', 'MM/dd/yyyy', 'M-d-yyyy', 'MM-dd-yyyy'];

  for (const format of formats) {
    const date = parse(dateStr, format, new Date());
    if (isValid(date)) {
      return date;
    }
  }

  // If all formats fail, try built-in parser
  const fallbackDate = new Date(dateStr);
  if (isValid(fallbackDate)) {
    return fallbackDate;
  }

  throw new Error(`Invalid date format: ${dateStr}`);
}

/**
 * Groups workout rows by date
 * @param {Array} rows - Array of workout rows from Excel
 * @returns {Object} Object with dates as keys, arrays of rows as values
 */
function groupByDate(rows) {
  const grouped = {};

  for (const row of rows) {
    const dateStr = row.date;
    if (!dateStr) continue;

    if (!grouped[dateStr]) {
      grouped[dateStr] = [];
    }
    grouped[dateStr].push(row);
  }

  return grouped;
}

/**
 * Generates summary notes for a workout
 * @param {Array} rows - Workout rows for a single day
 * @returns {string} Summary text
 */
function generateWorkoutNotes(rows) {
  // Group by muscle/exercise
  const exerciseGroups = {};

  for (const row of rows) {
    const key = row.targetMuscle || 'General';
    if (!exerciseGroups[key]) {
      exerciseGroups[key] = new Set();
    }
    if (row.exercise) {
      exerciseGroups[key].add(row.exercise);
    }
  }

  // Build summary
  const parts = [];

  for (const [muscle, exercises] of Object.entries(exerciseGroups)) {
    const exerciseList = Array.from(exercises).join(', ');
    parts.push(`${muscle}: ${exerciseList}`);
  }

  const totalSets = rows.length;
  parts.push(`\nTotal: ${totalSets} sets`);

  return parts.join('\n');
}

/**
 * Transforms MyoAdapt Excel rows into workout objects for Firestore
 * @param {Array} rows - Parsed Excel rows
 * @param {string} userId - Firebase user ID
 * @returns {Array} Array of workout objects ready for Firestore
 */
export function transformToWorkouts(rows, userId) {
  if (!rows || rows.length === 0) {
    return [];
  }

  if (!userId) {
    throw new Error('userId is required');
  }

  // Group rows by date
  const groupedByDate = groupByDate(rows);

  // Transform each date group into a workout object
  const workouts = [];

  for (const [dateStr, dateRows] of Object.entries(groupedByDate)) {
    try {
      // Parse the date
      const workoutDate = parseDateString(dateStr);

      // Calculate total duration (sum of set times + rest times)
      let totalSeconds = 0;

      for (const row of dateRows) {
        totalSeconds += parseTimeToSeconds(row.setTime);
        totalSeconds += parseTimeToSeconds(row.restTime);
        totalSeconds += parseTimeToSeconds(row.warmupTime);
      }

      const durationMinutes = Math.round(totalSeconds / 60);

      // Generate notes
      const notes = generateWorkoutNotes(dateRows);

      // Create workout object
      const workout = {
        userId,
        workoutType: 'Strength Training',
        duration: durationMinutes,
        calories: null,
        distance: null,
        notes,
        timestamp: workoutDate
      };

      workouts.push(workout);

    } catch (error) {
      console.error(`Error processing workout for date ${dateStr}:`, error);
      // Skip this date and continue with others
    }
  }

  // Sort by date (oldest first)
  workouts.sort((a, b) => a.timestamp - b.timestamp);

  return workouts;
}
