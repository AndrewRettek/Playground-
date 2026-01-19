import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, orderBy, getDocs, where, deleteDoc, doc } from 'firebase/firestore'
import { db, auth } from '../firebase'
import { ArrowLeft, Trash2 } from 'lucide-react'
import { format } from 'date-fns'

function Notes() {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchNotes()
  }, [])

  const fetchNotes = async () => {
    try {
      const q = query(
        collection(db, 'notes'),
        where('userId', '==', auth.currentUser.uid),
        orderBy('timestamp', 'desc')
      )
      const snapshot = await getDocs(q)
      const notesData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setNotes(notesData)
    } catch (error) {
      console.error('Error fetching notes:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!title || !content) return

    setLoading(true)
    try {
      await addDoc(collection(db, 'notes'), {
        userId: auth.currentUser.uid,
        title: title,
        content: content,
        timestamp: new Date()
      })

      setTitle('')
      setContent('')
      fetchNotes()
    } catch (error) {
      console.error('Error saving note:', error)
    }
    setLoading(false)
  }

  const handleDelete = async (noteId) => {
    if (!confirm('Are you sure you want to delete this note?')) return

    try {
      await deleteDoc(doc(db, 'notes', noteId))
      fetchNotes()
    } catch (error) {
      console.error('Error deleting note:', error)
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Notes</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Create a new note</h2>

            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Note title"
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Content
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="10"
                  placeholder="What's on your mind?"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={!title || !content || loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Saving...' : 'Save Note'}
              </button>
            </form>
          </div>

          <div className="bg-white rounded-xl shadow-md p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Your Notes</h2>

            {notes.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No notes yet. Create your first note!</p>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto">
                {notes.map((note) => (
                  <div key={note.id} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-800">{note.title}</h3>
                      <button
                        onClick={() => handleDelete(note.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-gray-600 text-sm whitespace-pre-wrap mb-2">
                      {note.content}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {format(note.timestamp.toDate(), 'MMM d, yyyy h:mm a')}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Notes
