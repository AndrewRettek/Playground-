#!/usr/bin/env node

import { getFirestore } from './firebase-admin.js';
import { syncOuraDataRange } from '../server/utils/ouraSyncService.js';
import { fetchWeightData, fetchActivityData, refreshAccessToken } from '../server/utils/googleFitService.js';
import { format, subDays } from 'date-fns';
import { appendFileSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const logFile = join(__dirname, '..', 'logs', 'daily-sync.log');

// Your user ID from Firebase (set this after first setup)
const USER_ID = process.env.USER_ID || 'YOUR_USER_ID_HERE';

/**
 * Logs message to both console and log file
 */
function log(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;
  console.log(message);
  appendFileSync(logFile, logMessage);
}

/**
 * Get Oura token from Firestore
 */
async function getOuraToken(db) {
  const doc = await db.collection('userTokens').doc(`${USER_ID}_oura`).get();
  if (!doc.exists) {
    throw new Error('Oura token not found. Run setup-oura.js first.');
  }
  return doc.data().accessToken;
}

/**
 * Get Google Fit tokens from Firestore
 */
async function getGoogleFitTokens(db) {
  const doc = await db.collection('userTokens').doc(`${USER_ID}_googlefit`).get();
  if (!doc.exists) {
    throw new Error('Google Fit tokens not found. Run auth-googlefit.js first.');
  }
  return doc.data();
}

/**
 * Update Google Fit tokens in Firestore
 */
async function updateGoogleFitTokens(db, tokens) {
  await db.collection('userTokens').doc(`${USER_ID}_googlefit`).update({
    accessToken: tokens.access_token,
    expiresAt: new Date(tokens.expiry_date)
  });
}

/**
 * Sync Oura Ring data for yesterday
 */
async function syncOura(db) {
  try {
    log('📊 Syncing Oura Ring data...');

    const token = await getOuraToken(db);
    const yesterday = format(subDays(new Date(), 1), 'yyyy-MM-dd');

    // Sync yesterday's data
    const ouraData = await syncOuraDataRange(token, yesterday, yesterday);

    if (ouraData && ouraData.length > 0) {
      const data = ouraData[0];

      // Save to Firestore
      await db.collection('ouraHistory').doc(`${USER_ID}_${yesterday}`).set({
        userId: USER_ID,
        date: yesterday,
        sleep: data.sleep,
        activity: data.activity,
        readiness: data.readiness,
        syncedAt: new Date()
      });

      log(`✅ Oura data synced for ${yesterday}`);
      log(`   Sleep score: ${data.sleep?.score || 'N/A'}`);
      log(`   Readiness: ${data.readiness?.score || 'N/A'}`);
      log(`   Activity score: ${data.activity?.score || 'N/A'}`);
    } else {
      log(`⚠️  No Oura data available for ${yesterday}`);
    }
  } catch (error) {
    log(`❌ Oura sync failed: ${error.message}`);
  }
}

/**
 * Sync Google Fit data for yesterday
 */
async function syncGoogleFit(db) {
  try {
    log('📊 Syncing Google Fit data...');

    let tokens = await getGoogleFitTokens(db);

    // Check if token is expired and refresh if needed
    if (tokens.expiresAt && new Date(tokens.expiresAt.toDate()) < new Date()) {
      log('🔄 Refreshing Google Fit access token...');
      const newTokens = await refreshAccessToken(tokens.refreshToken);
      await updateGoogleFitTokens(db, newTokens);
      tokens.accessToken = newTokens.access_token;
    }

    const yesterday = format(subDays(new Date(), 1), 'yyyy-MM-dd');

    // Fetch weight data
    const weightData = await fetchWeightData(tokens.accessToken, yesterday, yesterday);
    if (weightData && weightData.length > 0) {
      for (const entry of weightData) {
        await db.collection('bodyMetrics').add({
          userId: USER_ID,
          date: entry.date,
          weight: entry.weight,
          source: 'googlefit',
          timestamp: new Date(entry.timestamp)
        });
      }
      log(`✅ Synced ${weightData.length} weight entry(s) for ${yesterday}`);
    }

    // Fetch activity data (steps, calories)
    const activityData = await fetchActivityData(tokens.accessToken, yesterday, yesterday);
    if (activityData && activityData.length > 0) {
      for (const entry of activityData) {
        await db.collection('dailyActivity').add({
          userId: USER_ID,
          date: entry.date,
          steps: entry.steps,
          totalCalories: entry.totalCalories,
          activeMinutes: entry.activeMinutes,
          source: 'googlefit',
          timestamp: new Date(entry.timestamp)
        });
      }
      log(`✅ Synced activity data for ${yesterday}`);
      log(`   Steps: ${activityData[0].steps || 0}`);
      log(`   Calories: ${activityData[0].totalCalories || 0}`);
    }

    if (!weightData.length && !activityData.length) {
      log(`⚠️  No Google Fit data available for ${yesterday}`);
    }
  } catch (error) {
    log(`❌ Google Fit sync failed: ${error.message}`);
  }
}

/**
 * Main sync function
 */
async function main() {
  log('='.repeat(60));
  log('🔄 Starting daily health data sync');
  log('='.repeat(60));

  if (USER_ID === 'YOUR_USER_ID_HERE') {
    log('❌ Error: USER_ID not set. Please set USER_ID environment variable or edit the script.');
    process.exit(1);
  }

  try {
    const db = getFirestore();

    // Run syncs in parallel
    await Promise.all([
      syncOura(db),
      syncGoogleFit(db)
    ]);

    log('='.repeat(60));
    log('✅ Daily sync completed successfully');
    log('='.repeat(60));
  } catch (error) {
    log(`❌ Fatal error: ${error.message}`);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
