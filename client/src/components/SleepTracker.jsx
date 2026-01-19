import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, orderBy, limit, getDocs, where } from 'firebase/firestore'
import { db, auth } from '../firebase'
import { ArrowLeft } from 'lucide-react'
import { format } from 'date-fns'

const sleepQualities = [
  { label: 'Excellent', value: 5, color: 'bg-green-500' },
  { label: 'Good', value: 4, color: 'bg-blue-500' },
  { label: 'Fair', value: 3, color: 'bg-yellow-500' },
  { label: 'Poor', value: 2, color: 'bg-orange-500' },
  { label: 'Terrible', value: 1, color: 'bg-red-500' }
]

function SleepTracker() {
  const [hours, setHours] = useState('')
  const [quality, setQuality] = useState(null)
  const [note, setNote] = useState('')
  const [recentSleep, setRecentSleep] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchRecentSleep()
  }, [])

  const fetchRecentSleep = async () => {
    try {
      const q = query(
        collection(db, 'sleep'),
        where('userId', '==', auth.currentUser.uid),
        orderBy('timestamp', 'desc'),
        limit(10)
      )
      const snapshot = await getDocs(q)
      const sleep = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setRecentSleep(sleep)
    } catch (error) {
      console.error('Error fetching sleep data:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!hours || !quality) return

    setLoading(true)
    try {
      await addDoc(collection(db, 'sleep'), {
        userId: auth.currentUser.uid,
        hours: parseFloat(hours),
        quality: quality,
        note: note,
        timestamp: new Date()
      })

      setHours('')
      setQuality(null)
      setNote('')
      fetchRecentSleep()
    } catch (error) {
      console.error('Error saving sleep data:', error)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link to="/" className="flex items-center text-gray-600 hover:text-gray-800">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Dashboard
          </Link>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Sleep Tracker</h1>

        <div className="bg-white rounded-xl shadow-md p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Log your sleep</h2>

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hours of sleep
              </label>
              <input
                type="number"
                step="0.5"
                min="0"
                max="24"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 7.5"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Sleep quality
              </label>
              <div className="grid grid-cols-5 gap-3">
                {sleepQualities.map((sq) => (
                  <button
                    key={sq.value}
                    type="button"
                    onClick={() => setQuality(sq.value)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      quality === sq.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className={`w-8 h-8 ${sq.color} rounded-full mx-auto mb-2`}></div>
                    <div className="text-xs font-medium text-gray-700">{sq.label}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notes (optional)
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="3"
                placeholder="How did you sleep? Any dreams?"
              />
            </div>

            <button
              type="submit"
              disabled={!hours || !quality || loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Save Sleep Data'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-md p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Recent Sleep</h2>

          {recentSleep.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No sleep data yet. Start tracking!</p>
          ) : (
            <div className="space-y-4">
              {recentSleep.map((sleep) => {
                const qualityData = sleepQualities.find(sq => sq.value === sleep.quality)
                return (
                  <div key={sleep.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div className={`w-12 h-12 ${qualityData?.color} rounded-full flex items-center justify-center text-white font-bold`}>
                      {sleep.hours}h
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-800">
                        {sleep.hours} hours - {qualityData?.label}
                      </div>
                      {sleep.note && <p className="text-gray-600 text-sm mt-1">{sleep.note}</p>}
                      <p className="text-gray-400 text-xs mt-2">
                        {format(sleep.timestamp.toDate(), 'MMM d, yyyy h:mm a')}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SleepTracker
