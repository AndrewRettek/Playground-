import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { collection, addDoc, query, orderBy, getDocs, where, deleteDoc, doc } from 'firebase/firestore'
import { ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'
import { db, auth, storage } from '../firebase'
import { ArrowLeft, Trash2, Upload } from 'lucide-react'
import { format } from 'date-fns'

function Photos() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [caption, setCaption] = useState('')
  const [photos, setPhotos] = useState([])
  const [loading, setLoading] = useState(false)
  const [preview, setPreview] = useState(null)

  useEffect(() => {
    fetchPhotos()
  }, [])

  useEffect(() => {
    if (selectedFile) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(selectedFile)
    } else {
      setPreview(null)
    }
  }, [selectedFile])

  const fetchPhotos = async () => {
    try {
      const q = query(
        collection(db, 'photos'),
        where('userId', '==', auth.currentUser.uid),
        orderBy('timestamp', 'desc')
      )
      const snapshot = await getDocs(q)
      const photosData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setPhotos(photosData)
    } catch (error) {
      console.error('Error fetching photos:', error)
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!selectedFile) return

    setLoading(true)
    try {
      const fileName = `${auth.currentUser.uid}/${Date.now()}_${selectedFile.name}`
      const storageRef = ref(storage, fileName)

      await uploadBytes(storageRef, selectedFile)
      const downloadURL = await getDownloadURL(storageRef)

      await addDoc(collection(db, 'photos'), {
        userId: auth.currentUser.uid,
        url: downloadURL,
        storagePath: fileName,
        caption: caption,
        timestamp: new Date()
      })

      setSelectedFile(null)
      setCaption('')
      setPreview(null)
      fetchPhotos()
    } catch (error) {
      console.error('Error uploading photo:', error)
      alert('Error uploading photo. Please try again.')
    }
    setLoading(false)
  }

  const handleDelete = async (photo) => {
    if (!confirm('Are you sure you want to delete this photo?')) return

    try {
      const storageRef = ref(storage, photo.storagePath)
      await deleteObject(storageRef)
      await deleteDoc(doc(db, 'photos', photo.id))
      fetchPhotos()
    } catch (error) {
      console.error('Error deleting photo:', error)
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Photos</h1>

        <div className="bg-white rounded-xl shadow-md p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Upload a photo</h2>

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Choose photo
              </label>
              <div className="flex items-center space-x-4">
                <label className="flex-1 cursor-pointer">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
                    {preview ? (
                      <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded" />
                    ) : (
                      <div>
                        <Upload className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                        <p className="text-gray-600">Click to select a photo</p>
                      </div>
                    )}
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </label>
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Caption (optional)
              </label>
              <input
                type="text"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Add a caption"
              />
            </div>

            <button
              type="submit"
              disabled={!selectedFile || loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Uploading...' : 'Upload Photo'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-md p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Your Photos</h2>

          {photos.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No photos yet. Upload your first photo!</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {photos.map((photo) => (
                <div key={photo.id} className="relative group">
                  <img
                    src={photo.url}
                    alt={photo.caption || 'Photo'}
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all rounded-lg flex items-center justify-center">
                    <button
                      onClick={() => handleDelete(photo)}
                      className="opacity-0 group-hover:opacity-100 bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition-all"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                  {photo.caption && (
                    <p className="mt-2 text-sm text-gray-700">{photo.caption}</p>
                  )}
                  <p className="text-xs text-gray-400">
                    {format(photo.timestamp.toDate(), 'MMM d, yyyy')}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Photos
