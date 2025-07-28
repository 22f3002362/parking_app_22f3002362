<template>
  <div class="user-reports-container">
    <!-- User Navbar -->
    <nav class="user-navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <div class="brand-logo">
            <img src="../assets/P.png" alt="ParkEase Logo" class="logo-img">
            <div class="brand-text">
              <h1>ParkEase</h1>
              <p>Smart Parking Solutions</p>
            </div>
          </div>
        </div>
        
        <!-- Desktop Menu -->
        <div class="navbar-menu desktop-menu">
          <div class="nav-links">
            <router-link to="/user-dashboard" class="nav-link">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/find-parking" class="nav-link">
              <i class="bi bi-search"></i>
              <span>Find Parking</span>
            </router-link>
            <router-link to="/my-bookings" class="nav-link">
              <i class="bi bi-calendar-check"></i>
              <span>My Bookings</span>
            </router-link>
            <router-link to="/user-reports" class="nav-link active">
              <i class="bi bi-graph-up"></i>
              <span>Reports</span>
            </router-link>
          </div>
          
          <div class="navbar-actions">
            <div class="user-profile">
              <div class="user-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
              <div class="user-info">
                <span class="user-name">{{ currentUser?.username || 'User' }}</span>
                <span class="user-role">User</span>
              </div>
            </div>
            <button @click="handleLogout" class="logout-btn">
              <i class="bi bi-box-arrow-right"></i>
              <span>Logout</span>
            </button>
          </div>
        </div>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle" @click="toggleMobileMenu">
          <i class="bi bi-list"></i>
        </button>
      </div>

      <!-- Mobile Menu Dropdown -->
      <div class="mobile-menu" :class="{ 'active': isMobileMenuOpen }">
        <div class="mobile-nav-section">
          <div class="mobile-nav-header">
            <i class="bi bi-list"></i>
            <span>Navigation</span>
          </div>
          <div class="mobile-nav-links">
            <router-link to="/user-dashboard" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/find-parking" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-search"></i>
              <span>Find Parking</span>
            </router-link>
            <router-link to="/my-bookings" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-calendar-check"></i>
              <span>My Bookings</span>
            </router-link>
            <router-link to="/user-reports" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-graph-up"></i>
              <span>Reports</span>
            </router-link>
          </div>
        </div>

        <div class="mobile-user-section">
          <div class="mobile-user-profile">
            <div class="mobile-user-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <div class="mobile-user-info">
              <span class="mobile-user-name">{{ currentUser?.username || 'User' }}</span>
              <span class="mobile-user-role">User</span>
            </div>
          </div>
          <button @click="handleLogout" class="mobile-logout-btn">
            <i class="bi bi-box-arrow-right"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Animated Background -->
    <div class="bg-animation"></div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">My Parking Reports</h1>
        </div>
      </div>

      <!-- Statistics Overview Section -->
      <div class="section-container stats-section" v-if="reportsData && !loading.charts">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-speedometer2"></i>
              My Parking Statistics
            </h2>
            <p class="section-subtitle">Overview of your parking activity and spending</p>
          </div>
          <button @click="fetchReportsData" class="cta-button secondary refresh-btn" :disabled="loading.charts">
            <i class="bi bi-arrow-clockwise"></i>
            <span>Refresh Data</span>
          </button>
        </div>

        <div class="stats-grid">
          <!-- Total Spent -->
          <div class="stat-card spending-card">
            <div class="stat-icon">
              <i class="bi bi-currency-rupee"></i>
            </div>
            <div class="stat-content">
              <h3>Total Spent</h3>
              <p class="stat-value">₹{{ safeStats.totalSpent.toLocaleString() }}</p>
              <span class="stat-label">All-time parking expenses</span>
            </div>
          </div>

          <!-- Total Bookings -->
          <div class="stat-card bookings-card">
            <div class="stat-icon">
              <i class="bi bi-calendar-check"></i>
            </div>
            <div class="stat-content">
              <h3>Total Bookings</h3>
              <p class="stat-value">{{ safeStats.totalBookings.toLocaleString() }}</p>
              <span class="stat-label">{{ safeStats.activeBookings }} currently active</span>
            </div>
          </div>

          <!-- Total Hours Parked -->
          <div class="stat-card hours-card">
            <div class="stat-icon">
              <i class="bi bi-clock"></i>
            </div>
            <div class="stat-content">
              <h3>Hours Parked</h3>
              <p class="stat-value">{{ safeStats.totalHours.toLocaleString() }}h</p>
              <span class="stat-label">Average {{ safeStats.avgHoursPerBooking }}h per booking</span>
            </div>
          </div>

          <!-- Favorite Location -->
          <div class="stat-card location-card">
            <div class="stat-icon">
              <i class="bi bi-geo-alt-fill"></i>
            </div>
            <div class="stat-content">
              <h3>Favorite Location</h3>
              <p class="stat-value">{{ safeStats.favoriteLocation || 'N/A' }}</p>
              <span class="stat-label">{{ safeStats.favoriteLocationCount }} visits</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State for Statistics -->
      <div v-if="loading.charts" class="section-container loading-section">
        <div class="loading-content">
          <div class="loading-spinner"></div>
          <p>Loading your parking reports...</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="section-container chart-section" v-if="reportsData && !loading.charts">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-bar-chart-line-fill"></i>
              Visual Insights
            </h2>
            <p class="section-subtitle">Your parking patterns and spending trends</p>
          </div>
        </div>

        <div class="charts-grid">
          <!-- Monthly Spending Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Monthly Spending Trend</h3>
            <Line
              :data="monthlySpendingData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Your parking expenses over the last 12 months.
            </p>
          </div>

          <!-- Booking Frequency Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Booking Frequency</h3>
            <Bar
              :data="bookingFrequencyData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Number of parking sessions per month.
            </p>
          </div>

          <!-- Favorite Locations Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Favorite Parking Locations</h3>
            <Doughnut
              :data="favoriteLocationsData"
              :options="pieChartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Distribution of your parking sessions by location.
            </p>
          </div>

          <!-- Daily Usage Pattern -->
          <div class="chart-card">
            <h3 class="chart-title">Daily Usage Pattern</h3>
            <Bar
              :data="dailyUsageData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Your parking usage by day of the week.
            </p>
          </div>

          <!-- Hourly Usage Pattern -->
          <div class="chart-card">
            <h3 class="chart-title">Hourly Usage Pattern</h3>
            <Line
              :data="hourlyUsageData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Your preferred parking times throughout the day.
            </p>
          </div>

          <!-- Duration Analysis -->
          <div class="chart-card">
            <h3 class="chart-title">Parking Duration Analysis</h3>
            <Bar
              :data="durationAnalysisData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Distribution of your parking session durations.
            </p>
          </div>
        </div>
      </div>

      <!-- Export Section -->
      <div class="section-container export-section" v-if="!loading.charts">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-file-earmark-arrow-down"></i>
              Export My Data
            </h2>
            <p class="section-subtitle">Download your parking history and reports</p>
          </div>
        </div>

        <div class="export-grid">
          <div class="export-card">
            <div class="export-icon">
              <i class="bi bi-file-earmark-spreadsheet"></i>
            </div>
            <h3>Booking History</h3>
            <p>Download complete history of your parking bookings</p>
            <button @click="exportBookingHistory" class="export-btn">
              <i class="bi bi-download"></i>
              Export CSV
            </button>
          </div>

          <div class="export-card">
            <div class="export-icon">
              <i class="bi bi-file-earmark-pdf"></i>
            </div>
            <h3>Monthly Summary</h3>
            <p>Generate PDF summary of your monthly parking activity</p>
            <button @click="exportMonthlySummary" class="export-btn">
              <i class="bi bi-download"></i>
              Export PDF
            </button>
          </div>

          <div class="export-card">
            <div class="export-icon">
              <i class="bi bi-receipt"></i>
            </div>
            <h3>Payment Receipts</h3>
            <p>Download all your parking payment receipts</p>
            <button @click="exportPaymentReceipts" class="export-btn">
              <i class="bi bi-download"></i>
              Export ZIP
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

// Chart.js imports
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  ArcElement
} from 'chart.js'
import { Bar, Line, Doughnut } from 'vue-chartjs'

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  ArcElement
)

const router = useRouter()

// Reactive state
const currentUser = ref({ username: 'User' })
const isMobileMenuOpen = ref(false)
const reportsData = ref(null)
const loading = ref({
  charts: true
})

// Chart data
const monthlySpendingData = ref({})
const bookingFrequencyData = ref({})
const favoriteLocationsData = ref({})
const dailyUsageData = ref({})
const hourlyUsageData = ref({})
const durationAnalysisData = ref({})

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#ffffff',
        font: {
          family: 'Poppins',
          size: 12
        }
      }
    }
  },
  scales: {
    x: {
      ticks: {
        color: '#ffffff',
        font: {
          family: 'Poppins',
          size: 11
        }
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      }
    },
    y: {
      ticks: {
        color: '#ffffff',
        font: {
          family: 'Poppins',
          size: 11
        }
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      }
    }
  }
}

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#ffffff',
        font: {
          family: 'Poppins',
          size: 12
        },
        padding: 20
      }
    }
  }
}

// Computed properties
const safeStats = computed(() => {
  if (!reportsData.value) {
    return {
      totalSpent: 0,
      totalBookings: 0,
      activeBookings: 0,
      totalHours: 0,
      avgHoursPerBooking: 0,
      favoriteLocation: 'N/A',
      favoriteLocationCount: 0
    }
  }
  return reportsData.value.stats
})

// Methods
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('role')
  router.push('/login')
}

const fetchReportsData = async () => {
  loading.value.charts = true
  try {
    console.log('Fetching user reports data...')
    
    // Call the user-specific reports API
    const response = await api.getUserReportsData()
    console.log('User reports API response:', response)
    
    if (response.status === 'success' && response.data) {
      reportsData.value = response.data
      setupChartData(response.data)
      console.log('User reports data loaded successfully:', reportsData.value)
    } else {
      console.error('Invalid response format:', response)
      // Use fallback empty data
      reportsData.value = createEmptyData()
      setupChartData(reportsData.value)
    }
    
  } catch (error) {
    console.error('Error fetching user reports data:', error)
    
    // Show user-friendly error message
    if (error.response?.status === 403) {
      console.error('Access denied - user not authorized')
    } else if (error.response?.status === 404) {
      console.error('User not found')
    } else {
      console.error('Network or server error:', error.message)
    }
    
    // Use fallback empty data on error
    reportsData.value = createEmptyData()
    setupChartData(reportsData.value)
    
  } finally {
    loading.value.charts = false
  }
}

const createEmptyData = () => {
  return {
    stats: {
      totalSpent: 0,
      totalBookings: 0,
      activeBookings: 0,
      totalHours: 0,
      avgHoursPerBooking: 0,
      favoriteLocation: 'No bookings yet',
      favoriteLocationCount: 0
    },
    monthlySpending: Array.from({length: 12}, (_, i) => {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      return { month: months[i], amount: 0 }
    }),
    bookingFrequency: Array.from({length: 12}, (_, i) => {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      return { month: months[i], bookings: 0 }
    }),
    favoriteLocations: [
      { name: 'No data', count: 0 }
    ],
    dailyUsage: [
      { day: 'Monday', sessions: 0 },
      { day: 'Tuesday', sessions: 0 },
      { day: 'Wednesday', sessions: 0 },
      { day: 'Thursday', sessions: 0 },
      { day: 'Friday', sessions: 0 },
      { day: 'Saturday', sessions: 0 },
      { day: 'Sunday', sessions: 0 }
    ],
    hourlyUsage: Array.from({length: 18}, (_, i) => {
      const hour = i + 6 // Start from 6 AM
      const hour12 = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
      const ampm = hour >= 12 ? 'PM' : 'AM'
      return { hour: `${hour12} ${ampm}`, sessions: 0 }
    }),
    durationAnalysis: [
      { duration: '< 1 hour', count: 0 },
      { duration: '1-2 hours', count: 0 },
      { duration: '2-4 hours', count: 0 },
      { duration: '4-6 hours', count: 0 },
      { duration: '6-8 hours', count: 0 },
      { duration: '> 8 hours', count: 0 }
    ]
  }
}

const setupChartData = (data) => {
  // Monthly Spending Chart
  monthlySpendingData.value = {
    labels: data.monthlySpending.map(item => item.month),
    datasets: [{
      label: 'Amount Spent (₹)',
      data: data.monthlySpending.map(item => item.amount),
      backgroundColor: 'rgba(0, 168, 232, 0.2)',
      borderColor: '#00a8e8',
      borderWidth: 2,
      tension: 0.4
    }]
  }

  // Booking Frequency Chart
  bookingFrequencyData.value = {
    labels: data.bookingFrequency.map(item => item.month),
    datasets: [{
      label: 'Number of Bookings',
      data: data.bookingFrequency.map(item => item.bookings),
      backgroundColor: 'rgba(0, 168, 232, 0.6)',
      borderColor: '#00a8e8',
      borderWidth: 1
    }]
  }

  // Favorite Locations Chart
  favoriteLocationsData.value = {
    labels: data.favoriteLocations.map(item => item.name),
    datasets: [{
      data: data.favoriteLocations.map(item => item.count),
      backgroundColor: [
        '#00a8e8',
        '#0077be',
        '#005fa3',
        '#004788',
        '#003066'
      ],
      borderColor: '#ffffff',
      borderWidth: 2
    }]
  }

  // Daily Usage Chart
  dailyUsageData.value = {
    labels: data.dailyUsage.map(item => item.day),
    datasets: [{
      label: 'Parking Sessions',
      data: data.dailyUsage.map(item => item.sessions),
      backgroundColor: 'rgba(0, 168, 232, 0.6)',
      borderColor: '#00a8e8',
      borderWidth: 1
    }]
  }

  // Hourly Usage Chart
  hourlyUsageData.value = {
    labels: data.hourlyUsage.map(item => item.hour),
    datasets: [{
      label: 'Sessions',
      data: data.hourlyUsage.map(item => item.sessions),
      backgroundColor: 'rgba(0, 168, 232, 0.2)',
      borderColor: '#00a8e8',
      borderWidth: 2,
      tension: 0.4
    }]
  }

  // Duration Analysis Chart
  durationAnalysisData.value = {
    labels: data.durationAnalysis.map(item => item.duration),
    datasets: [{
      label: 'Number of Sessions',
      data: data.durationAnalysis.map(item => item.count),
      backgroundColor: 'rgba(0, 168, 232, 0.6)',
      borderColor: '#00a8e8',
      borderWidth: 1
    }]
  }
}

const exportBookingHistory = async () => {
    try {
        console.log('Exporting booking history...')
        
        // Show loading state
        const exportBtn = event?.target
        if (exportBtn) {
            exportBtn.disabled = true
            exportBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Exporting...'
        }
        
        // Fetch booking history from API
        const response = await api.getUserBookingHistory()
        
        if (response.status === 'success' && response.data) {
            const bookings = response.data
            
            // Create CSV header
            const csvHeader = 'Booking ID,Date,Location,Start Time,End Time,Duration (Hours),Amount (₹),Status,Vehicle Number\n'
            
            // Convert booking data to CSV rows
            const csvRows = bookings.map(booking => {
                const startDate = new Date(booking.start_time).toLocaleDateString()
                const startTime = new Date(booking.start_time).toLocaleTimeString()
                const endTime = booking.end_time ? new Date(booking.end_time).toLocaleTimeString() : 'Ongoing'
                const duration = booking.duration_hours || 'N/A'
                const amount = booking.total_amount || 0
                const location = booking.parking_space?.name || 'Unknown Location'
                const status = booking.status || 'Unknown'
                const vehicleNumber = booking.vehicle_number || 'N/A'
                
                return `${booking.id},"${startDate}","${location}","${startTime}","${endTime}","${duration}","${amount}","${status}","${vehicleNumber}"`
            }).join('\n')
            
            // Combine header and rows
            const csvData = csvHeader + csvRows
            
            // Create and download file
            const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `parking-history-${new Date().toISOString().split('T')[0]}.csv`
            a.click()
            window.URL.revokeObjectURL(url)
            
            console.log('Booking history exported successfully')
            
        } else {
            throw new Error('Failed to fetch booking history')
        }
        
    } catch (error) {
        console.error('Error exporting booking history:', error)
        alert('Failed to export booking history. Please try again.')
    } finally {
        // Reset button state
        const exportBtn = event?.target
        if (exportBtn) {
            exportBtn.disabled = false
            exportBtn.innerHTML = '<i class="bi bi-download"></i> Export CSV'
        }
    }
}

const exportMonthlySummary = async () => {
    try {
        console.log('Exporting monthly summary...')
        
        // Show loading state
        const exportBtn = event?.target
        if (exportBtn) {
            exportBtn.disabled = true
            exportBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Generating PDF...'
        }
        
        // Get current date for filename
        const currentDate = new Date()
        const monthYear = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
        
        // Fetch user's monthly data
        const response = await api.getUserReportsData()
        
        if (response.status === 'success' && response.data) {
            const data = response.data
            
            // Create HTML content for PDF
            const htmlContent = `
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            margin: 20px; 
                            color: #333;
                            line-height: 1.6;
                        }
                        .header { 
                            text-align: center; 
                            margin-bottom: 30px; 
                            border-bottom: 2px solid #00a8e8;
                            padding-bottom: 20px;
                        }
                        .header h1 { 
                            color: #00a8e8; 
                            margin: 0;
                            font-size: 28px;
                        }
                        .header p { 
                            margin: 5px 0; 
                            color: #666;
                            font-size: 14px;
                        }
                        .summary-section { 
                            margin: 30px 0; 
                            background: #f9f9f9;
                            padding: 20px;
                            border-radius: 8px;
                            border-left: 4px solid #00a8e8;
                        }
                        .summary-section h2 { 
                            color: #00a8e8; 
                            margin-top: 0;
                            font-size: 20px;
                        }
                        .stats-grid { 
                            display: grid; 
                            grid-template-columns: repeat(2, 1fr); 
                            gap: 20px; 
                            margin: 20px 0;
                        }
                        .stat-box { 
                            background: white; 
                            padding: 15px; 
                            border-radius: 8px; 
                            border: 1px solid #ddd;
                            text-align: center;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .stat-box h3 { 
                            margin: 0 0 10px 0; 
                            color: #333;
                            font-size: 14px;
                        }
                        .stat-box .value { 
                            font-size: 24px; 
                            font-weight: bold; 
                            color: #00a8e8;
                            margin: 0;
                        }
                        .monthly-data { 
                            margin: 20px 0;
                        }
                        .monthly-data table { 
                            width: 100%; 
                            border-collapse: collapse;
                            background: white;
                            border-radius: 8px;
                            overflow: hidden;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .monthly-data th, .monthly-data td { 
                            padding: 12px; 
                            text-align: left; 
                            border-bottom: 1px solid #ddd;
                        }
                        .monthly-data th { 
                            background: #00a8e8; 
                            color: white;
                            font-weight: bold;
                        }
                        .monthly-data tr:hover { 
                            background: #f5f5f5;
                        }
                        .footer { 
                            margin-top: 40px; 
                            text-align: center; 
                            color: #666;
                            font-size: 12px;
                            border-top: 1px solid #ddd;
                            padding-top: 20px;
                        }
                        .insights {
                            background: #e8f4fd;
                            padding: 15px;
                            border-radius: 8px;
                            margin: 20px 0;
                            border-left: 4px solid #00a8e8;
                        }
                        .insights h3 {
                            color: #00a8e8;
                            margin-top: 0;
                        }
                        .insights ul {
                            margin: 10px 0;
                            padding-left: 20px;
                        }
                        .insights li {
                            margin: 5px 0;
                            color: #555;
                        }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>🅿️ ParkEase - Monthly Summary</h1>
                        <p>Parking Activity Report for ${monthYear}</p>
                        <p>Generated on: ${new Date().toLocaleDateString()}</p>
                        <p>User: ${currentUser.value?.username || 'User'}</p>
                    </div>

                    <div class="summary-section">
                        <h2>📊 Monthly Overview</h2>
                        <div class="stats-grid">
                            <div class="stat-box">
                                <h3>Total Spent This Month</h3>
                                <p class="value">₹${data.stats.totalSpent.toLocaleString()}</p>
                            </div>
                            <div class="stat-box">
                                <h3>Total Bookings</h3>
                                <p class="value">${data.stats.totalBookings}</p>
                            </div>
                            <div class="stat-box">
                                <h3>Total Hours Parked</h3>
                                <p class="value">${data.stats.totalHours}h</p>
                            </div>
                            <div class="stat-box">
                                <h3>Average Session</h3>
                                <p class="value">${data.stats.avgHoursPerBooking}h</p>
                            </div>
                        </div>
                    </div>

                    <div class="summary-section">
                        <h2>📅 Monthly Spending Breakdown</h2>
                        <div class="monthly-data">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Month</th>
                                        <th>Amount Spent (₹)</th>
                                        <th>Number of Bookings</th>
                                        <th>Average per Booking (₹)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.monthlySpending.map((month, index) => {
                                        const bookings = data.bookingFrequency[index]?.bookings || 0;
                                        const avgPerBooking = bookings > 0 ? (month.amount / bookings).toFixed(2) : '0.00';
                                        return `
                                            <tr>
                                                <td>${month.month}</td>
                                                <td>₹${month.amount.toLocaleString()}</td>
                                                <td>${bookings}</td>
                                                <td>₹${avgPerBooking}</td>
                                            </tr>
                                        `;
                                    }).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="summary-section">
                        <h2>🏢 Favorite Parking Locations</h2>
                        <div class="monthly-data">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Location</th>
                                        <th>Number of Visits</th>
                                        <th>Percentage</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.favoriteLocations.map(location => {
                                        const total = data.favoriteLocations.reduce((sum, loc) => sum + loc.count, 0);
                                        const percentage = total > 0 ? ((location.count / total) * 100).toFixed(1) : '0.0';
                                        return `
                                            <tr>
                                                <td>${location.name}</td>
                                                <td>${location.count}</td>
                                                <td>${percentage}%</td>
                                            </tr>
                                        `;
                                    }).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="insights">
                        <h3>💡 Insights & Recommendations</h3>
                        <ul>
                            <li><strong>Most Active Day:</strong> ${data.dailyUsage.reduce((max, day) => day.sessions > max.sessions ? day : max, data.dailyUsage[0])?.day || 'N/A'}</li>
                            <li><strong>Preferred Parking Time:</strong> ${data.hourlyUsage.reduce((max, hour) => hour.sessions > max.sessions ? hour : max, data.hourlyUsage[0])?.hour || 'N/A'}</li>
                            <li><strong>Average Session Duration:</strong> ${data.stats.avgHoursPerBooking} hours</li>
                            <li><strong>Most Used Location:</strong> ${data.stats.favoriteLocation} (${data.stats.favoriteLocationCount} visits)</li>
                            ${data.stats.totalSpent > 0 ? `<li><strong>Monthly Average Spending:</strong> ₹${(data.stats.totalSpent / 12).toFixed(2)}</li>` : ''}
                        </ul>
                    </div>

                    <div class="footer">
                        <p>This report was automatically generated by ParkEase</p>
                        <p>For questions or support, contact us at support@parkease.com</p>
                        <p>© 2024 ParkEase. All rights reserved.</p>
                    </div>
                </body>
                </html>
            `;
            
            // Create a new window for printing
            const printWindow = window.open('', '_blank');
            printWindow.document.write(htmlContent);
            printWindow.document.close();
            
            // Wait for content to load then trigger print
            printWindow.onload = () => {
                setTimeout(() => {
                    printWindow.print();
                    printWindow.close();
                }, 500);
            };
            
            console.log('Monthly summary generated successfully')
            
        } else {
            throw new Error('Failed to fetch user data for summary')
        }
        
    } catch (error) {
        console.error('Error generating monthly summary:', error)
        alert('Failed to generate monthly summary. Please try again.')
    } finally {
        // Reset button state
        const exportBtn = event?.target
        if (exportBtn) {
            exportBtn.disabled = false
            exportBtn.innerHTML = '<i class="bi bi-download"></i> Export PDF'
        }
    }
}

const exportPaymentReceipts = () => {
  console.log('Exporting payment receipts...')
  alert('Payment receipts export feature coming soon!')
}

// Lifecycle
onMounted(() => {
  const username = localStorage.getItem('username') || 'User'
  currentUser.value = { username }
  fetchReportsData()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.user-reports-container {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* User Navbar */
.user-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(26, 45, 67, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0;
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-logo .logo-img {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.brand-text h1 {
  color: white;
  font-size: 1.7rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.brand-text p {
  color: #00a8e8;
  font-size: 0.8rem;
  margin: 0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 30px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.active {
  color: white;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-link i {
  font-size: 1.1rem;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
}

.user-avatar i {
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.9);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.user-role {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

/* Mobile Menu */
.mobile-menu-toggle {
  display: none;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.mobile-menu-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
}

.mobile-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 999;
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.3s ease;
}

.mobile-menu.active {
  display: block;
  opacity: 1;
  transform: translateY(0);
}

.mobile-nav-section {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-nav-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #00a8e8;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.mobile-nav-header i {
  font-size: 1.1rem;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.02);
}

.mobile-nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.mobile-nav-link.router-link-active {
  color: white;
  background: rgba(0, 168, 232, 0.2);
  border-left: 3px solid #00a8e8;
}

.mobile-nav-link i {
  font-size: 1.2rem;
  width: 20px;
  text-align: center;
}

.mobile-user-section {
  padding: 1.5rem;
}

.mobile-user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.mobile-user-avatar i {
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.mobile-user-info {
  display: flex;
  flex-direction: column;
}

.mobile-user-name {
  font-weight: 600;
  font-size: 1.1rem;
  color: white;
}

.mobile-user-role {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

.mobile-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.mobile-logout-btn:hover {
  background: linear-gradient(135deg, #ee5a6f, #e53e3e);
  transform: translateY(-2px);
}

/* Animated Background */
.bg-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  background-image: url('/car1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.bg-animation::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1;
}

/* Main Content */
.main-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  min-height: 100vh;
  padding-top: 70px;
  margin: 0 auto;
  max-width: 1400px;
}

/* Hero Section */
.hero-section {
  padding: 2rem 0;
  text-align: center;
  background: linear-gradient(135deg, rgba(0,0,0,0.3) 0%, rgba(26,45,67,0.6) 100%);
  border-radius: 25px;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
  margin-bottom: 0.5rem;
}

.main-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #00a8e8, #ffffff);
  margin: 1rem auto;
}

/* Section Container */
.section-container {
  backdrop-filter: blur(20px);
  border-radius: 25px;
  padding: 2.5rem;
  margin-bottom: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.section-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #00a8e8, #0077be, #00a8e8);
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: -200% 0; }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-title-area {
  flex: 1;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-title i {
  color: #00a8e8;
  font-size: 1.8rem;
}

.section-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0.5rem 0 0 0;
  font-weight: 400;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: slideUpFade 0.6s ease-out forwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }
@keyframes slideUpFade {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.stat-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.08);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.stat-icon {
  font-size: 2.5rem;
  color: #00a8e8;
  background: rgba(0, 168, 232, 0.1);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.stat-icon i {
  font-size: 1.5rem;
  color: #00a8e8;
}

.stat-content h3 {
  font-size: 1.1rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: #00a8e8;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 400;
}

/* Loading State */
.loading-section {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 168, 232, 0.3);
  border-top: 4px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  height: 400px; /* Fixed height to prevent expansion */
  overflow: hidden; /* Prevent overflow */
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 30px rgba(0, 168, 232, 0.15);
  border-color: rgba(0, 168, 232, 0.3);
}

.chart-title {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-canvas {
  height: 280px !important; /* Fixed height with !important */
  width: 100% !important;
  max-height: 280px; /* Maximum height constraint */
  margin-bottom: 1rem;
}

.chart-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  font-style: italic;
  margin-top: 0.5rem;
}

/* Export Section */
.export-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.export-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.export-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 30px rgba(0, 168, 232, 0.15);
  border-color: rgba(0, 168, 232, 0.3);
}

.export-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  box-shadow: 0 8px 20px rgba(0, 168, 232, 0.3);
}

.export-icon i {
  font-size: 1.5rem;
  color: #ffffff;
}

.export-card h3 {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.export-card p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.export-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.export-btn:hover {
  background: linear-gradient(135deg, #005fa3, #0094d1);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 232, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 1rem;
    height: 70px;
  }
  
  /* Hide brand text on mobile, show only logo */
  .brand-text {
    display: none;
  }
  
  /* Hide desktop menu */
  .desktop-menu {
    display: none;
  }
  
  /* Show mobile menu toggle */
  .mobile-menu-toggle {
    display: flex;
  }
  
  /* Mobile menu becomes visible */
  .mobile-menu {
    display: none;
  }
  
  .mobile-menu.active {
    display: block;
  }
  
  .main-content {
    padding: 1rem;
    padding-top: 80px;
  }
  
  .main-title {
    font-size: 2.2rem;
  }
  
  .hero-section {
    padding: 2rem 0;
  }
  
  .section-container {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .chart-card {
    padding: 1.5rem;
    height: 350px; /* Smaller height for mobile */
  }
  
  .chart-canvas {
    height: 220px !important; /* Smaller chart for mobile */
    max-height: 220px;
  }
  
  .export-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 480px) {
  .brand-text h1 {
    font-size: 1.4rem;
  }
  
  .brand-text p {
    display: none;
  }
  
  .main-content {
    padding: 0.75rem;
    padding-top: 80px;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .hero-section {
    padding: 1.5rem 0;
  }
  
  .section-container {
    padding: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .section-title {
    font-size: 1.4rem;
  }
  
  .section-subtitle {
    font-size: 0.9rem;
  }
  
  .stat-card {
    padding: 1.5rem;
  }
  
  .chart-card {
    padding: 1rem;
    height: 320px; /* Even smaller for very small screens */
  }
  
  .chart-canvas {
    height: 200px !important;
    max-height: 200px;
  }
  
  .export-card {
    padding: 1.5rem;
  }
}
</style>
