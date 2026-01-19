import { Link } from 'react-router-dom'
import { signOut } from 'firebase/auth'
import { auth } from '../firebase'
import { Smile, Moon, FileText, Image, Activity, Watch } from 'lucide-react'

function Dashboard() {
  const handleLogout = () => {
    signOut(auth)
  }

  const features = [
    { name: 'Mood Tracker', icon: Smile, path: '/mood', color: 'bg-yellow-500' },
    { name: 'Sleep Tracker', icon: Moon, path: '/sleep', color: 'bg-indigo-500' },
    { name: 'Notes', icon: FileText, path: '/notes', color: 'bg-green-500' },
    { name: 'Photos', icon: Image, path: '/photos', color: 'bg-pink-500' },
    { name: 'Oura Integration', icon: Watch, path: '/oura', color: 'bg-purple-500' },
    { name: 'Workout Data', icon: Activity, path: '/workouts', color: 'bg-red-500' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Life Logger</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Sign Out
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Welcome back!
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => (
            <Link
              key={feature.path}
              to={feature.path}
              className="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow p-6 flex items-center space-x-4"
            >
              <div className={`${feature.color} p-3 rounded-lg`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <span className="text-lg font-semibold text-gray-800">
                {feature.name}
              </span>
            </Link>
          ))}
        </div>

        <div className="mt-12 bg-white rounded-xl shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Today's Summary
          </h3>
          <p className="text-gray-600">
            Track your mood, sleep, notes, and photos all in one place. Connect your Oura ring and workout data for a complete picture of your health and wellness.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
