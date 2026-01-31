#!/usr/bin/env node

import { getFirestore } from './firebase-admin.js';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function main() {
  console.log('='.repeat(60));
  console.log('🔐 Oura Ring Token Setup');
  console.log('='.repeat(60));
  console.log('');

  const userId = await question('Enter your Firebase User ID: ');
  console.log('');
  console.log('Get your Oura Personal Access Token from:');
  console.log('👉 https://cloud.ouraring.com/personal-access-tokens');
  console.log('');
  const token = await question('Enter your Oura token: ');

  console.log('');
  console.log('💾 Saving token to Firestore...');

  try {
    const db = getFirestore();

    await db.collection('userTokens').doc(`${userId}_oura`).set({
      userId: userId,
      provider: 'oura',
      accessToken: token,
      createdAt: new Date()
    });

    console.log('✅ Oura token saved successfully!');
    console.log('');
    console.log('You can now run daily-sync.js to fetch your Oura data');
  } catch (error) {
    console.error('❌ Error saving token:', error.message);
  }

  rl.close();
}

main();
