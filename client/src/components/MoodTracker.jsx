import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, orderBy, limit, getDocs, where } from 'firebase/firestore'
import { db, auth } from '../firebase'
import { ArrowLeft } from 'lucide-react'
import { format } from 'date-fns'

const moods = [
  { emoji: '😄', label: 'Great', value: 5 },
  { emoji: '🙂', label: 'Good', value: 4 },
  { emoji: '😐', label: 'Okay', value: 3 },
  { emoji: '😔', label: 'Bad', value: 2 },
  { emoji: '😢', label: 'Terrible', value: 1 }
]

function MoodTracker() {
  const [selectedMood, setSelectedMood] = useState(null)
  const [note, setNote] = useState('')
  const [recentMoods, setRecentMoods] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchRecentMoods()
  }, [])

  const fetchRecentMoods = async () => {
    try {
      const q = query(
        collection(db, 'moods'),
        where('userId', '==', auth.currentUser.uid),
        orderBy('timestamp', 'desc'),
        limit(10)
      )
      const snapshot = await getDocs(q)
      const moods = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setRecentMoods(moods)
    } catch (error) {
      console.error('Error fetching moods:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedMood) return

    setLoading(true)
    try {
      await addDoc(collection(db, 'moods'), {
        userId: auth.currentUser.uid,
        mood: selectedMood,
        note: note,
        timestamp: new Date()
      })

      setSelectedMood(null)
      setNote('')
      fetchRecentMoods()
    } catch (error) {
      console.error('Error saving mood:', error)
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Mood Tracker</h1>

        <div className="bg-white rounded-xl shadow-md p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">How are you feeling?</h2>

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-5 gap-4 mb-6">
              {moods.map((mood) => (
                <button
                  key={mood.value}
                  type="button"
                  onClick={() => setSelectedMood(mood.value)}
                  className={`p-6 rounded-xl border-2 transition-all ${
                    selectedMood === mood.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-4xl mb-2">{mood.emoji}</div>
                  <div className="text-sm font-medium text-gray-700">{mood.label}</div>
                </button>
              ))}
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add a note (optional)
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="3"
                placeholder="What's on your mind?"
              />
            </div>

            <button
              type="submit"
              disabled={!selectedMood || loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Save Mood'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-md p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Recent Moods</h2>

          {recentMoods.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No mood entries yet. Start tracking!</p>
          ) : (
            <div className="space-y-4">
              {recentMoods.map((mood) => {
                const moodData = moods.find(m => m.value === mood.mood)
                return (
                  <div key={mood.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div className="text-3xl">{moodData?.emoji}</div>
                    <div className="flex-1">
                      <div className="font-medium text-gray-800">{moodData?.label}</div>
                      {mood.note && <p className="text-gray-600 text-sm mt-1">{mood.note}</p>}
                      <p className="text-gray-400 text-xs mt-2">
                        {format(mood.timestamp.toDate(), 'MMM d, yyyy h:mm a')}
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

export default MoodTracker
