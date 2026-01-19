import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Activity, Moon, Heart, Flame } from 'lucide-react'
import axios from 'axios'
import { format } from 'date-fns'

function OuraIntegration() {
  const [isConnected, setIsConnected] = useState(false)
  const [accessToken, setAccessToken] = useState('')
  const [ouraData, setOuraData] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('oura_access_token')
    if (token) {
      setAccessToken(token)
      setIsConnected(true)
      fetchOuraData(token)
    }
  }, [])

  const handleConnect = () => {
    const token = prompt('Enter your Oura API Personal Access Token:\n\nGet it from: https://cloud.ouraring.com/personal-access-tokens')
    if (token) {
      localStorage.setItem('oura_access_token', token)
      setAccessToken(token)
      setIsConnected(true)
      fetchOuraData(token)
    }
  }

  const handleDisconnect = () => {
    localStorage.removeItem('oura_access_token')
    setAccessToken('')
    setIsConnected(false)
    setOuraData(null)
  }

  const fetchOuraData = async (token) => {
    setLoading(true)
    try {
      const today = format(new Date(), 'yyyy-MM-dd')

      const [sleepResponse, activityResponse, readinessResponse] = await Promise.all([
        axios.get('/api/oura/sleep', {
          params: { token, date: today }
        }),
        axios.get('/api/oura/activity', {
          params: { token, date: today }
        }),
        axios.get('/api/oura/readiness', {
          params: { token, date: today }
        })
      ])

      setOuraData({
        sleep: sleepResponse.data,
        activity: activityResponse.data,
        readiness: readinessResponse.data
      })
    } catch (error) {
      console.error('Error fetching Oura data:', error)
      alert('Error fetching Oura data. Please check your token and try again.')
    }
    setLoading(false)
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Oura Ring Integration</h1>

        {!isConnected ? (
          <div className="bg-white rounded-xl shadow-md p-8 text-center">
            <div className="bg-purple-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
              <Activity className="w-12 h-12 text-purple-600" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Connect Your Oura Ring</h2>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Track your sleep, activity, and readiness scores from your Oura Ring.
              You'll need a Personal Access Token from your Oura account.
            </p>
            <div className="space-y-4">
              <button
                onClick={handleConnect}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium"
              >
                Connect Oura Ring
              </button>
              <p className="text-sm text-gray-500">
                Get your token at:{' '}
                <a
                  href="https://cloud.ouraring.com/personal-access-tokens"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-purple-600 hover:underline"
                >
                  cloud.ouraring.com/personal-access-tokens
                </a>
              </p>
            </div>
          </div>
        ) : (
          <div>
            <div className="bg-white rounded-xl shadow-md p-6 mb-8 flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-gray-700 font-medium">Oura Ring Connected</span>
              </div>
              <div className="space-x-4">
                <button
                  onClick={() => fetchOuraData(accessToken)}
                  disabled={loading}
                  className="px-4 py-2 text-purple-600 hover:text-purple-700 font-medium disabled:opacity-50"
                >
                  {loading ? 'Refreshing...' : 'Refresh Data'}
                </button>
                <button
                  onClick={handleDisconnect}
                  className="px-4 py-2 text-red-600 hover:text-red-700 font-medium"
                >
                  Disconnect
                </button>
              </div>
            </div>

            {loading ? (
              <div className="bg-white rounded-xl shadow-md p-8 text-center">
                <p className="text-gray-600">Loading Oura data...</p>
              </div>
            ) : ouraData ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl shadow-md p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="bg-blue-100 p-3 rounded-lg">
                      <Moon className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-800">Sleep</h3>
                  </div>
                  {ouraData.sleep ? (
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Score</span>
                        <span className="font-semibold">{ouraData.sleep.score || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total Sleep</span>
                        <span className="font-semibold">{ouraData.sleep.total_sleep_duration ? `${Math.round(ouraData.sleep.total_sleep_duration / 3600)}h ${Math.round((ouraData.sleep.total_sleep_duration % 3600) / 60)}m` : 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Efficiency</span>
                        <span className="font-semibold">{ouraData.sleep.efficiency ? `${ouraData.sleep.efficiency}%` : 'N/A'}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No sleep data available</p>
                  )}
                </div>

                <div className="bg-white rounded-xl shadow-md p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="bg-green-100 p-3 rounded-lg">
                      <Heart className="w-6 h-6 text-green-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-800">Readiness</h3>
                  </div>
                  {ouraData.readiness ? (
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Score</span>
                        <span className="font-semibold">{ouraData.readiness.score || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Temperature</span>
                        <span className="font-semibold">{ouraData.readiness.temperature_deviation ? `${ouraData.readiness.temperature_deviation > 0 ? '+' : ''}${ouraData.readiness.temperature_deviation}°C` : 'N/A'}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No readiness data available</p>
                  )}
                </div>

                <div className="bg-white rounded-xl shadow-md p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="bg-orange-100 p-3 rounded-lg">
                      <Flame className="w-6 h-6 text-orange-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-800">Activity</h3>
                  </div>
                  {ouraData.activity ? (
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Score</span>
                        <span className="font-semibold">{ouraData.activity.score || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Steps</span>
                        <span className="font-semibold">{ouraData.activity.steps?.toLocaleString() || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Calories</span>
                        <span className="font-semibold">{ouraData.activity.total_calories || 'N/A'}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No activity data available</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-md p-8 text-center">
                <p className="text-gray-600">Click "Refresh Data" to load your Oura stats</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default OuraIntegration
