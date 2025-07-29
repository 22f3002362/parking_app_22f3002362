<template>
  <div class="my-bookings">
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
              <i class="bi bi-house"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/find-parking" class="nav-link">
              <i class="bi bi-search"></i>
              <span>Find Parking</span>
            </router-link>
            <router-link to="/my-bookings" class="nav-link active">
              <i class="bi bi-calendar-check"></i>
              <span>My Bookings</span>
            </router-link>
            <router-link to="/user-reports" class="nav-link">
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
                <span class="user-name">{{ user?.username || 'User' }}</span>
                <span class="user-role">User</span>
              </div>
            </div>
            <button @click="logout" class="logout-btn">
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
      <div class="mobile-menu" :class="{ 'active': mobileMenuOpen }">
        <div class="mobile-nav-section">
          <div class="mobile-nav-header">
            <i class="bi bi-list"></i>
            <span>Navigation</span>
          </div>
          <div class="mobile-nav-links">
            <router-link to="/user-dashboard" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-house"></i>
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
              <span class="mobile-user-name">{{ user?.username || 'User' }}</span>
              <span class="mobile-user-role">User</span>
            </div>
          </div>
          <button @click="logout" class="mobile-logout-btn">
            <i class="bi bi-box-arrow-right"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- My Custom Wallpaper is under this div -->
    <div class="bg-animation">
    </div>

    <!-- Main Content -->
    <div class="booking-content">
      <div class="page-header">
        <h1>My Bookings</h1>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading your bookings...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-container">
        <i class="bi bi-exclamation-triangle"></i>
        <h3>Error Loading Bookings</h3>
        <p>{{ error }}</p>
        <button @click="fetchReservations" class="retry-btn">
          <i class="bi bi-arrow-clockwise"></i>
          Try Again
        </button>
      </div>

      <!-- Bookings Content -->
      <div v-else class="bookings-wrapper">
        <!-- Summary Cards -->
        <div class="summary-cards">
          <div class="summary-card active">
            <div class="card-icon">
              <i class="bi bi-car-front"></i>
            </div>
            <div class="card-content">
              <div class="card-number">{{ activeReservations.length }}</div>
              <div class="card-label">Active Bookings</div>
            </div>
          </div>
          
          <div class="summary-card completed">
            <div class="card-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="card-content">
              <div class="card-number">{{ completedReservations.length }}</div>
              <div class="card-label">Completed Bookings</div>
            </div>
          </div>
          
          <div class="summary-card total">
            <div class="card-icon">
              <i class="bi bi-bookmark-check"></i>
            </div>
            <div class="card-content">
              <div class="card-number">{{ totalReservations.length }}</div>
              <div class="card-label">Total Bookings</div>
            </div>
          </div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-tabs">
          <button 
            @click="activeTab = 'active'" 
            :class="['tab-btn', { active: activeTab === 'active' }]"
          >
            <i class="bi bi-car-front"></i>
            Active Bookings ({{ activeReservations.length }})
          </button>
          <button 
            @click="activeTab = 'completed'" 
            :class="['tab-btn', { active: activeTab === 'completed' }]"
          >
            <i class="bi bi-check-circle"></i>
            Completed Bookings ({{ completedReservations.length }})
          </button>
          <button 
            @click="activeTab = 'all'" 
            :class="['tab-btn', { active: activeTab === 'all' }]"
          >
            <i class="bi bi-list-check"></i>
            All Bookings ({{ totalReservations.length }})
          </button>
        </div>

        <!-- Active Bookings -->
        <div v-if="activeTab === 'active'" class="bookings-section">
          <div v-if="activeReservations.length === 0" class="empty-state">
            <i class="bi bi-car-front"></i>
            <h3>No Active Bookings</h3>
            <p>You don't have any active parking reservations at the moment.</p>
          </div>
          
          <div v-else class="booking-cards">
            <div v-for="reservation in activeReservations" :key="reservation.id" class="booking-card active">
              <div class="card-header">
                <div class="status-badge active">
                  <i class="bi bi-car-front"></i>
                  Active
                </div>
                <div class="booking-id">#{{ reservation.id }}</div>
              </div>
              
              <div class="card-content">
                <div class="location-info">
                  <h3>{{ reservation.lot_name || 'Unknown Location' }}</h3>
                  <p><i class="bi bi-geo-alt"></i> Spot #{{ reservation.spot_id || 'N/A' }}</p>
                </div>
                
                <div class="booking-details">
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-calendar3"></i>
                      Parked:
                    </span>
                    <span class="detail-value">{{ formatDateTime(reservation.parking_time) }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-clock"></i>
                      Duration:
                    </span>
                    <span class="detail-value">{{ calculateDuration(reservation.parking_time) }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-clock-history"></i>
                      Expires:
                    </span>
                    <span class="detail-value">
                      {{ reservation.leaving_time ? formatDateTime(reservation.leaving_time) : 'Manual Release Only' }}
                    </span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-currency-rupee"></i>
                      Estimated Cost:
                    </span>
                    <span class="detail-value cost">
                      ₹{{ calculateEstimatedCost(reservation) }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="card-actions">
                <button 
                  @click="releaseParkingSpot(reservation)"
                  :disabled="releasing"
                  class="release-btn"
                >
                  <i class="bi bi-car-front-fill"></i>
                  {{ releasing ? 'Releasing...' : 'Release Spot' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Completed Bookings -->
        <div v-if="activeTab === 'completed'" class="bookings-section">
          <div v-if="completedReservations.length === 0" class="empty-state">
            <i class="bi bi-check-circle"></i>
            <h3>No Completed Bookings</h3>
            <p>You haven't completed any parking sessions yet.</p>
          </div>
          
          <div v-else class="booking-cards">
            <div v-for="reservation in completedReservations" :key="reservation.id" class="booking-card completed">
              <div class="card-header">
                <div class="status-badge completed">
                  <i class="bi bi-check-circle"></i>
                  Completed
                </div>
                <div class="booking-id">#{{ reservation.id }}</div>
              </div>
              
              <div class="card-content">
                <div class="location-info">
                  <h3>{{ reservation.lot_name || 'Unknown Location' }}</h3>
                  <p><i class="bi bi-geo-alt"></i> Spot #{{ reservation.spot_id || 'N/A' }}</p>
                </div>
                
                <div class="booking-details">
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-calendar3"></i>
                      Parked:
                    </span>
                    <span class="detail-value">{{ formatDateTime(reservation.parking_time) }}</span>
                  </div>
                  
                  <div class="detail-row" v-if="reservation.leaving_time">
                    <span class="detail-label">
                      <i class="bi bi-calendar-x"></i>
                      Released:
                    </span>
                    <span class="detail-value">{{ formatDateTime(reservation.leaving_time) }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-clock"></i>
                      Duration:
                    </span>
                    <span class="detail-value">{{ calculateTotalDuration(reservation) }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-currency-rupee"></i>
                      Total Cost:
                    </span>
                    <span class="detail-value cost">₹{{ reservation.parking_cost || '0' }}</span>
                  </div>
                  
                  <!-- Transaction Details for Completed Reservations -->
                  <div v-if="reservation.transaction_id" class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-receipt"></i>
                      Transaction ID:
                    </span>
                    <span class="detail-value transaction-id">{{ reservation.transaction_id }}</span>
                  </div>
                  
                  <div v-if="reservation.payment_method" class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-credit-card"></i>
                      Payment Method:
                    </span>
                    <span class="detail-value">{{ reservation.payment_method }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- All Bookings -->
        <div v-if="activeTab === 'all'" class="bookings-section">
          <div v-if="totalReservations.length === 0" class="empty-state">
            <i class="bi bi-list-check"></i>
            <h3>No Bookings Found</h3>
            <p>You haven't made any parking reservations yet.</p>
            <router-link to="/find-parking" class="find-parking-btn">
              <i class="bi bi-search"></i>
              Find Parking
            </router-link>
          </div>
          
          <div v-else class="booking-cards">
            <div v-for="reservation in sortedReservations" :key="reservation.id" 
                 :class="['booking-card', reservation.leaving_time ? 'completed' : 'active']">
              <div class="card-header">
                <div :class="['status-badge', reservation.leaving_time ? 'completed' : 'active']">
                  <i :class="reservation.leaving_time ? 'bi bi-check-circle' : 'bi bi-car-front'"></i>
                  {{ reservation.leaving_time ? 'Completed' : 'Active' }}
                </div>
                <div class="booking-id">#{{ reservation.id }}</div>
              </div>
              
              <div class="card-content">
                <div class="location-info">
                  <h3>{{ reservation.lot_name || 'Unknown Location' }}</h3>
                  <p><i class="bi bi-geo-alt"></i> Spot #{{ reservation.spot_id || 'N/A' }}</p>
                </div>
                
                <div class="booking-details">
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-calendar3"></i>
                      Parked:
                    </span>
                    <span class="detail-value">{{ formatDateTime(reservation.parking_time) }}</span>
                  </div>
                  
                  <div class="detail-row" v-if="reservation.leaving_time">
                    <span class="detail-label">
                      <i class="bi bi-calendar-x"></i>
                      Released:
                    </span>
                    <span class="detail-value">{{ formatDateTime(reservation.leaving_time) }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-clock"></i>
                      Duration:
                    </span>
                    <span class="detail-value">
                      {{ reservation.leaving_time ? calculateTotalDuration(reservation) : calculateDuration(reservation.parking_time) }}
                    </span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-currency-rupee"></i>
                      Cost:
                    </span>
                    <span class="detail-value cost">
                      {{ reservation.parking_cost ? '₹' + reservation.parking_cost : (reservation.leaving_time ? '₹0' : 'Calculated on Release') }}
                    </span>
                  </div>
                  
                  <!-- Transaction Details for Completed Reservations -->
                  <div v-if="reservation.transaction_id && reservation.leaving_time" class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-receipt"></i>
                      Transaction ID:
                    </span>
                    <span class="detail-value transaction-id">{{ reservation.transaction_id }}</span>
                  </div>
                  
                  <div v-if="reservation.payment_method && reservation.leaving_time" class="detail-row">
                    <span class="detail-label">
                      <i class="bi bi-credit-card"></i>
                      Payment Method:
                    </span>
                    <span class="detail-value">{{ reservation.payment_method }}</span>
                  </div>
                </div>
              </div>
              
              <div v-if="!reservation.leaving_time" class="card-actions">
                <button 
                  @click="releaseParkingSpot(reservation)"
                  :disabled="releasing"
                  class="release-btn"
                >
                  <i class="bi bi-car-front-fill"></i>
                  {{ releasing ? 'Releasing...' : 'Release Spot' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Modal -->
    <PaymentModal
      :is-visible="showPaymentModal"
      :reservation="currentReservation"
      :amount="currentReservation?.parking_cost"
      @close="closePaymentModal"
      @payment-success="handlePaymentSuccess"
    />

    <!-- Custom Alert Modal -->
    <div v-if="showCustomAlert" class="alert-modal-overlay" @click="closeAlert">
      <div class="alert-modal" @click.stop>
        <div class="alert-header" :class="alertType">
          <div class="alert-icon">
            <i v-if="alertType === 'success'" class="bi bi-check-circle"></i>
            <i v-else-if="alertType === 'error'" class="bi bi-exclamation-circle"></i>
            <i v-else-if="alertType === 'warning'" class="bi bi-exclamation-triangle"></i>
          </div>
          <h3>{{ alertTitle }}</h3>
        </div>
        <div class="alert-content">
          <p>{{ alertMessage }}</p>
        </div>
        <div class="alert-actions">
          <button @click="closeAlert" class="alert-btn" :class="alertType">
            <i class="bi bi-check"></i>
            OK
          </button>
        </div>
      </div>
    </div>

    <!-- Custom Confirmation Modal -->
    <div v-if="showConfirmModal" class="alert-modal-overlay" @click="cancelConfirmation">
      <div class="alert-modal" @click.stop>
        <div class="alert-header warning">
          <div class="alert-icon">
            <i class="bi bi-question-circle"></i>
          </div>
          <h3>{{ confirmTitle }}</h3>
        </div>
        <div class="alert-content">
          <p>{{ confirmMessage }}</p>
        </div>
        <div class="alert-actions">
          <button @click="cancelConfirmation" class="confirm-btn cancel">
            <i class="bi bi-x"></i>
            Cancel
          </button>
          <button @click="confirmAction" class="confirm-btn confirm">
            <i class="bi bi-check"></i>
            Confirm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import PaymentModal from './PaymentModal.vue'

export default {
  name: 'MyBookings',
  components: {
    PaymentModal
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const releasing = ref(false)
    const activeTab = ref('active')
    const mobileMenuOpen = ref(false)
    
    // Custom alert modal states
    const showCustomAlert = ref(false)
    const alertTitle = ref('')
    const alertMessage = ref('')
    const alertType = ref('success') // 'success', 'error', 'warning'
    
    // Custom confirmation modal states
    const showConfirmModal = ref(false)
    const confirmTitle = ref('')
    const confirmMessage = ref('')
    const confirmCallback = ref(null)
    
    const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const totalReservations = ref([])

    const activeReservations = computed(() => 
      totalReservations.value.filter(reservation => !reservation.leaving_time)
    )

    const completedReservations = computed(() => 
      totalReservations.value.filter(reservation => reservation.leaving_time)
    )

    const sortedReservations = computed(() => 
      [...totalReservations.value].sort((a, b) => new Date(b.parking_time) - new Date(a.parking_time))
    )

    const fetchReservations = async () => {
      loading.value = true
      error.value = null
      
      try {
        const userId = user.value.id
        if (!userId) {
          error.value = 'User ID not found. Please log in again.'
          return
        }
        
        const response = await api.getUserReservations(userId)
        totalReservations.value = response.reservations || response || []
      } catch (err) {
        console.error('Error fetching reservations:', err)
        error.value = 'Failed to load reservations. Please try again.'
      } finally {
        loading.value = false
      }
    }

    // Payment modal state
    const showPaymentModal = ref(false)
    const currentReservation = ref(null)

    const releaseParkingSpot = async (reservation) => {
      console.log('🔥 releaseParkingSpot function called!')
      console.log('Reservation data:', reservation)
      
      if (releasing.value) {
        console.log('Already releasing, returning')
        return
      }
      
      // Calculate parking cost
      console.log('Calculating parking cost...')
      const parkingCost = calculateParkingCost(reservation)
      console.log('Calculated cost:', parkingCost)
      
      // Show custom confirmation modal
      showConfirmation(
        'Release Parking Spot',
        `Are you sure you want to release parking spot #${reservation.spot_id}?\n\nEstimated cost: ₹${parkingCost}`,
        () => {
          // Show payment modal
          console.log('Setting current reservation and showing modal...')
          currentReservation.value = { ...reservation, parking_cost: parkingCost }
          showPaymentModal.value = true
          console.log('Modal should be visible now. showPaymentModal.value:', showPaymentModal.value)
          console.log('currentReservation.value:', currentReservation.value)
        }
      )
    }

    const calculateEstimatedCost = (reservation) => {
      if (!reservation.parking_time) return 20 // Default minimum cost
      
      const startTime = new Date(reservation.parking_time)
      const now = new Date()
      const diffMs = now - startTime
      const diffHours = Math.ceil(diffMs / (1000 * 60 * 60)) // Round up to next hour
      
      // Use the actual lot price from the reservation data, fallback to ₹10 per hour
      const costPerHour = reservation.lot_price || 10
      // Keep minimum cost as ₹20 regardless of hourly rate
      const totalCost = Math.max(diffHours * costPerHour, 20)
      
      return totalCost
    }

    // Custom alert functions
    const showAlert = (title, message, type = 'success') => {
      alertTitle.value = title
      alertMessage.value = message
      alertType.value = type
      showCustomAlert.value = true
    }

    const closeAlert = () => {
      showCustomAlert.value = false
      alertTitle.value = ''
      alertMessage.value = ''
      alertType.value = 'success'
    }

    // Custom confirmation functions
    const showConfirmation = (title, message, callback) => {
      confirmTitle.value = title
      confirmMessage.value = message
      confirmCallback.value = callback
      showConfirmModal.value = true
    }

    const confirmAction = () => {
      showConfirmModal.value = false
      if (confirmCallback.value) {
        confirmCallback.value()
      }
      confirmCallback.value = null
    }

    const cancelConfirmation = () => {
      showConfirmModal.value = false
      confirmTitle.value = ''
      confirmMessage.value = ''
      confirmCallback.value = null
    }

    const calculateParkingCost = (reservation) => {
      return calculateEstimatedCost(reservation)
    }

    const handlePaymentSuccess = async (paymentData) => {
      releasing.value = true
      
      try {
        console.log('🔥 Payment successful, calling API to release parking spot...')
        console.log('Payment data:', paymentData)
        console.log('Current reservation:', currentReservation.value)
        
        // Prepare transaction data for backend
        const transactionData = {
          transactionId: paymentData.transactionId,
          paymentMethod: paymentData.paymentMethod
        }
        
        // Call the API to actually release the parking spot with transaction details
        const response = await api.releaseParkingSpot(currentReservation.value.id, transactionData)
        console.log('✅ Release API response:', response)
        
        // Update the reservation in local state with the actual response data
        const index = totalReservations.value.findIndex(r => r.id === currentReservation.value.id)
        if (index !== -1) {
          totalReservations.value[index] = {
            ...totalReservations.value[index],
            leaving_time: response.reservation?.leaving_time || new Date().toISOString(),
            parking_cost: response.reservation?.parking_cost || paymentData.amount,
            transaction_id: response.reservation?.transaction_id || paymentData.transactionId,
            payment_method: response.reservation?.payment_method || paymentData.paymentMethod,
            status: 'completed'
          }
          console.log('✅ Updated reservation in local state')
        }
        
        // Close payment modal
        showPaymentModal.value = false
        currentReservation.value = null
        
        // Show success message
        showAlert('Parking Released Successfully', `Total cost: ₹${response.reservation?.parking_cost || paymentData.amount}\nTransaction ID: ${response.reservation?.transaction_id || paymentData.transactionId}`, 'success')
        
        // Refresh reservations data from server to ensure consistency
        await fetchReservations()
        
      } catch (err) {
        console.error('❌ Error releasing parking spot:', err)
        console.error('Error details:', err.response?.data || err.message)
        
        // Still close the modal since payment was successful
        showPaymentModal.value = false
        currentReservation.value = null
        
        // Show error but acknowledge payment success
        const errorMsg = err.response?.data?.msg || err.message || 'Unknown error occurred'
        showAlert('Payment Successful with Warning', `Payment was successful, but there was an issue releasing the parking spot: ${errorMsg}\n\nPlease contact support with this transaction ID: ${paymentData.transactionId}`, 'warning')
        
        // Try to refresh data anyway
        try {
          await fetchReservations()
        } catch (refreshErr) {
          console.error('Failed to refresh reservations:', refreshErr)
        }
      } finally {
        releasing.value = false
      }
    }

    const closePaymentModal = () => {
      showPaymentModal.value = false
      currentReservation.value = null
    }

    const testModal = () => {
      console.log('🧪 Test modal button clicked!')
      const testReservation = {
        id: 999,
        spot_id: 42,
        lot_name: 'Test Mall',
        parking_time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        parking_cost: 50
      }
      currentReservation.value = testReservation
      showPaymentModal.value = true
      console.log('✅ Test modal should be visible now!')
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      
      try {
        const date = new Date(dateString)
        return date.toLocaleString('en-IN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        })
      } catch (err) {
        return 'Invalid Date'
      }
    }

    const calculateDuration = (startTime) => {
      if (!startTime) return 'N/A'
      
      try {
        const start = new Date(startTime)
        const now = new Date()
        const diffMs = now - start
        
        const hours = Math.floor(diffMs / (1000 * 60 * 60))
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
        
        if (hours > 0) {
          return `${hours}h ${minutes}m`
        } else {
          return `${minutes}m`
        }
      } catch (err) {
        return 'N/A'
      }
    }

    const calculateTotalDuration = (reservation) => {
      if (!reservation.parking_time || !reservation.leaving_time) return 'N/A'
      
      try {
        const start = new Date(reservation.parking_time)
        const end = new Date(reservation.leaving_time)
        const diffMs = end - start
        
        const hours = Math.floor(diffMs / (1000 * 60 * 60))
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
        
        if (hours > 0) {
          return `${hours}h ${minutes}m`
        } else {
          return `${minutes}m`
        }
      } catch (err) {
        return 'N/A'
      }
    }

    const logout = () => {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      router.push('/login')
    }

    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }

    const closeMobileMenu = () => {
      mobileMenuOpen.value = false
    }

    onMounted(() => {
      fetchReservations()
    })

    return {
      loading,
      error,
      releasing,
      activeTab,
      user,
      totalReservations,
      activeReservations,
      completedReservations,
      sortedReservations,
      mobileMenuOpen,
      showPaymentModal,
      currentReservation,
      fetchReservations,
      releaseParkingSpot,
      handlePaymentSuccess,
      closePaymentModal,
      testModal,
      calculateEstimatedCost,
      formatDateTime,
      calculateDuration,
      calculateTotalDuration,
      logout,
      toggleMobileMenu,
      closeMobileMenu,
      // Custom alert modal
      showCustomAlert,
      alertTitle,
      alertMessage,
      alertType,
      closeAlert,
      // Custom confirmation modal
      showConfirmModal,
      confirmTitle,
      confirmMessage,
      confirmAction,
      cancelConfirmation
    }
  }
}
</script>

<style scoped>
/* User Navbar */

.my-bookings { 
  font-family: 'poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}
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

/* Mobile Menu Toggle */
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

/* Main Content */
.my-bookings {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
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
  background-color: rgba(0, 0, 0, 0.8); /* 80% black overlay */
  z-index: 1;
}

.booking-content {
  position: relative;
  z-index: 2;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  padding-top: 70px;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.3) 0%, rgba(26,45,67,0.6) 100%);
  border-radius: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
}

.page-header h1::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #00a8e8, #ffffff);
  margin: 1rem auto;
}

.page-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  max-width: 600px;
  margin: 0 auto;
}

/* Loading and Error States */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

.loading-container p {
  color: rgba(255, 255, 255, 0.8);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top: 4px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container i {
  font-size: 3rem;
  color: #ff6b6b;
  margin-bottom: 1rem;
}

.error-container h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: linear-gradient(135deg, #005fa3, #0094d1);
  transform: translateY(-1px);
}

/* Summary Cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  animation: slideUpFade 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
}

.summary-card:nth-child(1) { animation-delay: 0.1s; }
.summary-card:nth-child(2) { animation-delay: 0.2s; }
.summary-card:nth-child(3) { animation-delay: 0.3s; }

@keyframes slideUpFade {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.summary-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.08);
}

.card-icon {
  font-size: 2.5rem;
  color: #00a8e8;
  background: rgba(0, 168, 232, 0.1);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content {
  flex: 1;
}

.card-number {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.card-label {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  font-size: 0.95rem;
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5rem;
  border-radius: 12px;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
}

.tab-btn.active {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 168, 232, 0.3);
}

.tab-btn i {
  font-size: 1rem;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}

.empty-state i {
  font-size: 4rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #ffffff;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2rem;
  max-width: 400px;
}

.find-parking-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.find-parking-btn:hover {
  background: linear-gradient(135deg, #005fa3, #0094d1);
  transform: translateY(-1px);
  color: white;
}

/* Booking Cards */
.booking-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.booking-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.booking-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.08);
}

.booking-card.active {
  border-left: 4px solid #00a8e8;
}

.booking-card.completed {
  border-left: 4px solid #4ecdc4;
}

.card-header {
  padding: 1.5rem 1.5rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: white;
}

.status-badge.active {
  background: linear-gradient(135deg, #0077be, #00a8e8);
}

.status-badge.completed {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.booking-id {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  font-weight: 500;
}

.card-content {
  padding: 0 1.5rem 1rem;
}

.location-info h3 {
  color: #ffffff;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.location-info p {
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.booking-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  font-weight: 500;
}

.detail-value {
  color: #ffffff;
  font-weight: 600;
  text-align: right;
}

.detail-value.cost {
  color: #4ecdc4;
  font-size: 1.1rem;
}

.detail-value.transaction-id {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #00a8e8;
  font-weight: 600;
  background: rgba(0, 168, 232, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.card-actions {
  padding: 1rem 1.5rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.release-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.release-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ee5a6f, #e53e3e);
  transform: translateY(-1px);
}

.release-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 1rem;
    height: 70px;
    position: relative;
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
  
  .booking-content {
    padding: 1rem;
    padding-top: 80px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .filter-tabs {
    flex-direction: column;
  }
  
  .booking-cards {
    grid-template-columns: 1fr;
  }
  
  .detail-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .detail-value {
    text-align: left;
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
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

/* Custom Alert Modal */
.alert-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20000;
  animation: alertFadeIn 0.3s ease-out;
}

@keyframes alertFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.alert-modal {
  background: rgba(26, 26, 26, 0.98);
  backdrop-filter: blur(30px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  width: 90%;
  margin: 1rem;
  overflow: hidden;
  animation: alertSlideIn 0.4s ease-out;
}

@keyframes alertSlideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.alert-header {
  padding: 2rem 1.5rem 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.alert-header.error {
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(220, 53, 69, 0.05));
  border-bottom-color: rgba(220, 53, 69, 0.2);
}

.alert-header.warning {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
  border-bottom-color: rgba(255, 193, 7, 0.2);
}

.alert-header.success {
  background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(40, 167, 69, 0.05));
  border-bottom-color: rgba(40, 167, 69, 0.2);
}

.alert-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.alert-header.error .alert-icon {
  color: #dc3545;
}

.alert-header.warning .alert-icon {
  color: #ffc107;
}

.alert-header.success .alert-icon {
  color: #28a745;
}

.alert-header h3 {
  color: #ffffff;
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
}

.alert-content {
  padding: 1.5rem;
  text-align: center;
}

.alert-content p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  white-space: pre-line;
}

.alert-actions {
  padding: 1rem 1.5rem 1.5rem;
  text-align: center;
}

.alert-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 120px;
  justify-content: center;
}

.alert-btn.error {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

.alert-btn.error:hover {
  background: linear-gradient(135deg, #c82333, #bd2130);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(220, 53, 69, 0.4);
}

.alert-btn.warning {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  color: #000000;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
}

.alert-btn.warning:hover {
  background: linear-gradient(135deg, #e0a800, #d39e00);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 193, 7, 0.4);
}

.alert-btn.success {
  background: linear-gradient(135deg, #28a745, #20692e);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.alert-btn.success:hover {
  background: linear-gradient(135deg, #20692e, #1e5f2a);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(40, 167, 69, 0.4);
}

/* Custom Confirmation Modal */
.confirm-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 100px;
  justify-content: center;
  margin: 0 0.5rem;
}

.confirm-btn.cancel {
  background: linear-gradient(135deg, #6c757d, #5a6268);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
}

.confirm-btn.cancel:hover {
  background: linear-gradient(135deg, #5a6268, #545b62);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(108, 117, 125, 0.4);
}

.confirm-btn.confirm {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  color: #000000;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
}

.confirm-btn.confirm:hover {
  background: linear-gradient(135deg, #e0a800, #d39e00);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 193, 7, 0.4);
}

.alert-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
</style>
