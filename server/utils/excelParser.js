import xlsx from 'xlsx';
import { parse } from 'csv-parse/sync';
import fs from 'fs';

/**
 * Parses a MyoAdapt file (CSV or Excel) and returns workout data
 * @param {string} filePath - Path to the file
 * @returns {Array} Array of workout row objects
 */
export function parseMyoAdaptFile(filePath) {
  const ext = filePath.toLowerCase().substring(filePath.lastIndexOf('.'));

  if (ext === '.csv') {
    return parseCSV(filePath);
  } else if (['.xlsx', '.xls'].includes(ext)) {
    return parseExcel(filePath);
  } else {
    throw new Error('Unsupported file format. Please upload .csv, .xlsx, or .xls files');
  }
}

/**
 * Parses a CSV file
 * @param {string} filePath - Path to the CSV file
 * @returns {Array} Array of workout row objects
 */
function parseCSV(filePath) {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const records = parse(fileContent, {
      columns: true,
      skip_empty_lines: true,
      trim: true
    });

    if (!records || records.length === 0) {
      throw new Error('CSV file is empty');
    }

    // Validate required columns
    validateRequiredColumns(records[0]);

    // Normalize data
    return normalizeData(records);

  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error('CSV file not found');
    }
    throw new Error(`Failed to parse CSV file: ${error.message}`);
  }
}

/**
 * Parses an Excel file
 * @param {string} filePath - Path to the Excel file
 * @returns {Array} Array of workout row objects
 */
function parseExcel(filePath) {
  try {
    // Read the Excel file
    const workbook = xlsx.readFile(filePath);

    // Get the first worksheet
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];

    // Convert to JSON with header row
    const rawData = xlsx.utils.sheet_to_json(worksheet);

    if (!rawData || rawData.length === 0) {
      throw new Error('Excel file is empty');
    }

    // Validate required columns
    validateRequiredColumns(rawData[0]);

    // Normalize data
    return normalizeData(rawData);

  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error('Excel file not found');
    }
    throw new Error(`Failed to parse Excel file: ${error.message}`);
  }
}

/**
 * Validates that required columns are present
 * @param {Object} firstRow - First row of data
 */
function validateRequiredColumns(firstRow) {
  const requiredColumns = ['Date', 'Exercise', 'Set time'];
  const missingColumns = requiredColumns.filter(col => !(col in firstRow));

  if (missingColumns.length > 0) {
    throw new Error(`Missing required columns: ${missingColumns.join(', ')}`);
  }
}

/**
 * Normalizes raw data into consistent format
 * @param {Array} rawData - Raw data from CSV or Excel
 * @returns {Array} Normalized data
 */
function normalizeData(rawData) {
  return rawData.map(row => ({
    date: row['Date'],
    targetMuscle: row['Target muscle'] || row['Target mu'] || '',
    day: row['Day'] || '',
    exercise: row['Exercise'] || '',
    set: row['Set'] || '',
    reps: row['Reps'] || '',
    rir: row['RIR'] || '',
    weight: row['Weight'] || '',
    bandColor: row['Band color'] || '',
    side: row['Side'] || '',
    setTime: row['Set time'] || '',
    restTime: row['Rest time'] || '',
    warmupTime: row['Warmup time'] || row['Warmup ti'] || '',
    notes: row['Notes'] || ''
  }));
}

/**
 * Validates that the file has a valid extension
 * @param {string} filename - Name of the file
 * @returns {boolean} True if valid file
 */
export function isValidFile(filename) {
  const validExtensions = ['.xlsx', '.xls', '.csv'];
  const ext = filename.toLowerCase().substring(filename.lastIndexOf('.'));
  return validExtensions.includes(ext);
}

// Keep old function name for backwards compatibility
export function parseMyoAdaptExcel(filePath) {
  return parseMyoAdaptFile(filePath);
}

export function isValidExcelFile(filename) {
  return isValidFile(filename);
}
