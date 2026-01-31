#!/usr/bin/env node

import { watch } from 'fs';
import { readFileSync, rename, existsSync, mkdirSync } from 'fs';
import { join, basename } from 'path';
import { getFirestore } from './firebase-admin.js';
import { parseMyoAdaptFile } from '../server/utils/excelParser.js';
import { transformToWorkouts, transformToExercises } from '../server/utils/workoutTransformer.js';

// Configuration
const WATCH_FOLDER = process.env.MYOADAPT_WATCH_FOLDER || 'C:\\Users\\andre\\Downloads';
const PROCESSED_FOLDER = join(WATCH_FOLDER, 'MyoAdapt_Processed');
const USER_ID = process.env.USER_ID || 'YOUR_USER_ID_HERE';

// Ensure processed folder exists
if (!existsSync(PROCESSED_FOLDER)) {
  mkdirSync(PROCESSED_FOLDER, { recursive: true });
}

console.log(`👀 Watching for MyoAdapt files in: ${WATCH_FOLDER}`);
console.log(`📁 Processed files will be moved to: ${PROCESSED_FOLDER}`);
console.log('');

/**
 * Check if file is a CSV file (case-insensitive)
 */
function isCSVFile(filename) {
  return filename.toLowerCase().endsWith('.csv');
}

/**
 * Process a MyoAdapt CSV file
 */
async function processFile(filePath) {
  const filename = basename(filePath);

  console.log(`📥 New file detected: ${filename}`);

  try {
    // Wait a moment to ensure file is fully written
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Parse the CSV file
    console.log('📊 Parsing CSV...');
    const rows = parseMyoAdaptFile(filePath);

    if (!rows || rows.length === 0) {
      console.log('⚠️  No data found in file');
      return;
    }

    console.log(`✅ Parsed ${rows.length} rows`);

    // Transform into workouts and exercises
    const workouts = transformToWorkouts(rows, USER_ID);
    const exercises = transformToExercises(rows, USER_ID);

    console.log(`📝 Transformed into ${workouts.length} workout(s) and ${exercises.length} exercise(s)`);

    // Save to Firestore
    const db = getFirestore();

    // Save workouts
    for (const workout of workouts) {
      // Check if workout for this date already exists
      const dateStr = workout.timestamp.toISOString().split('T')[0];
      const existing = await db.collection('workouts')
        .where('userId', '==', USER_ID)
        .where('timestamp', '>=', new Date(dateStr))
        .where('timestamp', '<', new Date(new Date(dateStr).getTime() + 86400000))
        .get();

      if (existing.empty) {
        await db.collection('workouts').add(workout);
        console.log(`✅ Saved workout for ${dateStr}`);
      } else {
        console.log(`⏭️  Skipped duplicate workout for ${dateStr}`);
      }
    }

    // Save exercises
    for (const exercise of exercises) {
      // Check if exercise already exists
      const dateStr = exercise.date;
      const existing = await db.collection('exercises')
        .where('userId', '==', USER_ID)
        .where('date', '==', dateStr)
        .where('exercise', '==', exercise.exercise)
        .get();

      if (existing.empty) {
        await db.collection('exercises').add(exercise);
      }
    }

    console.log(`✅ Saved ${exercises.length} exercise record(s)`);

    // Move file to processed folder
    const processedPath = join(PROCESSED_FOLDER, filename);
    rename(filePath, processedPath, (err) => {
      if (err) {
        console.error(`❌ Failed to move file: ${err.message}`);
      } else {
        console.log(`📦 Moved to: ${processedPath}`);
      }
    });

    console.log('');
  } catch (error) {
    console.error(`❌ Error processing file: ${error.message}`);
    console.log('');
  }
}

/**
 * Watch folder for new files
 */
function startWatching() {
  if (USER_ID === 'YOUR_USER_ID_HERE') {
    console.error('❌ Error: USER_ID not set. Please set USER_ID environment variable.');
    process.exit(1);
  }

  const watcher = watch(WATCH_FOLDER, { persistent: true }, (eventType, filename) => {
    if (eventType === 'rename' && filename && isCSVFile(filename)) {
      const filePath = join(WATCH_FOLDER, filename);

      // Check if file exists (rename event triggers for both create and delete)
      if (existsSync(filePath)) {
        processFile(filePath);
      }
    }
  });

  console.log('✅ File watcher started');
  console.log('💡 Drop MyoAdapt CSV files into Downloads folder to auto-import');
  console.log('Press Ctrl+C to stop\n');

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n👋 Stopping file watcher...');
    watcher.close();
    process.exit(0);
  });
}

// Start watching
startWatching();
