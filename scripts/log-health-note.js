#!/usr/bin/env node

import { getFirestore } from './firebase-admin.js';
import { format } from 'date-fns';

const USER_ID = process.env.USER_ID || 'YOUR_USER_ID_HERE';

/**
 * Log a health note/observation
 * @param {string} note - The note text
 * @param {string} category - Category (mood, workout, recovery, sleep, etc.)
 * @param {Array<string>} tags - Optional tags
 * @param {string} date - Optional date (defaults to today)
 */
export async function logHealthNote(note, category = 'general', tags = [], date = null) {
  if (USER_ID === 'YOUR_USER_ID_HERE') {
    throw new Error('USER_ID not set');
  }

  const db = getFirestore();
  const noteDate = date ? new Date(date) : new Date();

  const healthNote = {
    userId: USER_ID,
    note: note,
    category: category,
    tags: tags,
    date: format(noteDate, 'yyyy-MM-dd'),
    timestamp: noteDate
  };

  await db.collection('healthNotes').add(healthNote);

  console.log(`✅ Logged health note: "${note}" [${category}]`);

  return healthNote;
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const note = process.argv[2];
  const category = process.argv[3] || 'general';

  if (!note) {
    console.error('Usage: node log-health-note.js "note text" [category]');
    console.error('Example: node log-health-note.js "Felt great after workout" workout');
    process.exit(1);
  }

  logHealthNote(note, category)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('❌ Error:', err.message);
      process.exit(1);
    });
}
