import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from './firebase'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import MoodTracker from './components/MoodTracker'
import SleepTracker from './components/SleepTracker'
import Notes from './components/Notes'
import Photos from './components/Photos'
import OuraIntegration from './components/OuraIntegration'
import WorkoutData from './components/WorkoutData'
import WorkoutImport from './components/WorkoutImport'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
    })
    return unsubscribe
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        <Route path="/" element={user ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/mood" element={user ? <MoodTracker /> : <Navigate to="/login" />} />
        <Route path="/sleep" element={user ? <SleepTracker /> : <Navigate to="/login" />} />
        <Route path="/notes" element={user ? <Notes /> : <Navigate to="/login" />} />
        <Route path="/photos" element={user ? <Photos /> : <Navigate to="/login" />} />
        <Route path="/oura" element={user ? <OuraIntegration /> : <Navigate to="/login" />} />
        <Route path="/workouts" element={user ? <WorkoutData /> : <Navigate to="/login" />} />
        <Route path="/workouts/import" element={user ? <WorkoutImport /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  )
}

export default App
