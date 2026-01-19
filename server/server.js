import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import axios from 'axios'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 5000

app.use(cors())
app.use(express.json())

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

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Life Logger API is running' })
})

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
