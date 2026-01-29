import { google } from 'googleapis';

// OAuth2 configuration
// These values should come from environment variables after user completes Google Cloud setup
const CLIENT_ID = process.env.GOOGLE_FIT_CLIENT_ID || 'YOUR_CLIENT_ID_HERE';
const CLIENT_SECRET = process.env.GOOGLE_FIT_CLIENT_SECRET || 'YOUR_CLIENT_SECRET_HERE';
const REDIRECT_URI = process.env.GOOGLE_FIT_REDIRECT_URI || 'http://localhost:3000/googlefit/callback';

// OAuth2 scopes
const SCOPES = [
  'https://www.googleapis.com/auth/fitness.body.read',
  'https://www.googleapis.com/auth/fitness.activity.read',
  'https://www.googleapis.com/auth/fitness.heart_rate.read',
  'https://www.googleapis.com/auth/fitness.sleep.read'
];

/**
 * Creates an OAuth2 client
 */
function getOAuth2Client() {
  return new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);
}

/**
 * Generates the OAuth2 authorization URL
 * @returns {string} Authorization URL
 */
export function getAuthUrl() {
  const oauth2Client = getOAuth2Client();

  return oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent' // Force consent screen to get refresh token
  });
}

/**
 * Exchanges authorization code for tokens
 * @param {string} code - Authorization code from OAuth callback
 * @returns {Promise<Object>} Tokens object { access_token, refresh_token, expiry_date }
 */
export async function exchangeCodeForTokens(code) {
  const oauth2Client = getOAuth2Client();

  const { tokens } = await oauth2Client.getToken(code);
  return tokens;
}

/**
 * Refreshes an expired access token
 * @param {string} refreshToken - Refresh token
 * @returns {Promise<Object>} New tokens object
 */
export async function refreshAccessToken(refreshToken) {
  const oauth2Client = getOAuth2Client();
  oauth2Client.setCredentials({ refresh_token: refreshToken });

  const { credentials } = await oauth2Client.refreshAccessToken();
  return credentials;
}

/**
 * Fetches weight data from Google Fit
 * @param {string} accessToken - Google Fit access token
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Promise<Array>} Array of weight data points
 */
export async function fetchWeightData(accessToken, startDate, endDate) {
  const oauth2Client = getOAuth2Client();
  oauth2Client.setCredentials({ access_token: accessToken });

  const fitness = google.fitness({ version: 'v1', auth: oauth2Client });

  // Convert dates to timestamps (milliseconds since epoch)
  const startTime = new Date(startDate).getTime();
  const endTime = new Date(endDate).setHours(23, 59, 59, 999);

  try {
    const response = await fitness.users.dataset.aggregate({
      userId: 'me',
      requestBody: {
        aggregateBy: [{
          dataTypeName: 'com.google.weight',
          dataSourceId: 'derived:com.google.weight:com.google.android.gms:merge_weight'
        }],
        bucketByTime: { durationMillis: 86400000 }, // 1 day buckets
        startTimeMillis: startTime,
        endTimeMillis: endTime
      }
    });

    // Parse the response
    const weightData = [];

    if (response.data.bucket) {
      for (const bucket of response.data.bucket) {
        if (bucket.dataset && bucket.dataset[0] && bucket.dataset[0].point) {
          for (const point of bucket.dataset[0].point) {
            const timestamp = new Date(parseInt(point.startTimeNanos) / 1000000);
            const weight = point.value[0].fpVal; // Weight in kg

            weightData.push({
              date: timestamp.toISOString().split('T')[0],
              weight: weight,
              timestamp: timestamp
            });
          }
        }
      }
    }

    return weightData;

  } catch (error) {
    console.error('Error fetching Google Fit weight data:', error);
    throw new Error(`Failed to fetch weight data: ${error.message}`);
  }
}

/**
 * Fetches activity data (steps, calories) from Google Fit
 * @param {string} accessToken - Google Fit access token
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Promise<Array>} Array of activity data points
 */
export async function fetchActivityData(accessToken, startDate, endDate) {
  const oauth2Client = getOAuth2Client();
  oauth2Client.setCredentials({ access_token: accessToken });

  const fitness = google.fitness({ version: 'v1', auth: oauth2Client });

  // Convert dates to timestamps
  const startTime = new Date(startDate).getTime();
  const endTime = new Date(endDate).setHours(23, 59, 59, 999);

  try {
    const response = await fitness.users.dataset.aggregate({
      userId: 'me',
      requestBody: {
        aggregateBy: [
          {
            dataTypeName: 'com.google.step_count.delta',
            dataSourceId: 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'
          },
          {
            dataTypeName: 'com.google.calories.expended',
            dataSourceId: 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended'
          },
          {
            dataTypeName: 'com.google.active_minutes',
            dataSourceId: 'derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes'
          }
        ],
        bucketByTime: { durationMillis: 86400000 }, // 1 day buckets
        startTimeMillis: startTime,
        endTimeMillis: endTime
      }
    });

    // Parse the response
    const activityData = [];

    if (response.data.bucket) {
      for (const bucket of response.data.bucket) {
        const timestamp = new Date(parseInt(bucket.startTimeMillis));
        const date = timestamp.toISOString().split('T')[0];

        let steps = 0;
        let calories = 0;
        let activeMinutes = 0;

        // Extract data from datasets
        if (bucket.dataset) {
          // Steps (dataset 0)
          if (bucket.dataset[0] && bucket.dataset[0].point && bucket.dataset[0].point.length > 0) {
            steps = bucket.dataset[0].point[0].value[0].intVal || 0;
          }

          // Calories (dataset 1)
          if (bucket.dataset[1] && bucket.dataset[1].point && bucket.dataset[1].point.length > 0) {
            calories = bucket.dataset[1].point[0].value[0].fpVal || 0;
          }

          // Active minutes (dataset 2)
          if (bucket.dataset[2] && bucket.dataset[2].point && bucket.dataset[2].point.length > 0) {
            activeMinutes = bucket.dataset[2].point[0].value[0].intVal || 0;
          }
        }

        activityData.push({
          date,
          steps,
          totalCalories: Math.round(calories),
          activeMinutes,
          timestamp
        });
      }
    }

    return activityData;

  } catch (error) {
    console.error('Error fetching Google Fit activity data:', error);
    throw new Error(`Failed to fetch activity data: ${error.message}`);
  }
}
