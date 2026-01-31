import admin from 'firebase-admin';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let db = null;

/**
 * Initialize Firebase Admin SDK
 * @returns {Object} Firestore database instance
 */
export function initializeFirebase() {
  if (db) {
    return db;
  }

  try {
    // Load service account key
    const serviceAccountPath = join(__dirname, '..', 'firebase-admin-key.json');
    const serviceAccount = JSON.parse(readFileSync(serviceAccountPath, 'utf8'));

    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });

    db = admin.firestore();
    console.log('✅ Firebase Admin initialized');
    return db;
  } catch (error) {
    console.error('❌ Failed to initialize Firebase Admin:', error.message);
    throw error;
  }
}

/**
 * Get Firestore instance (initializes if needed)
 * @returns {Object} Firestore database
 */
export function getFirestore() {
  if (!db) {
    return initializeFirebase();
  }
  return db;
}

export { admin };
