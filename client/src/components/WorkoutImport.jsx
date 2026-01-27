import { useState } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, where, getDocs } from 'firebase/firestore'
import { db, auth } from '../firebase'
import { ArrowLeft, Upload, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'

function WorkoutImport() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setError(null)
      setResult(null)
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
      setResult(null)
    }
  }

  const checkForDuplicates = async (workouts) => {
    const userId = auth.currentUser.uid
    const duplicates = []

    for (const workout of workouts) {
      // Check if workout already exists for this date
      const workoutDate = new Date(workout.timestamp)
      workoutDate.setHours(0, 0, 0, 0)

      const nextDay = new Date(workoutDate)
      nextDay.setDate(nextDay.getDate() + 1)

      const q = query(
        collection(db, 'workouts'),
        where('userId', '==', userId),
        where('timestamp', '>=', workoutDate),
        where('timestamp', '<', nextDay)
      )

      const snapshot = await getDocs(q)
      if (!snapshot.empty) {
        duplicates.push(workoutDate.toLocaleDateString())
      }
    }

    return duplicates
  }

  const handleImport = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Create FormData to send file
      const formData = new FormData()
      formData.append('file', file)
      formData.append('userId', auth.currentUser.uid)

      // Send to server for parsing
      const response = await axios.post('/api/workouts/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      if (!response.data.success) {
        throw new Error(response.data.error || 'Import failed')
      }

      const { workouts } = response.data

      // Check for duplicates
      const duplicateDates = await checkForDuplicates(workouts)

      // Filter out duplicates
      const workoutsToImport = workouts.filter(workout => {
        const dateStr = new Date(workout.timestamp).toLocaleDateString()
        return !duplicateDates.includes(dateStr)
      })

      // Save non-duplicate workouts to Firestore
      let importedCount = 0
      for (const workout of workoutsToImport) {
        await addDoc(collection(db, 'workouts'), {
          ...workout,
          timestamp: new Date(workout.timestamp) // Convert string to Date
        })
        importedCount++
      }

      setResult({
        total: workouts.length,
        imported: importedCount,
        skipped: duplicateDates.length,
        duplicateDates
      })

      setFile(null)

    } catch (err) {
      console.error('Import error:', err)
      setError(err.response?.data?.error || err.message || 'Failed to import workouts')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link to="/workouts" className="flex items-center text-gray-600 hover:text-gray-800">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Workouts
          </Link>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Import MyoAdapt Data</h1>

        <div className="bg-white rounded-xl shadow-md p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Upload Excel File</h2>

          {/* Drag & Drop Zone */}
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />

            {file ? (
              <div className="mb-4">
                <p className="text-gray-700 font-medium">{file.name}</p>
                <p className="text-gray-500 text-sm">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            ) : (
              <div>
                <p className="text-gray-600 mb-2">
                  Drag and drop your MyoAdapt Excel file here
                </p>
                <p className="text-gray-500 text-sm">or</p>
              </div>
            )}

            <label className="mt-4 inline-block">
              <span className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors cursor-pointer">
                {file ? 'Choose Different File' : 'Select File'}
              </span>
              <input
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          </div>

          {/* Import Button */}
          <button
            onClick={handleImport}
            disabled={!file || loading}
            className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Importing...' : 'Import Workouts'}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
              <XCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-red-800 font-medium">Import Failed</p>
                <p className="text-red-600 text-sm mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Success Message */}
          {result && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-green-800 font-medium">Import Successful!</p>
                  <div className="text-green-700 text-sm mt-2">
                    <p>• Imported: {result.imported} workout(s)</p>
                    {result.skipped > 0 && (
                      <p>• Skipped: {result.skipped} duplicate(s)</p>
                    )}
                  </div>
                  {result.duplicateDates.length > 0 && (
                    <details className="mt-2">
                      <summary className="text-green-700 text-sm cursor-pointer">
                        View skipped dates
                      </summary>
                      <ul className="text-green-600 text-sm mt-1 ml-4 list-disc">
                        {result.duplicateDates.map((date, i) => (
                          <li key={i}>{date}</li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">
            How to Import
          </h3>
          <ol className="text-blue-800 text-sm space-y-2">
            <li>1. Request workout export from your MyoAdapt app</li>
            <li>2. Download the Excel file from the email MyoAdapt sends you</li>
            <li>3. Upload the file here using drag & drop or the file selector</li>
            <li>4. Click "Import Workouts" and wait for processing</li>
            <li>5. Your workouts will be automatically added to your log!</li>
          </ol>

          <div className="mt-4 pt-4 border-t border-blue-200">
            <p className="text-blue-900 font-medium text-sm mb-1">What gets imported:</p>
            <ul className="text-blue-700 text-sm space-y-1 ml-4 list-disc">
              <li>One workout entry per day</li>
              <li>Total duration calculated from all sets</li>
              <li>Summary of exercises and muscle groups</li>
              <li>Duplicate dates are automatically skipped</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WorkoutImport
