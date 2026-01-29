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

/**
 * Calculates estimated 1RM using Brzycki formula
 * @param {number} weight - Weight lifted
 * @param {number} reps - Reps performed
 * @returns {number} Estimated 1RM
 */
function calculateEstimated1RM(weight, reps) {
  if (!weight || !reps || reps <= 0) return 0;
  if (reps === 1) return weight;

  // Brzycki formula: weight × (36 / (37 – reps))
  return Math.round(weight * (36 / (37 - reps)));
}

/**
 * Groups workout rows by date and exercise
 * @param {Array} rows - Array of workout rows
 * @returns {Object} Nested object { date: { exercise: [rows] } }
 */
function groupByDateAndExercise(rows) {
  const grouped = {};

  for (const row of rows) {
    const dateStr = row.date;
    const exercise = row.exercise;

    if (!dateStr || !exercise) continue;

    if (!grouped[dateStr]) {
      grouped[dateStr] = {};
    }

    if (!grouped[dateStr][exercise]) {
      grouped[dateStr][exercise] = [];
    }

    grouped[dateStr][exercise].push(row);
  }

  return grouped;
}

/**
 * Transforms MyoAdapt rows into individual exercise records for detailed tracking
 * @param {Array} rows - Parsed Excel/CSV rows
 * @param {string} userId - Firebase user ID
 * @returns {Array} Array of exercise objects ready for Firestore
 */
export function transformToExercises(rows, userId) {
  if (!rows || rows.length === 0) {
    return [];
  }

  if (!userId) {
    throw new Error('userId is required');
  }

  // Group rows by date and exercise
  const groupedByDateAndExercise = groupByDateAndExercise(rows);

  // Transform each date+exercise group into an exercise object
  const exercises = [];

  for (const [dateStr, exerciseGroups] of Object.entries(groupedByDateAndExercise)) {
    for (const [exerciseName, exerciseRows] of Object.entries(exerciseGroups)) {
      try {
        // Parse the date
        const exerciseDate = parseDateString(dateStr);

        // Build sets array
        const sets = [];
        let totalVolume = 0;
        let totalDuration = 0;
        let heaviestSet = { weight: 0, reps: 0 };

        for (let i = 0; i < exerciseRows.length; i++) {
          const row = exerciseRows[i];

          const weight = parseFloat(row.weight) || 0;
          const reps = parseInt(row.reps, 10) || 0;
          const rir = parseInt(row.rir, 10) || null;
          const setTime = parseTimeToSeconds(row.setTime);
          const restTime = parseTimeToSeconds(row.restTime);

          // Track heaviest set for 1RM calculation
          if (weight > heaviestSet.weight || (weight === heaviestSet.weight && reps > heaviestSet.reps)) {
            heaviestSet = { weight, reps };
          }

          sets.push({
            setNumber: i + 1,
            reps,
            weight,
            rir,
            setTime,
            restTime
          });

          // Calculate volume (weight × reps)
          totalVolume += weight * reps;

          // Calculate total duration
          totalDuration += setTime + restTime;
        }

        // Calculate estimated 1RM from heaviest set
        const estimated1RM = calculateEstimated1RM(heaviestSet.weight, heaviestSet.reps);

        // Get target muscle (should be same for all rows of this exercise)
        const targetMuscle = exerciseRows[0].targetMuscle || 'General';

        // Create exercise object
        const exercise = {
          userId,
          date: dateStr,
          exercise: exerciseName,
          targetMuscle,
          sets,
          totalVolume,
          totalDuration,
          estimated1RM,
          timestamp: exerciseDate
        };

        exercises.push(exercise);

      } catch (error) {
        console.error(`Error processing exercise ${exerciseName} for date ${dateStr}:`, error);
        // Skip this exercise and continue with others
      }
    }
  }

  // Sort by date (oldest first), then by exercise name
  exercises.sort((a, b) => {
    const dateDiff = a.timestamp - b.timestamp;
    if (dateDiff !== 0) return dateDiff;
    return a.exercise.localeCompare(b.exercise);
  });

  return exercises;
}
