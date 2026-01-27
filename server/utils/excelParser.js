import xlsx from 'xlsx';

/**
 * Parses a MyoAdapt Excel file and returns workout data
 * @param {string} filePath - Path to the Excel file
 * @returns {Array} Array of workout row objects
 */
export function parseMyoAdaptExcel(filePath) {
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
    const requiredColumns = ['Date', 'Exercise', 'Set time'];
    const firstRow = rawData[0];
    const missingColumns = requiredColumns.filter(col => !(col in firstRow));

    if (missingColumns.length > 0) {
      throw new Error(`Missing required columns: ${missingColumns.join(', ')}`);
    }

    // Parse and normalize the data
    const normalizedData = rawData.map(row => ({
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

    return normalizedData;

  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error('Excel file not found');
    }
    throw new Error(`Failed to parse Excel file: ${error.message}`);
  }
}

/**
 * Validates that the file is a valid Excel format
 * @param {string} filename - Name of the file
 * @returns {boolean} True if valid Excel file
 */
export function isValidExcelFile(filename) {
  const validExtensions = ['.xlsx', '.xls'];
  const ext = filename.toLowerCase().substring(filename.lastIndexOf('.'));
  return validExtensions.includes(ext);
}
