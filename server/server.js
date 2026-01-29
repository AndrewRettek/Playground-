import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import axios from 'axios'
import multer from 'multer'
import { importWorkoutsFromExcel } from './controllers/workoutImportController.js'
import { syncOuraDataRange } from './utils/ouraSyncService.js'
import { getAuthUrl, exchangeCodeForTokens, fetchWeightData, fetchActivityData } from './utils/googleFitService.js'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 5000

app.use(cors())
app.use(express.json())

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/') // Store in uploads directory
  },
  filename: (req, file, cb) => {
    // Generate unique filename
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
    cb(null, uniqueSuffix + '-' + file.originalname)
  }
})

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB limit
  }
})

// Oura API endpoints
app.get('/api/oura/sleep', async (req, res) => {
  try {
    const { token, date } = req.query

    if (!token) {
      return res.status(400).json({ error: 'Token required' })
    }

    const response = await axios.get('https://api.ouraring.com/v2/usercollection/daily_sleep', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        start_date: date,
        end_date: date
      }
    })

    const sleepData = response.data.data && response.data.data.length > 0
      ? response.data.data[0]
      : null

    res.json(sleepData)
  } catch (error) {
    console.error('Oura sleep API error:', error.response?.data || error.message)
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch sleep data',
      details: error.response?.data || error.message
    })
  }
})

app.get('/api/oura/activity', async (req, res) => {
  try {
    const { token, date } = req.query

    if (!token) {
      return res.status(400).json({ error: 'Token required' })
    }

    const response = await axios.get('https://api.ouraring.com/v2/usercollection/daily_activity', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        start_date: date,
        end_date: date
      }
    })

    const activityData = response.data.data && response.data.data.length > 0
      ? response.data.data[0]
      : null

    res.json(activityData)
  } catch (error) {
    console.error('Oura activity API error:', error.response?.data || error.message)
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch activity data',
      details: error.response?.data || error.message
    })
  }
})

app.get('/api/oura/readiness', async (req, res) => {
  try {
    const { token, date } = req.query

    if (!token) {
      return res.status(400).json({ error: 'Token required' })
    }

    const response = await axios.get('https://api.ouraring.com/v2/usercollection/daily_readiness', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        start_date: date,
        end_date: date
      }
    })

    const readinessData = response.data.data && response.data.data.length > 0
      ? response.data.data[0]
      : null

    res.json(readinessData)
  } catch (error) {
    console.error('Oura readiness API error:', error.response?.data || error.message)
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch readiness data',
      details: error.response?.data || error.message
    })
  }
})

// Oura sync endpoint - sync multiple dates at once
app.post('/api/oura/sync', async (req, res) => {
  try {
    const { token, startDate, endDate } = req.body

    if (!token) {
      return res.status(400).json({ error: 'Token required' })
    }

    if (!startDate || !endDate) {
      return res.status(400).json({ error: 'Start date and end date required' })
    }

    const ouraData = await syncOuraDataRange(token, startDate, endDate)

    res.json({
      success: true,
      data: ouraData,
      count: ouraData.length
    })
  } catch (error) {
    console.error('Oura sync error:', error.message)
    res.status(500).json({
      success: false,
      error: 'Failed to sync Oura data',
      details: error.message
    })
  }
})

// Google Fit OAuth - get authorization URL
app.get('/api/googlefit/auth', (req, res) => {
  try {
    const authUrl = getAuthUrl()
    res.json({ authUrl })
  } catch (error) {
    console.error('Google Fit auth URL error:', error)
    res.status(500).json({ error: 'Failed to generate auth URL' })
  }
})

// Google Fit OAuth - handle callback and exchange code for tokens
app.get('/api/googlefit/callback', async (req, res) => {
  try {
    const { code } = req.query

    if (!code) {
      return res.status(400).json({ error: 'Authorization code required' })
    }

    const tokens = await exchangeCodeForTokens(code)

    // Return tokens to client (client will store encrypted in Firestore)
    res.json({
      success: true,
      tokens: tokens
    })
  } catch (error) {
    console.error('Google Fit token exchange error:', error)
    res.status(500).json({
      success: false,
      error: 'Failed to exchange authorization code',
      details: error.message
    })
  }
})

// Google Fit - sync weight data
app.post('/api/googlefit/sync-weight', async (req, res) => {
  try {
    const { accessToken, startDate, endDate } = req.body

    if (!accessToken) {
      return res.status(400).json({ error: 'Access token required' })
    }

    if (!startDate || !endDate) {
      return res.status(400).json({ error: 'Start date and end date required' })
    }

    const weightData = await fetchWeightData(accessToken, startDate, endDate)

    res.json({
      success: true,
      data: weightData,
      count: weightData.length
    })
  } catch (error) {
    console.error('Google Fit weight sync error:', error.message)
    res.status(500).json({
      success: false,
      error: 'Failed to sync weight data',
      details: error.message
    })
  }
})

// Google Fit - sync activity data
app.post('/api/googlefit/sync-activity', async (req, res) => {
  try {
    const { accessToken, startDate, endDate } = req.body

    if (!accessToken) {
      return res.status(400).json({ error: 'Access token required' })
    }

    if (!startDate || !endDate) {
      return res.status(400).json({ error: 'Start date and end date required' })
    }

    const activityData = await fetchActivityData(accessToken, startDate, endDate)

    res.json({
      success: true,
      data: activityData,
      count: activityData.length
    })
  } catch (error) {
    console.error('Google Fit activity sync error:', error.message)
    res.status(500).json({
      success: false,
      error: 'Failed to sync activity data',
      details: error.message
    })
  }
})

// Workout import endpoint
app.post('/api/workouts/import', upload.single('file'), importWorkoutsFromExcel)

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Life Logger API is running' })
})

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
