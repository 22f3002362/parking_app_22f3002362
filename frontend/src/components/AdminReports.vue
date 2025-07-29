// frontend/src/views/ReportsView.vue
<template>
  <div class="reports-container">
    <!-- Admin Navbar (You might want to pass current user or fetch it here) -->
    <nav class="admin-navbar">
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
        
        <div class="navbar-menu desktop-menu">
          <div class="nav-links">
            <router-link to="/admin-dashboard" class="nav-link">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/parking-lots" class="nav-link">
              <i class="bi bi-geo-alt-fill"></i>
              <span>Parking Lots</span>
            </router-link>
            <router-link to="/manage-users" class="nav-link">
              <i class="bi bi-people-fill"></i>
              <span>Users</span>
            </router-link>
            <router-link to="/admin-reports" class="nav-link active">
              <i class="bi bi-graph-up"></i>
              <span>Reports</span>
            </router-link>
          </div>
          
          <div class="navbar-actions">
            <div class="admin-profile">
              <div class="admin-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
              <div class="admin-info">
                <span class="admin-name">{{ currentUser?.username || 'Admin' }}</span>
                <span class="admin-role">Administrator</span>
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
            <router-link to="/admin-dashboard" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/parking-lots" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-geo-alt-fill"></i>
              <span>Parking Lots</span>
            </router-link>
            <router-link to="/manage-users" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-people-fill"></i>
              <span>Users</span>
            </router-link>
            <router-link to="/admin-reports" class="mobile-nav-link" @click="closeMobileMenu">
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
              <span class="mobile-user-name">{{ currentUser?.username || 'Admin' }}</span>
              <span class="mobile-user-role">Administrator</span>
            </div>
          </div>
          <button @click="handleLogout" class="mobile-logout-btn">
            <i class="bi bi-box-arrow-right"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>

    <div class="bg-animation"></div>

    <div class="main-content">
      <!-- Hero Section for Reports -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">Reports & Analytics</h1>
        </div>
      </div>

      <!-- Statistics Overview Section -->
      <div class="section-container stats-section" v-if="reportsData && !loading.charts">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-speedometer2"></i>
              Key Statistics
            </h2>
            <p class="section-subtitle">Overview of parking system performance</p>
          </div>
          <button @click="fetchChartData" class="cta-button secondary refresh-btn" :disabled="loading.charts">
            <i class="bi bi-arrow-clockwise"></i>
            <span>Refresh Data</span>
          </button>
        </div>

        <div class="stats-grid">
          <!-- Total Revenue -->
          <div class="stat-card revenue-card">
            <div class="stat-icon">
              <i class="bi bi-currency-rupee"></i>
            </div>
            <div class="stat-content">
              <h3>Total Revenue</h3>
              <p class="stat-value">₹{{ safeStats.revenue.toLocaleString() }}</p>
              <span class="stat-label">All-time earnings</span>
            </div>
          </div>

          <!-- Total Reservations -->
          <div class="stat-card reservations-card">
            <div class="stat-icon">
              <i class="bi bi-calendar-check"></i>
            </div>
            <div class="stat-content">
              <h3>Total Reservations</h3>
              <p class="stat-value">{{ safeStats.reservations.toLocaleString() }}</p>
              <span class="stat-label">{{ safeStats.activeReservations }} currently active</span>
            </div>
          </div>

          <!-- Total Users -->
          <div class="stat-card users-card">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <h3>Total Users</h3>
              <p class="stat-value">{{ safeStats.users.toLocaleString() }}</p>
              <span class="stat-label">{{ safeStats.regularUsers }} regular users</span>
            </div>
          </div>

          <!-- Occupancy Rate -->
          <div class="stat-card occupancy-card">
            <div class="stat-icon">
              <i class="bi bi-pie-chart"></i>
            </div>
            <div class="stat-content">
              <h3>Overall Occupancy</h3>
              <p class="stat-value">{{ getOverallOccupancyRate() }}%</p>
              <span class="stat-label">{{ safeStats.occupiedSpots }}/{{ safeStats.totalSpots }} spots occupied</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State for Statistics -->
      <div v-if="loading.charts" class="section-container loading-section">
        <div class="loading-content">
          <div class="loading-spinner"></div>
          <p>Loading reports data...</p>
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
            <p class="section-subtitle">Key performance indicators and trend analysis</p>
          </div>
          <button @click="fetchChartData" class="cta-button secondary refresh-btn" :disabled="loading.charts">
            <i class="bi bi-arrow-clockwise"></i>
            <span>Refresh Charts</span>
          </button>
        </div>

        <div class="charts-grid">
          <!-- Parking Lot Occupancy Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Parking Lot Occupancy</h3>
            <Bar
              :data="parkingLotOccupancyData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Overview of occupied vs. total spots in each parking lot.
            </p>
          </div>

          <!-- Overall Parking Spot Status Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Overall Parking Spot Status</h3>
            <Bar
              :data="overallSpotStatusData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Total available and occupied parking spots across all lots.
            </p>
          </div>

          <!-- Monthly Parking Trends Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Monthly Parking Trends</h3>
            <Line
              :data="monthlyTrendsData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Historical trend of parking spot bookings per month.
            </p>
          </div>

          <!-- User Activity Distribution -->
          <div class="chart-card">
            <h3 class="chart-title">User Role Distribution</h3>
            <Doughnut
              :data="userRoleDistributionData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Distribution of different user roles in the system.
            </p>
          </div>

          <!-- Daily Revenue Line Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Daily Revenue Trends</h3>
            <Line
              :data="dailyRevenueData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Daily revenue trends over the last 30 days.
            </p>
          </div>

          <!-- Monthly Revenue Line Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Monthly Revenue Trends</h3>
            <Line
              :data="monthlyRevenueData"
              :options="chartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Monthly revenue trends for the current year.
            </p>
          </div>

          <!-- Parking Lot Occupancy Comparison Pie Chart -->
          <div class="chart-card">
            <h3 class="chart-title">Parking Lot Occupancy Comparison</h3>
            <Doughnut
              :data="parkingLotComparisonData"
              :options="pieChartOptions"
              class="chart-canvas"
            />
            <p class="chart-description">
              Comparative occupancy rates across all parking lots.
            </p>
          </div>
        </div>
      </div>

      <!-- Additional Report Sections (e.g., CSV Export, Monthly Report Generation) -->
      <div class="section-container">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-file-earmark-arrow-down-fill"></i>
              Data Export & Reports
            </h2>
            <p class="section-subtitle">Generate and download detailed reports for analysis.</p>
          </div>
        </div>
        <div class="reports-grid">
          <!-- Parking Details Export -->
          <div class="report-card">
            <h3 class="report-card-title">📊 Export Parking Details</h3>
            <p class="report-card-description">Download comprehensive CSV file with all parking reservations, user details, and revenue information.</p>
            <button class="cta-button primary" @click="exportParkingDetails" :disabled="loading.charts">
              <i class="bi bi-download"></i> 
              <span v-if="loading.charts">Generating...</span>
              <span v-else>Export Detailed CSV</span>
            </button>
          </div>
          
          <!-- Monthly Report -->
          <div class="report-card">
            <h3 class="report-card-title">📅 Monthly Summary Report</h3>
            <p class="report-card-description">Generate and download a formatted monthly activity summary with key statistics and revenue breakdown.</p>
            <button class="cta-button primary" @click="generateMonthlyReport" :disabled="loading.charts">
              <i class="bi bi-calendar-check"></i> 
              <span v-if="loading.charts">Generating...</span>
              <span v-else>Generate Report</span>
            </button>
          </div>
          
          <!-- Analytics Summary Export -->
          <div class="report-card">
            <h3 class="report-card-title">📈 Analytics Export</h3>
            <p class="report-card-description">Export current dashboard analytics data including occupancy rates, trends, and performance metrics.</p>
            <button class="cta-button primary" @click="exportAnalyticsSummary" :disabled="loading.charts">
              <i class="bi bi-graph-up-arrow"></i> 
              <span v-if="loading.charts">Generating...</span>
              <span v-else>Export Analytics</span>
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Logout Confirmation Modal (copied from AdminDashboard for consistency) -->
    <div v-if="showLogoutModal" class="modal-overlay" @click="cancelLogout">
      <div class="modal-container logout-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>Confirm Logout</h3>
            <p>Are you sure you want to logout from your account?</p>
          </div>
          <button class="close-btn" @click="cancelLogout">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="logout-modal-content">
          <div class="logout-icon">
            <i class="bi bi-box-arrow-right"></i>
          </div>
          <div class="logout-message">
            <h4>You will be logged out</h4>
            <p>You'll need to sign in again to access the admin dashboard</p>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="cta-button secondary" @click="cancelLogout">
            <i class="bi bi-x-circle"></i>
            Cancel
          </button>
          <button type="button" class="cta-button primary logout-confirm-btn" @click="confirmLogout">
            <i class="bi bi-box-arrow-right"></i>
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import { useToast } from 'vue-toast-notification';
import api from '../services/api';

// Chart.js imports
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'vue-chartjs';

// Register Chart.js components globally
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement
);

const router = useRouter();
const toast = useToast();

// Reactive data for charts
const reportsData = ref(null); // Store all reports data from API
const loading = reactive({ charts: true }); // Loading state for charts
const currentUser = ref(null);
const showLogoutModal = ref(false);
const isMobileMenuOpen = ref(false);

// Chart Data (Reactive for dynamic updates)
const parkingLotOccupancyData = ref({
  labels: [],
  datasets: [
    { label: 'Occupied Spots', backgroundColor: '#ef4444', data: [], borderRadius: 5 },
    { label: 'Available Spots', backgroundColor: '#22c55e', data: [], borderRadius: 5 }
  ]
});

const overallSpotStatusData = ref({
  labels: ['Total Spots'],
  datasets: [
    { label: 'Total Occupied', backgroundColor: '#f97316', data: [], borderRadius: 5 },
    { label: 'Total Available', backgroundColor: '#0ea5e9', data: [], borderRadius: 5 }
  ]
});

const monthlyTrendsData = ref({
  labels: [],
  datasets: [
    {
      label: 'Bookings per Month',
      backgroundColor: 'rgba(102, 126, 234, 0.5)',
      borderColor: '#667eea',
      data: [],
      tension: 0.3,
      fill: true,
    }
  ]
});

const userRoleDistributionData = ref({
  labels: ['Admin', 'Users'],
  datasets: [
    {
      backgroundColor: ['#00a8e8', 'rgba(255, 255, 255, 0.1)'],
      data: [0, 0],
      hoverOffset: 4,
    }
  ]
});

// Daily Revenue Data
const dailyRevenueData = ref({
  labels: [],
  datasets: [
    {
      label: 'Daily Revenue (₹)',
      backgroundColor: 'rgba(34, 197, 94, 0.2)',
      borderColor: '#22c55e',
      data: [],
      tension: 0.4,
      fill: true,
      pointBackgroundColor: '#22c55e',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointRadius: 4,
    }
  ]
});

// Monthly Revenue Data
const monthlyRevenueData = ref({
  labels: [],
  datasets: [
    {
      label: 'Monthly Revenue (₹)',
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: '#3b82f6',
      data: [],
      tension: 0.4,
      fill: true,
      pointBackgroundColor: '#3b82f6',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointRadius: 5,
    }
  ]
});

// Parking Lot Comparison Data (Pie Chart)
const parkingLotComparisonData = ref({
  labels: [],
  datasets: [
    {
      backgroundColor: [
        '#ef4444', '#f97316', '#eab308', '#22c55e', 
        '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'
      ],
      data: [],
      hoverOffset: 8,
      borderWidth: 2,
      borderColor: '#ffffff',
    }
  ]
});

// Chart Options for smooth animations and responsiveness
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1200,
    easing: 'easeOutQuart',
  },
  scales: {
    x: {
      grid: { display: false, color: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: 'rgba(255, 255, 255, 0.7)' }
    },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(255, 255, 255, 0.1)' },
      ticks: { color: 'rgba(255, 255, 255, 0.7)' }
    }
  },
  plugins: {
    legend: {
      position: 'top',
      labels: { font: { size: 14, family: 'Poppins, sans-serif' }, color: 'white' }
    },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.8)',
      titleFont: { size: 16, family: 'Poppins, sans-serif', weight: '600' },
      bodyFont: { size: 14, family: 'Poppins, sans-serif' },
      padding: 12,
      cornerRadius: 10,
      borderColor: '#00a8e8',
      borderWidth: 1,
    }
  }
});

// Specific options for pie/doughnut charts
const pieChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1500,
    easing: 'easeInOutQuart',
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: { 
        font: { size: 12, family: 'Poppins, sans-serif' }, 
        color: 'white',
        padding: 15,
        usePointStyle: true,
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.9)',
      titleFont: { size: 16, family: 'Poppins, sans-serif', weight: '600' },
      bodyFont: { size: 14, family: 'Poppins, sans-serif' },
      padding: 15,
      cornerRadius: 10,
      borderColor: '#00a8e8',
      borderWidth: 2,
      callbacks: {
        label: function(context) {
          const label = context.label || '';
          const value = context.parsed;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
          return `${label}: ${value} (${percentage}%)`;
        }
      }
    }
  }
});

// Get current user info
const getCurrentUser = () => {
  try {
    const userString = localStorage.getItem('user');
    if (userString) {
      currentUser.value = JSON.parse(userString);
    }
  } catch (error) {
    console.error('Error parsing user data:', error);
  }
};

// Mobile menu toggle
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

// Logout functionality
const handleLogout = () => {
  showLogoutModal.value = true;
};

const confirmLogout = () => {
  localStorage.clear();
  toast.success('Logged out successfully');
  router.push('/login');
  showLogoutModal.value = false;
};

const cancelLogout = () => {
  showLogoutModal.value = false;
};

// Check authentication before loading data
const checkAuth = () => {
  console.log('Checking authentication...');
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const accessToken = localStorage.getItem('access_token');
  const userString = localStorage.getItem('user');
  
  console.log('Auth check details:', {
    isLoggedIn,
    hasAccessToken: !!accessToken,
    hasUser: !!userString
  });
  
  if (!isLoggedIn || isLoggedIn !== 'true' || !accessToken) {
    console.log('Authentication failed - missing credentials');
    toast.error('Please log in to access this page');
    router.push('/login');
    return false;
  }

  try {
    const user = JSON.parse(userString || '{}');
    console.log('Parsed user:', user);
    
    if (user?.role !== 'admin') {
      console.log('Access denied - not admin role');
      toast.error('Access denied. Admin privileges required.');
      router.push('/user-dashboard');
      return false;
    }
    
    console.log('Authentication successful');
    return true;
  } catch (error) {
    console.error('Error parsing user data:', error);
    toast.error('Invalid user data. Please log in again.');
    localStorage.clear();
    router.push('/login');
    return false;
  }
};

// Fetch data for charts
const fetchChartData = async () => {
  console.log('fetchChartData called');
  
  // Temporarily make auth check less strict for debugging
  const authResult = checkAuth();
  console.log('Auth check result:', authResult);
  
  if (!authResult) {
    console.log('Auth failed, but continuing for debugging...');
    // Don't return, continue with fake data for debugging
    loading.charts = false;
    return;
  }

  loading.charts = true;
  try {
    console.log('Fetching reports data...');
    // Fetch reports data from the new API endpoint
    const response = await api.getReportsData();
    console.log('Reports API response:', response);
    
    reportsData.value = response.data;
    console.log('Reports data set:', reportsData.value);

    updateChartData();
    toast.success('Chart data loaded successfully!');
  } catch (error) {
    console.error("Error fetching chart data:", error);
    console.error("Error details:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    handleApiError(error, 'Failed to load chart data');
  } finally {
    loading.charts = false;
  }
};

// Function to update chart data based on fetched reports data
const updateChartData = () => {
  console.log('updateChartData called');
  if (!reportsData.value) {
    console.log('No reports data available');
    return;
  }

  const data = reportsData.value;
  console.log('Updating charts with data:', data);

  // Parking Lot Occupancy Data
  if (data.parking_lots && data.parking_lots.length > 0) {
    const lotLabels = data.parking_lots.map(lot => lot.location_name);
    const occupiedData = data.parking_lots.map(lot => lot.occupied_spots);
    const availableData = data.parking_lots.map(lot => lot.available_spots);

    parkingLotOccupancyData.value = {
      labels: lotLabels,
      datasets: [
        { label: 'Occupied Spots', backgroundColor: '#ef4444', data: occupiedData, borderRadius: 5 },
        { label: 'Available Spots', backgroundColor: '#22c55e', data: availableData, borderRadius: 5 }
      ]
    };
  }

  // Overall Parking Spot Status Data
  if (data.overall_occupancy) {
    const totalOccupied = data.overall_occupancy.occupied_spots || 0;
    const totalAvailable = data.overall_occupancy.available_spots || 0;

    overallSpotStatusData.value = {
      labels: ['Total Spots'],
      datasets: [
        { label: 'Total Occupied', backgroundColor: '#f97316', data: [totalOccupied], borderRadius: 5 },
        { label: 'Total Available', backgroundColor: '#0ea5e9', data: [totalAvailable], borderRadius: 5 }
      ]
    };
  }

  // Monthly Trends Data
  if (data.monthly_trends && data.monthly_trends.length > 0) {
    const monthLabels = data.monthly_trends.map(trend => {
      try {
        const date = new Date(trend.month);
        return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
      } catch (e) {
        return trend.month;
      }
    });
    const monthlyData = data.monthly_trends.map(trend => trend.reservations || 0);

    monthlyTrendsData.value = {
      labels: monthLabels,
      datasets: [
        {
          label: 'Bookings per Month',
          backgroundColor: 'rgba(102, 126, 234, 0.5)',
          borderColor: '#667eea',
          data: monthlyData,
          tension: 0.3,
          fill: true,
        }
      ]
    };
  }

  // User Role Distribution Data
  if (data.user_stats) {
    const adminCount = data.user_stats.admin_users || 0;
    const regularUserCount = data.user_stats.regular_users || 0;

    userRoleDistributionData.value = {
      labels: ['Admin', 'Users'],
      datasets: [
        {
          backgroundColor: ['#00a8e8', 'rgba(255, 255, 255, 0.1)'],
          data: [adminCount, regularUserCount],
          hoverOffset: 4,
        }
      ]
    };
  }

  // Daily Revenue Data
  if (data.daily_revenue && data.daily_revenue.length > 0) {
    const dailyLabels = data.daily_revenue.map(day => {
      try {
        const date = new Date(day.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      } catch (e) {
        return day.date;
      }
    });
    const dailyRevenueValues = data.daily_revenue.map(day => day.revenue || 0);

    dailyRevenueData.value = {
      labels: dailyLabels,
      datasets: [
        {
          label: 'Daily Revenue (₹)',
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          borderColor: '#22c55e',
          data: dailyRevenueValues,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#22c55e',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
        }
      ]
    };
  } else {
    // Generate sample daily revenue data for the last 30 days if no data available
    const last30Days = [];
    const sampleDailyRevenue = [];
    for (let i = 29; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      last30Days.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
      // Generate sample revenue between 500-5000
      sampleDailyRevenue.push(Math.floor(Math.random() * 4500) + 500);
    }

    dailyRevenueData.value = {
      labels: last30Days,
      datasets: [
        {
          label: 'Daily Revenue (₹)',
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          borderColor: '#22c55e',
          data: sampleDailyRevenue,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#22c55e',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
        }
      ]
    };
  }

  // Monthly Revenue Data
  if (data.monthly_revenue && data.monthly_revenue.length > 0) {
    const monthlyRevenueLabels = data.monthly_revenue.map(month => {
      try {
        const date = new Date(month.month);
        return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
      } catch (e) {
        return month.month;
      }
    });
    const monthlyRevenueValues = data.monthly_revenue.map(month => month.revenue || 0);

    monthlyRevenueData.value = {
      labels: monthlyRevenueLabels,
      datasets: [
        {
          label: 'Monthly Revenue (₹)',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          borderColor: '#3b82f6',
          data: monthlyRevenueValues,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#3b82f6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 5,
        }
      ]
    };
  } else {
    // Generate sample monthly revenue data for the last 12 months
    const last12Months = [];
    const sampleMonthlyRevenue = [];
    for (let i = 11; i >= 0; i--) {
      const date = new Date();
      date.setMonth(date.getMonth() - i);
      last12Months.push(date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' }));
      // Generate sample revenue between 15000-50000
      sampleMonthlyRevenue.push(Math.floor(Math.random() * 35000) + 15000);
    }

    monthlyRevenueData.value = {
      labels: last12Months,
      datasets: [
        {
          label: 'Monthly Revenue (₹)',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          borderColor: '#3b82f6',
          data: sampleMonthlyRevenue,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#3b82f6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 5,
        }
      ]
    };
  }

  // Parking Lot Occupancy Comparison Pie Chart
  if (data.parking_lots && data.parking_lots.length > 0) {
    const lotLabels = data.parking_lots.map(lot => lot.location_name);
    const occupancyRates = data.parking_lots.map(lot => {
      const totalSpots = lot.total_spots || 1;
      const occupiedSpots = lot.occupied_spots || 0;
      return Math.round((occupiedSpots / totalSpots) * 100);
    });

    parkingLotComparisonData.value = {
      labels: lotLabels,
      datasets: [
        {
          backgroundColor: [
            '#ef4444', '#f97316', '#eab308', '#22c55e', 
            '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'
          ].slice(0, lotLabels.length),
          data: occupancyRates,
          hoverOffset: 8,
          borderWidth: 2,
          borderColor: '#ffffff',
        }
      ]
    };
  }

  console.log('Chart data updated successfully');
};

// Computed function for overall occupancy rate
const getOverallOccupancyRate = () => {
  if (!reportsData.value || !reportsData.value.overall_occupancy) return 0;
  const { total_spots, occupied_spots } = reportsData.value.overall_occupancy;
  return total_spots > 0 ? Math.round((occupied_spots / total_spots) * 100) : 0;
};

// Computed function to safely get stats with fallbacks
const safeStats = computed(() => {
  if (!reportsData.value) {
    return {
      revenue: 0,
      reservations: 0,
      activeReservations: 0,
      users: 0,
      regularUsers: 0,
      occupiedSpots: 0,
      totalSpots: 0
    };
  }
  
  return {
    revenue: reportsData.value.reservation_stats?.total_revenue || 0,
    reservations: reportsData.value.reservation_stats?.total_reservations || 0,
    activeReservations: reportsData.value.reservation_stats?.active_reservations || 0,
    users: reportsData.value.user_stats?.total_users || 0,
    regularUsers: reportsData.value.user_stats?.regular_users || 0,
    occupiedSpots: reportsData.value.overall_occupancy?.occupied_spots || 0,
    totalSpots: reportsData.value.overall_occupancy?.total_spots || 0
  };
});

// Debug info computed property
const debugInfo = computed(() => {
  return {
    isLoggedIn: localStorage.getItem('isLoggedIn'),
    hasToken: !!localStorage.getItem('access_token'),
    user: localStorage.getItem('user'),
    currentUser: currentUser.value,
    loading: loading.charts,
    hasReportsData: !!reportsData.value
  };
});

// Enhanced error handling
const handleApiError = (error, defaultMessage) => {
  console.error('API Error:', error);
  
  if (error.response) {
    const status = error.response.status;
    const message = error.response.data?.msg || error.response.data?.message || defaultMessage;
    
    if (status === 401 || status === 422) {
      toast.error('Session expired. Please log in again.');
      localStorage.clear();
      router.push('/login');
      return;
    }
    
    toast.error(message);
  } else if (error.request) {
    toast.error('Network error. Please check your connection.');
  } else {
    toast.error(error.message || defaultMessage);
  }
};

// Export and report generation functions
const exportParkingDetails = async () => {
  try {
    loading.charts = true;
    toast.info("Generating comprehensive parking details CSV...");
    
    // Check authentication state
    console.log('Export auth check:', {
      isLoggedIn: localStorage.getItem('isLoggedIn'),
      hasToken: !!localStorage.getItem('access_token'),
      userString: localStorage.getItem('user')
    });
    
    const response = await api.exportParkingDetails();
    console.log('Export response received:', response);
    
    if (response.data && response.data.length > 0) {
      // Enhanced CSV format with better structure
      const enhancedData = response.data.map((record, index) => ({
        'Sr. No.': index + 1,
        'Reservation ID': record.reservation_id,
        'User Name': record.user_name || 'N/A',
        'Email': record.user_email || 'N/A',
        'Vehicle Number': record.vehicle_number || 'Not Provided',
        'Parking Lot': record.parking_lot || 'Unknown',
        'Spot Number': record.spot_number || 'N/A',
        'Check-in Date': formatDateForCSV(record.parking_time),
        'Check-in Time': formatTimeForCSV(record.parking_time),
        'Check-out Date': record.leaving_time ? formatDateForCSV(record.leaving_time) : 'Still Parked',
        'Check-out Time': record.leaving_time ? formatTimeForCSV(record.leaving_time) : 'Active',
        'Duration (Hours)': calculateDuration(record.parking_time, record.leaving_time),
        'Parking Cost (₹)': record.parking_cost || 0,
        'Transaction ID': record.transaction_id || 'Not Available',
        'Payment Method': record.payment_method || 'Not Specified',
        'Status': record.status || 'Unknown',
        'Revenue Generated': record.leaving_time ? `₹${record.parking_cost || 0}` : 'Pending'
      }));
      
      // Convert to CSV format with proper Excel compatibility
      const csvContent = convertToExcelCSV(enhancedData);
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
      const filename = `ParkEase_Parking_Details_${timestamp}.csv`;
      
      downloadCSV(csvContent, filename);
      
      // Show detailed success message
      const totalRevenue = response.data
        .filter(record => record.leaving_time)
        .reduce((sum, record) => sum + (record.parking_cost || 0), 0);
      
      toast.success(
        `✅ Successfully exported ${response.data.length} parking records!\n` +
        `💰 Total Revenue: ₹${totalRevenue.toLocaleString()}\n` +
        `📁 File: ${filename}`,
        { duration: 5000 }
      );
    } else {
      toast.warning("No parking data available for export. Please ensure there are reservations in the system.");
    }
  } catch (error) {
    console.error("Error exporting parking details:", error);
    console.error("Error details:", {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    });
    
    // More specific error handling
    if (error.response?.status === 401) {
      toast.error('Authentication failed. Please log in again.');
      localStorage.clear();
      router.push('/login');
    } else if (error.response?.status === 403) {
      toast.error('Access denied. Admin privileges required.');
    } else {
      handleApiError(error, 'Failed to export parking details');
    }
  } finally {
    loading.charts = false;
  }
};

// Enhanced CSV generation for Excel compatibility
const convertToExcelCSV = (data) => {
  if (!data || data.length === 0) return '';
  
  const headers = Object.keys(data[0]);
  
  // Add BOM for proper UTF-8 encoding in Excel
  const BOM = '\uFEFF';
  
  // Create header row
  const csvHeaders = headers.map(header => `"${header}"`).join(',');
  
  // Create data rows with proper escaping
  const csvRows = data.map(row => 
    headers.map(header => {
      let value = row[header];
      
      // Handle different data types
      if (value === null || value === undefined) {
        value = '';
      } else if (typeof value === 'string') {
        // Escape quotes and wrap in quotes for Excel
        value = `"${value.replace(/"/g, '""')}"`;
      } else if (typeof value === 'number') {
        // Keep numbers as is for proper Excel formatting
        value = value;
      } else {
        // Convert other types to string and wrap in quotes
        value = `"${String(value).replace(/"/g, '""')}"`;
      }
      
      return value;
    }).join(',')
  );
  
  return BOM + [csvHeaders, ...csvRows].join('\r\n');
};

// Helper function to format date for CSV
const formatDateForCSV = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  } catch (e) {
    return 'Invalid Date';
  }
};

// Helper function to format time for CSV
const formatTimeForCSV = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
  } catch (e) {
    return 'Invalid Time';
  }
};

// Helper function to calculate duration
const calculateDuration = (startTime, endTime) => {
  try {
    if (!endTime) return 'Ongoing';
    
    const start = new Date(startTime);
    const end = new Date(endTime);
    const durationMs = end - start;
    const durationHours = durationMs / (1000 * 60 * 60);
    
    if (durationHours < 1) {
      const minutes = Math.round(durationMs / (1000 * 60));
      return `${minutes} min`;
    } else {
      return `${durationHours.toFixed(2)} hrs`;
    }
  } catch (e) {
    return 'Unknown';
  }
};

const generateMonthlyReport = async () => {
  try {
    loading.charts = true;
    toast.info("Generating comprehensive monthly report...");
    
    const response = await api.generateMonthlyReport();
    
    if (response.data) {
      const reportData = response.data;
      
      // Create detailed monthly report data
      const monthlyReportData = [
        ['PAREASE MONTHLY REPORT', '', '', ''],
        ['Report Generated:', new Date().toLocaleString('en-IN'), '', ''],
        ['Report Period:', reportData.month, '', ''],
        ['', '', '', ''],
        ['SUMMARY STATISTICS', '', '', ''],
        ['Total Reservations:', reportData.total_reservations || 0, '', ''],
        ['Total Revenue:', `₹${(reportData.total_revenue || 0).toLocaleString()}`, '', ''],
        ['Average Revenue per Reservation:', reportData.total_reservations > 0 ? `₹${((reportData.total_revenue || 0) / reportData.total_reservations).toFixed(2)}` : '₹0', '', ''],
        ['', '', '', ''],
        ['ADDITIONAL DETAILS', '', '', ''],
        ['Report Type:', 'Monthly Summary', '', ''],
        ['Generated By:', 'ParkEase Admin System', '', ''],
        ['Status:', 'Completed', '', '']
      ];
      
      // Convert to CSV
      const csvContent = monthlyReportData.map(row => 
        row.map(cell => `"${cell}"`).join(',')
      ).join('\r\n');
      
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
      const filename = `ParkEase_Monthly_Report_${reportData.month.replace(' ', '_')}_${timestamp}.csv`;
      
      // Add BOM for Excel compatibility
      const finalCsvContent = '\uFEFF' + csvContent;
      downloadCSV(finalCsvContent, filename);
      
      toast.success(
        `📊 Monthly Report Generated Successfully!\n` +
        `📅 Period: ${reportData.month}\n` +
        `🎯 ${reportData.total_reservations} reservations\n` +
        `💰 ₹${(reportData.total_revenue || 0).toLocaleString()} revenue\n` +
        `📁 File: ${filename}`,
        { duration: 6000 }
      );
    }
  } catch (error) {
    console.error("Error generating monthly report:", error);
    handleApiError(error, 'Failed to generate monthly report');
  } finally {
    loading.charts = false;
  }
};

// New function to export analytics summary
const exportAnalyticsSummary = async () => {
  try {
    loading.charts = true;
    toast.info("Generating analytics summary export...");
    
    if (!reportsData.value) {
      toast.warning("No analytics data available. Please refresh the dashboard first.");
      return;
    }
    
    const data = reportsData.value;
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
    
    // Create comprehensive analytics export
    const analyticsData = [
      ['PAREASE ANALYTICS DASHBOARD EXPORT', '', '', '', ''],
      ['Generated:', new Date().toLocaleString('en-IN'), '', '', ''],
      ['', '', '', '', ''],
      
      ['SYSTEM OVERVIEW', '', '', '', ''],
      ['Total Users:', data.user_stats?.total_users || 0, '', '', ''],
      ['Admin Users:', data.user_stats?.admin_users || 0, '', '', ''],
      ['Regular Users:', data.user_stats?.regular_users || 0, '', '', ''],
      ['Total Reservations:', data.reservation_stats?.total_reservations || 0, '', '', ''],
      ['Active Reservations:', data.reservation_stats?.active_reservations || 0, '', '', ''],
      ['Total Revenue:', `₹${(data.reservation_stats?.total_revenue || 0).toLocaleString()}`, '', '', ''],
      ['', '', '', '', ''],
      
      ['PARKING LOT PERFORMANCE', '', '', '', ''],
      ['Parking Lot', 'Total Spots', 'Occupied', 'Available', 'Occupancy %'],
      ...(data.parking_lots || []).map(lot => [
        lot.location_name,
        lot.total_spots,
        lot.occupied_spots,
        lot.available_spots,
        `${lot.occupancy_rate}%`
      ]),
      ['', '', '', '', ''],
      
      ['MONTHLY TRENDS (Last 6 Months)', '', '', '', ''],
      ['Month', 'Reservations', '', '', ''],
      ...(data.monthly_trends || []).slice(-6).map(trend => [
        trend.month,
        trend.reservations,
        '', '', ''
      ]),
      ['', '', '', '', ''],
      
      ['REVENUE ANALYSIS', '', '', '', ''],
      ['Period', 'Revenue (₹)', '', '', ''],
      ...(data.monthly_revenue || []).slice(-6).map(revenue => [
        revenue.month,
        `₹${revenue.revenue.toLocaleString()}`,
        '', '', ''
      ]),
      ['', '', '', '', ''],
      
      ['OVERALL STATISTICS', '', '', '', ''],
      ['Total Parking Spots:', data.overall_occupancy?.total_spots || 0, '', '', ''],
      ['Currently Occupied:', data.overall_occupancy?.occupied_spots || 0, '', '', ''],
      ['Currently Available:', data.overall_occupancy?.available_spots || 0, '', '', ''],
      ['Overall Occupancy Rate:', `${getOverallOccupancyRate()}%`, '', '', ''],
      ['', '', '', '', ''],
      
      ['EXPORT DETAILS', '', '', '', ''],
      ['Report Type:', 'Analytics Dashboard Export', '', '', ''],
      ['Generated By:', 'ParkEase Admin System', '', '', ''],
      ['Export Format:', 'CSV (Excel Compatible)', '', '', ''],
      ['Status:', 'Completed', '', '', '']
    ];
    
    // Convert to CSV with proper formatting
    const csvContent = '\uFEFF' + analyticsData.map(row => 
      row.map(cell => `"${cell}"`).join(',')
    ).join('\r\n');
    
    const filename = `ParkEase_Analytics_Export_${timestamp}.csv`;
    downloadCSV(csvContent, filename);
    
    toast.success(
      `📊 Analytics Export Completed!\n` +
      `📈 Dashboard data exported successfully\n` +
      `🏢 ${(data.parking_lots || []).length} parking lots analyzed\n` +
      `💰 Total revenue: ₹${(data.reservation_stats?.total_revenue || 0).toLocaleString()}\n` +
      `📁 File: ${filename}`,
      { duration: 5000 }
    );
    
  } catch (error) {
    console.error("Error exporting analytics summary:", error);
    toast.error('Failed to export analytics summary. Please try again.');
  } finally {
    loading.charts = false;
  }
};

// Enhanced helper function to download CSV with Excel compatibility
const downloadCSV = (csvContent, filename) => {
  try {
    // Create blob with proper MIME type for Excel
    const blob = new Blob([csvContent], { 
      type: 'text/csv;charset=utf-8;' 
    });
    
    // Create download link
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      
      // Add to DOM, click, and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the URL object
      setTimeout(() => URL.revokeObjectURL(url), 100);
      
      console.log(`CSV file "${filename}" downloaded successfully`);
    } else {
      // Fallback for browsers that don't support download attribute
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      setTimeout(() => URL.revokeObjectURL(url), 100);
    }
  } catch (error) {
    console.error('Error downloading CSV:', error);
    toast.error('Failed to download CSV file. Please try again.');
  }
};

// Helper function to download JSON
const downloadJSON = (data, filename) => {
  const jsonContent = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonContent], { type: 'application/json;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};


// Initialize component
onMounted(() => {
  console.log('Reports component mounted');
  console.log('Current localStorage state:', {
    isLoggedIn: localStorage.getItem('isLoggedIn'),
    hasAccessToken: !!localStorage.getItem('access_token'),
    user: localStorage.getItem('user')
  });
  
  getCurrentUser();
  
  // Add a small delay to ensure localStorage is ready
  setTimeout(() => {
    fetchChartData();
  }, 100);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Base Container */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Base Container */
.reports-container {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
}

/* Admin Navbar  */
.admin-navbar {
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

.admin-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
}

.admin-avatar i {
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.9);
}

.admin-info {
  display: flex;
  flex-direction: column;
}

.admin-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.admin-role {
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

/* Mobile Menu */
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
  background-image: url('/car1.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  pointer-events: none;
}

.bg-animation::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8); /* 50% black overlay */
  z-index: 1;
}

/* Main Content */
.main-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 70px;
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
  border: 1px solid rgba(255, 215, 0, 0.1);
  border-radius: 25px;
  padding: 2.5rem;
  margin-bottom: 3rem;
  position: relative;
  overflow: hidden;
}

.section-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  /* background: linear-gradient(90deg, transparent, #00a8e8, transparent); */
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
  text-align: left;
}

.refresh-btn {
  flex-shrink: 0;
  min-width: auto;
}

.section-title {
  font-size: 2rem;
  font-weight: 500;
  color: #00a8e8;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0.5rem 0 0 0;
}

/* CTA Buttons */
.cta-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'Poppins', sans-serif;
  min-height: 40px;
  border: 1px solid transparent;
}

.cta-button.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.2);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.35);
  background: linear-gradient(135deg, #005fa3, #0094d1);
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.1);
}

.cta-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: modalFadeIn 0.3s ease-out;
  overflow: hidden; /* Prevent any scrolling in overlay */
  padding: 1rem;
  box-sizing: border-box;
}

@keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-container {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(23, 83, 148, 0.3);
  border-radius: 25px;
  width: 100%;
  max-width: 500px; /* Reduced from 600px */
  max-height: calc(100vh - 2rem); /* Account for padding */
  overflow-y: auto;
  overflow-x: hidden; /* Prevent horizontal scroll */
  animation: modalSlideIn 0.4s ease-out;
  box-sizing: border-box;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.modal-title-section {
  flex: 1;
  min-width: 0; /* Allow flex item to shrink */
  margin-right: 1rem;
}

.modal-title-section h3 {
  font-size: 1.5rem; /* Reduced from 1.8rem */
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.5rem;
  word-wrap: break-word;
}

.modal-title-section p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
  word-wrap: break-word;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 107, 107, 0.8);
  transform: scale(1.1);
}

/* Form Styles (for logout modal, if needed) */
.modal-form {
  padding: 2rem;
}

/* Logout Modal Specific Styles */
.logout-modal {
  max-width: 400px; /* Reduced from 450px */
}

.logout-modal-content {
  padding: 1.5rem; /* Reduced from 2rem */
  text-align: center;
  word-wrap: break-word;
}

.logout-icon {
  width: 70px; /* Reduced from 80px */
  height: 70px;
  margin: 0 auto 1rem; /* Reduced margin */
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: logoutIconPulse 2s ease-in-out infinite;
}

.logout-icon i {
  font-size: 2rem; /* Reduced from 2.5rem */
  color: white;
}

@keyframes logoutIconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 15px rgba(255, 107, 107, 0);
  }
}

.logout-message h4 {
  color: #ffffff;
  font-size: 1.2rem; /* Reduced from 1.3rem */
  font-weight: 600;
  margin-bottom: 0.5rem;
  word-wrap: break-word;
}

.logout-message p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem; /* Reduced from 1rem */
  margin: 0;
  word-wrap: break-word;
}

.logout-confirm-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f) !important;
  border-color: #ff6b6b !important;
}

.logout-confirm-btn:hover {
  background: linear-gradient(135deg, #ff5252, #e53e3e) !important;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35) !important;
}

/* Additional modal fixes */
.modal-footer {
  padding: 1rem 1.5rem 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.modal-footer .cta-button {
  flex: 1;
  min-width: 120px;
  max-width: 200px;
}

/* Statistics Section */
.stats-section {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 168, 232, 0.1);
  border-radius: 20px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #00a8e8, #667eea);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 168, 232, 0.2);
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  flex-shrink: 0;
}

.revenue-card .stat-icon {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.reservations-card .stat-icon {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.users-card .stat-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.occupancy-card .stat-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  color: white;
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  font-weight: 500;
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
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left: 4px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-content p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin: 0;
}

/* Chart Specific Styles */
.chart-section {
  margin-top: 3rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 168, 232, 0.1);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-5px);
}

.chart-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #00a8e8;
  margin-bottom: 1rem;
}

.chart-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 1rem;
}

.chart-canvas {
  max-height: 350px;
  width: 100%;
}

/* New styles for Data Export & Reports section */
.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.report-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 168, 232, 0.1);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  min-height: 250px;
}

.report-card:hover {
  transform: translateY(-5px);
}

.report-card-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #00a8e8;
  margin-bottom: 1rem;
}

.report-card-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
  line-height: 1.5;
}
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
  
  .navbar-menu {
    gap: 1rem;
  }
  
  .nav-links {
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .nav-link span {
    display: none;
  }
  
  .admin-info {
    display: none;
  }
  
  .logout-btn span {
    display: none;
  }
  
  .main-content { 
    padding: 1rem; 
    padding-top: 80px; 
    overflow-x: hidden;
  }
  
  .main-title { 
    font-size: 2rem; 
  }
  
  .hero-section { 
    padding: 2rem 1rem; 
  }
  
  .stats-grid { 
    grid-template-columns: 1fr; 
    gap: 1rem; 
  }
  
  .stat-card { 
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.8rem;
  }
  
  .stat-value {
    font-size: 2rem;
  }
  
  .section-container { 
    padding: 2rem 1.5rem; 
    overflow-x: hidden;
  }
  
  .section-header { 
    flex-direction: column;
    text-align: center;
    align-items: center;
    gap: 1rem;
  }
  
  .section-title-area {
    text-align: center;
  }
  
  .refresh-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .chart-card {
    padding: 1.5rem;
  }
  
  .chart-canvas {
    height: 250px !important;
    max-height: 250px;
  }
  
  .chart-title {
    font-size: 1.3rem;
  }
  
  .reports-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .report-card {
    padding: 1.5rem;
    min-height: 200px;
  }
  
  .report-card-title {
    font-size: 1.2rem;
  }
  
  .cta-button { 
    width: 100%; 
    justify-content: center; 
  }
  
  /* Modal specific mobile fixes */
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-container {
    max-width: calc(100vw - 1rem);
    margin: 0;
  }
  
  .modal-header {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .modal-title-section {
    margin-right: 0;
  }
  
  .logout-modal-content {
    padding: 1rem;
  }
  
  .modal-footer {
    padding: 1rem;
    flex-direction: column;
  }
  
  .modal-footer .cta-button {
    width: 100%;
    max-width: none;
  }
}
@media (max-width: 480px) {
  .brand-text h1 {
    font-size: 1.5rem;
  }
  
  .brand-text p {
    display: none;
  }
  
  .navbar-actions {
    gap: 0.5rem;
  }
  
  .reports-container { 
    padding: 0; 
    overflow-x: hidden;
    width: 100vw;
  }
  
  .main-title { 
    font-size: 1.8rem; 
  }
  
  .main-content { 
    padding: 0.5rem; 
    padding-top: 70px; 
    overflow-x: hidden;
    width: 100%;
  }
  
  .hero-section { 
    padding: 1.5rem 1rem; 
  }
  
  .section-container { 
    padding: 1.5rem 1rem; 
    margin-left: 0;
    margin-right: 0;
    overflow-x: hidden;
  }
  
  .stat-card { 
    padding: 1rem;
    gap: 0.75rem;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
  
  .stat-content h3 {
    font-size: 1rem;
  }
  
  .chart-card {
    padding: 1rem;
  }
  
  .chart-title {
    font-size: 1.1rem;
  }
  
  .chart-canvas {
    height: 200px !important;
    max-height: 200px;
  }
  
  .report-card {
    padding: 1rem;
    min-height: 180px;
  }
  
  .report-card-title {
    font-size: 1.1rem;
  }
  
  .report-card-description {
    font-size: 0.85rem;
  }
  
  /* Extra small screen modal fixes */
  .modal-overlay {
    padding: 0.25rem;
  }
  
  .modal-container {
    max-width: calc(100vw - 0.5rem);
    border-radius: 15px;
  }
  
  .modal-header {
    padding: 0.75rem;
  }
  
  .modal-title-section h3 {
    font-size: 1.2rem;
  }
  
  .modal-title-section p {
    font-size: 0.8rem;
  }
  
  .logout-modal-content {
    padding: 0.75rem;
  }
  
  .logout-icon {
    width: 60px;
    height: 60px;
  }
  
  .logout-icon i {
    font-size: 1.8rem;
  }
  
  .logout-message h4 {
    font-size: 1.1rem;
  }
  
  .logout-message p {
    font-size: 0.8rem;
  }
}
</style>
