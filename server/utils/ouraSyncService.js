import axios from 'axios';

const OURA_API_BASE = 'https://api.ouraring.com/v2/usercollection';

/**
 * Fetches Oura data for multiple dates and returns structured data
 * @param {string} token - Oura Personal Access Token
 * @param {Array<string>} dates - Array of date strings (YYYY-MM-DD)
 * @returns {Promise<Array>} Array of Oura data objects by date
 */
export async function syncOuraData(token, dates) {
  if (!token) {
    throw new Error('Oura token is required');
  }

  if (!dates || dates.length === 0) {
    throw new Error('At least one date is required');
  }

  const results = [];

  for (const date of dates) {
    try {
      // Fetch all three endpoints for this date
      const [sleepResponse, activityResponse, readinessResponse] = await Promise.all([
        axios.get(`${OURA_API_BASE}/daily_sleep`, {
          headers: { 'Authorization': `Bearer ${token}` },
          params: { start_date: date, end_date: date }
        }),
        axios.get(`${OURA_API_BASE}/daily_activity`, {
          headers: { 'Authorization': `Bearer ${token}` },
          params: { start_date: date, end_date: date }
        }),
        axios.get(`${OURA_API_BASE}/daily_readiness`, {
          headers: { 'Authorization': `Bearer ${token}` },
          params: { start_date: date, end_date: date }
        })
      ]);

      // Extract data (first item in array, or null if no data)
      const sleepData = sleepResponse.data.data && sleepResponse.data.data.length > 0
        ? sleepResponse.data.data[0]
        : null;

      const activityData = activityResponse.data.data && activityResponse.data.data.length > 0
        ? activityResponse.data.data[0]
        : null;

      const readinessData = readinessResponse.data.data && readinessResponse.data.data.length > 0
        ? readinessResponse.data.data[0]
        : null;

      results.push({
        date,
        sleep: sleepData,
        activity: activityData,
        readiness: readinessData,
        syncedAt: new Date()
      });

    } catch (error) {
      console.error(`Error fetching Oura data for ${date}:`, error.message);
      // Continue with other dates even if one fails
      results.push({
        date,
        sleep: null,
        activity: null,
        readiness: null,
        error: error.message,
        syncedAt: new Date()
      });
    }
  }

  return results;
}

/**
 * Fetches Oura data for a date range
 * @param {string} token - Oura Personal Access Token
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Promise<Array>} Array of Oura data objects
 */
export async function syncOuraDataRange(token, startDate, endDate) {
  if (!token) {
    throw new Error('Oura token is required');
  }

  if (!startDate || !endDate) {
    throw new Error('Start date and end date are required');
  }

  // Generate array of dates between start and end
  const dates = [];
  const current = new Date(startDate);
  const end = new Date(endDate);

  while (current <= end) {
    dates.push(current.toISOString().split('T')[0]);
    current.setDate(current.getDate() + 1);
  }

  return syncOuraData(token, dates);
}
