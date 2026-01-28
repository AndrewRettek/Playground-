import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, orderBy, limit, getDocs, where, deleteDoc, doc } from 'firebase/firestore'
import { db, auth } from '../firebase'
import { ArrowLeft, Trash2 } from 'lucide-react'
import { format } from 'date-fns'

const workoutTypes = [
  'Running', 'Cycling', 'Swimming', 'Walking', 'Weightlifting',
  'Yoga', 'HIIT', 'Pilates', 'CrossFit', 'Other'
]

function WorkoutData() {
  const [workoutType, setWorkoutType] = useState('')
  const [duration, setDuration] = useState('')
  const [calories, setCalories] = useState('')
  const [distance, setDistance] = useState('')
  const [notes, setNotes] = useState('')
  const [workouts, setWorkouts] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchWorkouts()
  }, [])

  const fetchWorkouts = async () => {
    try {
      const q = query(
        collection(db, 'workouts'),
        where('userId', '==', auth.currentUser.uid),
        orderBy('timestamp', 'desc'),
        limit(20)
      )
      const snapshot = await getDocs(q)
      const workoutsData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setWorkouts(workoutsData)
    } catch (error) {
      console.error('Error fetching workouts:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!workoutType || !duration) return

    setLoading(true)
    try {
      await addDoc(collection(db, 'workouts'), {
        userId: auth.currentUser.uid,
        workoutType,
        duration: parseInt(duration),
        calories: calories ? parseInt(calories) : null,
        distance: distance ? parseFloat(distance) : null,
        notes,
        timestamp: new Date()
      })

      setWorkoutType('')
      setDuration('')
      setCalories('')
      setDistance('')
      setNotes('')
      fetchWorkouts()
    } catch (error) {
      console.error('Error saving workout:', error)
    }
    setLoading(false)
  }

  const handleDelete = async (workoutId) => {
    if (!confirm('Are you sure you want to delete this workout?')) return

    try {
      await deleteDoc(doc(db, 'workouts', workoutId))
      fetchWorkouts()
    } catch (error) {
      console.error('Error deleting workout:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link to="/" className="flex items-center text-gray-600 hover:text-gray-800">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Dashboard
          </Link>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Workout Data</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Log a workout</h2>

            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Workout Type
                </label>
                <select
                  value={workoutType}
                  onChange={(e) => setWorkoutType(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select a type</option>
                  {workoutTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Duration (minutes)
                </label>
                <input
                  type="number"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., 30"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Calories (optional)
                </label>
                <input
                  type="number"
                  value={calories}
                  onChange={(e) => setCalories(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., 300"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Distance (km, optional)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={distance}
                  onChange={(e) => setDistance(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., 5.0"
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notes (optional)
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="3"
                  placeholder="How did it go?"
                />
              </div>

              <button
                type="submit"
                disabled={!workoutType || !duration || loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Saving...' : 'Save Workout'}
              </button>
            </form>
          </div>

          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Recent Workouts</h2>

            {workouts.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No workouts yet. Log your first workout!</p>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto">
                {workouts.map((workout) => (
                  <div key={workout.id} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-semibold text-gray-800">{workout.workoutType}</h3>
                        <div className="flex flex-wrap gap-3 mt-2 text-sm text-gray-600">
                          <span>{workout.duration} min</span>
                          {workout.calories && <span>{workout.calories} cal</span>}
                          {workout.distance && <span>{workout.distance} km</span>}
                        </div>
                      </div>
                      <button
                        onClick={() => handleDelete(workout.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    {workout.notes && (
                      <p className="text-gray-600 text-sm mt-2">{workout.notes}</p>
                    )}
                    <p className="text-gray-400 text-xs mt-2">
                      {format(workout.timestamp.toDate(), 'MMM d, yyyy h:mm a')}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Import Workout Data
          </h3>
          <p className="text-blue-800 text-sm mb-4">
            Import your workout data from MyoAdapt or other fitness apps. Upload a CSV or Excel file and we'll automatically parse and add your workouts.
          </p>
          <Link
            to="/workouts/import"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
          >
            Import from MyoAdapt
          </Link>
        </div>
      </div>
    </div>
  )
}

export default WorkoutData
