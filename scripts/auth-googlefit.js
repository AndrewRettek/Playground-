#!/usr/bin/env node

import { getFirestore } from './firebase-admin.js';
import { getAuthUrl, exchangeCodeForTokens } from '../server/utils/googleFitService.js';
import readline from 'readline';
import { exec } from 'child_process';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function main() {
  console.log('='.repeat(60));
  console.log('🔐 Google Fit OAuth Setup');
  console.log('='.repeat(60));
  console.log('');

  const userId = await question('Enter your Firebase User ID: ');
  console.log('');

  // Generate OAuth URL
  console.log('📝 Generating authorization URL...');
  const authUrl = getAuthUrl();

  console.log('');
  console.log('🌐 Opening browser for Google authorization...');
  console.log('If browser doesn\'t open, visit this URL:');
  console.log('');
  console.log(authUrl);
  console.log('');

  // Try to open browser (Windows)
  try {
    exec(`start ${authUrl}`);
  } catch (err) {
    // Ignore if start command fails (non-Windows or no browser)
  }

  console.log('After authorizing, you\'ll be redirected to a localhost URL.');
  console.log('The URL will look like:');
  console.log('http://localhost:3000/googlefit/callback?code=XXXXX');
  console.log('');
  console.log('Copy the ENTIRE authorization code from the URL (the part after code=)');
  console.log('');

  const code = await question('Paste the authorization code here: ');

  console.log('');
  console.log('🔄 Exchanging code for access tokens...');

  try {
    const tokens = await exchangeCodeForTokens(code);

    console.log('');
    console.log('💾 Saving tokens to Firestore...');

    const db = getFirestore();

    await db.collection('userTokens').doc(`${userId}_googlefit`).set({
      userId: userId,
      provider: 'googlefit',
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token,
      expiresAt: new Date(tokens.expiry_date),
      scopes: tokens.scope?.split(' ') || [],
      createdAt: new Date()
    });

    console.log('✅ Google Fit tokens saved successfully!');
    console.log('');
    console.log('You can now run daily-sync.js to fetch your Google Fit data');
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('');
    console.log('Make sure:');
    console.log('1. You completed the Google Cloud setup (see GOOGLE_FIT_SETUP.md)');
    console.log('2. CLIENT_ID and CLIENT_SECRET are set in server/.env');
    console.log('3. You copied the entire authorization code');
  }

  rl.close();
}

main();
