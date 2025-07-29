<template>
  <div class="user-dashboard-container">
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
            <router-link to="/user-dashboard" class="nav-link active">
              <i class="bi bi-house"></i>
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

    <!-- Background Animation -->
    <div class="bg-animation"></div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
            <h1 class="main-title">Welcome {{ currentUser?.username || 'User' }}</h1>
          <p class="hero-subtitle">Find and book your perfect parking spot with ease</p>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="bi bi-car-front"></i>
              </div>
              <div class="stat-details">
                <div class="stat-number">{{ activeReservations.length }}</div>
                <div class="stat-label">Active Parking</div>
              </div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="bi bi-clock-history"></i>
              </div>
              <div class="stat-details">
                <div class="stat-number">{{ totalReservations.length }}</div>
                <div class="stat-label">Total Bookings</div>
              </div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="bi bi-geo-alt"></i>
              </div>
              <div class="stat-details">
                <div class="stat-number">{{ availableLots.length }}</div>
                <div class="stat-label">Available Lots</div>
              </div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="bi bi-currency-rupee"></i>
              </div>
              <div class="stat-details">
                <div class="stat-number">₹{{ totalSpentMoney.toFixed(0) }}</div>
                <div class="stat-label">Total Spent</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Active Parking -->
      <div v-if="activeReservations.length > 0" class="section-container">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-car-front-fill"></i>
              Current Parking
            </h2>
            <p class="section-subtitle">Manage your active parking sessions</p>
          </div>
        </div>

        <div class="active-parking-grid">
          <div v-for="reservation in activeReservations" :key="reservation.id" class="active-parking-card">
            <div class="parking-header">
              <div class="parking-location">
                <h3>{{ reservation.lot_name || 'Unknown Location' }}</h3>
                <p>Spot #{{ reservation.spot_id || 'N/A' }}</p>
              </div>
              <div class="parking-status">
                <span class="status-badge occupied">Active</span>
              </div>
            </div>
            
            <div class="parking-details">
              <div class="detail-item">
                <i class="bi bi-calendar"></i>
                <span>Parked: {{ formatDateTime(reservation.parking_time) }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-clock"></i>
                <span>Duration: {{ calculateDuration(reservation.parking_time) }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-clock-history"></i>
                <span>Expires: {{ reservation.leaving_time ? formatDateTime(reservation.leaving_time) : 'Manual Release Only' }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-currency-rupee"></i>
                <span>Cost: {{ reservation.parking_cost ? '₹' + reservation.parking_cost : 'Calculated on Release' }}</span>
              </div>
            </div>

            <div class="parking-actions">
              <button 
                class="action-btn release"
                @click="releaseParkingSpot(reservation)"
                :disabled="releasing"
              >
                <i class="bi bi-car-front"></i>
                {{ releasing ? 'Releasing...' : 'Release Parking' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Available Parking Lots -->
      <div class="section-container" id="parking-lots">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-geo-alt-fill"></i>
              Available Parking Lots
            </h2>
            <p class="section-subtitle">Choose from our available parking facilities</p>
          </div>
          <div class="section-actions">
            <button class="cta-button primary" @click="refreshData">
              <i class="bi bi-arrow-clockwise"></i>
              Refresh
            </button>
          </div>
        </div>

        <div v-if="loading.lots" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading parking lots...</p>
        </div>

        <div v-else-if="availableLots.length === 0" class="empty-state">
          <i class="bi bi-geo-alt"></i>
          <h3>No parking lots available</h3>
          <p>Please check back later for available parking spots</p>
        </div>

        <div v-else class="lots-grid">
          <div v-for="lot in availableLots" :key="lot.id" class="lot-card">
            <div class="lot-header">
              <div class="lot-info">
                <h3 class="lot-name">{{ lot.location_name }}</h3>
                <p class="lot-address">{{ lot.address }}</p>
                <span class="lot-pincode">{{ lot.pincode }}</span>
              </div>
              <div class="lot-price">
                <span class="price-amount">₹{{ lot.price }}</span>
                <span class="price-unit">/hour</span>
              </div>
            </div>

            <div class="lot-stats">
              <div class="stat-item">
                <i class="bi bi-car-front"></i>
                <span>{{ lot.available_slots }} / {{ lot.number_of_slots }} Available</span>
              </div>
              <div class="availability-bar">
                <div 
                  class="availability-fill"
                  :style="{ width: (lot.available_slots / lot.number_of_slots * 100) + '%' }"
                ></div>
              </div>
            </div>

            <div class="lot-actions">
              <button 
                class="cta-button primary full-width"
                @click="selectParkingLot(lot)"
                :disabled="lot.available_slots === 0 || booking"
              >
                <i class="bi bi-car-front-fill"></i>
                {{ lot.available_slots === 0 ? 'Full' : (booking ? 'Booking...' : 'Park Here') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- My Reservations History -->
      <div class="section-container" id="my-bookings">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-bookmark-check-fill"></i>
              My Booking History
            </h2>
            <p class="section-subtitle">View all your past and current parking reservations</p>
          </div>
        </div>

        <div v-if="loading.reservations" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading your reservations...</p>
        </div>

        <div v-else-if="totalReservations.length === 0" class="empty-state">
          <i class="bi bi-bookmark"></i>
          <h3>No reservations found</h3>
          <p>You haven't made any parking reservations yet</p>
        </div>

        <div v-else class="table-container">
          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Location</th>
                  <th>Spot</th>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Duration</th>
                  <th>Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(reservation, idx) in sortedReservations" :key="reservation.id">
                  <td>{{ String(idx + 1).padStart(2, '0') }}</td>
                  <td class="location-cell">
                    <div class="location-info">
                      <span class="location-name">{{ reservation.lot_name || 'N/A' }}</span>
                      <small class="location-address">{{ reservation.lot_address || '' }}</small>
                    </div>
                  </td>
                  <td>
                    <span class="badge spot-badge">#{{ reservation.spot_id || 'N/A' }}</span>
                  </td>
                  <td>{{ formatDateTime(reservation.parking_time) }}</td>
                  <td>{{ reservation.leaving_time ? formatDateTime(reservation.leaving_time) : 'Ongoing' }}</td>
                  <td>
                    <span v-if="reservation.leaving_time" class="badge duration-badge">
                      {{ calculateCompletedDuration(reservation.parking_time, reservation.leaving_time) }}
                    </span>
                    <span v-else class="badge ongoing-badge">{{ calculateDuration(reservation.parking_time) }}</span>
                  </td>
                  <td>
                    <span class="badge price-badge">
                      {{ reservation.parking_cost ? '₹' + reservation.parking_cost : 'On Release' }}
                    </span>
                  </td>
                  <td>
                    <span 
                      class="badge status-badge"
                      :class="getReservationStatus(reservation).toLowerCase()"
                    >
                      {{ getReservationStatus(reservation) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message.text" :class="['message-toast', message.type]">
      <i :class="message.type === 'success' ? 'bi bi-check-circle' : 'bi bi-exclamation-triangle'"></i>
      {{ message.text }}
    </div>

    <!-- Vehicle Number Modal -->
    <div v-if="showVehicleModal" class="modal-overlay" @click="closeVehicleModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>Vehicle Information Required</h3>
            <p>Please provide your vehicle number to proceed with parking reservation</p>
          </div>
          <button class="close-btn" @click="closeVehicleModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <form @submit.prevent="submitVehicleNumber" class="modal-form">
          <div class="form-group">
            <label class="form-label">
              <i class="bi bi-car-front"></i>
              Vehicle Number
            </label>
            <input
              v-model="vehicleForm.vehicle_number"
              type="text"
              class="form-input"
              placeholder="Enter your vehicle number (e.g., MH01AB1234)"
              required
              pattern="[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
              title="Please enter a valid vehicle number format (e.g., MH01AB1234)"
              maxlength="13"
              style="text-transform: uppercase;"
              @input="vehicleForm.vehicle_number = $event.target.value.toUpperCase()"
            />
            <small class="form-hint">Enter your vehicle registration number</small>
          </div>

          <div class="modal-footer">
            <button type="button" class="cta-button secondary" @click="closeVehicleModal">
              Cancel
            </button>
            <button type="submit" class="cta-button primary" :disabled="submittingVehicle || !vehicleForm.vehicle_number">
              <span v-if="submittingVehicle" class="loading-spinner"></span>
              {{ submittingVehicle ? 'Saving...' : 'Save & Book Parking' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Logout Confirmation Modal -->
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
            <p>You'll need to sign in again to access your dashboard</p>
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

    <!-- Payment Modal -->
    <PaymentModal
      :is-visible="showPaymentModal"
      :reservation="currentReservation"
      :amount="currentReservation?.parking_cost"
      @close="closePaymentModal"
      @payment-success="handlePaymentSuccess"
    />

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
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api.js';
import PaymentModal from './PaymentModal.vue';

export default {
  name: 'UserDashboard',
  components: {
    PaymentModal
  },
  setup() {
    const router = useRouter();
    
    // Reactive data
    const currentUser = ref(null);
    const parkingLots = ref([]);
    const userReservations = ref([]);
    const loading = ref({
      lots: false,
      reservations: false
    });
    const booking = ref(false);
    const releasing = ref(false);
    const message = ref({ text: '', type: '' });

    // Vehicle modal state
    const showVehicleModal = ref(false);
    const submittingVehicle = ref(false);
    const pendingLot = ref(null); // Store the lot to book after vehicle number is provided
    const vehicleForm = ref({
      vehicle_number: ''
    });

    // Logout modal state
    const showLogoutModal = ref(false);

    // Mobile menu state
    const isMobileMenuOpen = ref(false);

    // Payment modal state
    const showPaymentModal = ref(false);
    const currentReservation = ref(null);

    // Custom confirmation modal states
    const showConfirmModal = ref(false)
    const confirmTitle = ref('')
    const confirmMessage = ref('')
    const confirmCallback = ref(null)

    // Computed properties
    const availableLots = computed(() => {
      return parkingLots.value.filter(lot => lot.available_slots > 0);
    });

    const activeReservations = computed(() => {
      const active = userReservations.value.filter(reservation => {
        // A reservation is active if:
        // 1. leaving_time is null (new system - unlimited until manual release), OR
        // 2. leaving_time is in the future (old system compatibility)
        const hasNoLeavingTime = !reservation.leaving_time || reservation.leaving_time === null;
        const hasFutureLeavingTime = reservation.leaving_time && new Date(reservation.leaving_time) > new Date();
        
        const isActive = hasNoLeavingTime || hasFutureLeavingTime;
        console.log(`Reservation ${reservation.id}: leaving=${reservation.leaving_time}, hasNoLeavingTime=${hasNoLeavingTime}, hasFutureLeavingTime=${hasFutureLeavingTime}, active=${isActive}`);
        
        return isActive;
      });
      
      console.log('Active reservations:', active);
      return active;
    });

    const totalReservations = computed(() => {
      return userReservations.value;
    });

    const sortedReservations = computed(() => {
      return [...userReservations.value].sort((a, b) => {
        return new Date(b.parking_time) - new Date(a.parking_time);
      });
    });

    const totalSpentMoney = computed(() => {
      return userReservations.value.reduce((total, reservation) => {
        // Only count completed reservations with a cost
        if (reservation.leaving_time && reservation.parking_cost) {
          return total + parseFloat(reservation.parking_cost);
        }
        return total;
      }, 0);
    });

    const getReservationStatus = (reservation) => {
      const now = new Date();
      const parkingTime = new Date(reservation.parking_time);
      
      // If no leaving time, it's active (new system)
      if (!reservation.leaving_time || reservation.leaving_time === null) {
        return 'Active';
      }
      
      const leavingTime = new Date(reservation.leaving_time);
      
      if (now < parkingTime) {
        return 'Scheduled';
      } else if (now >= parkingTime && now <= leavingTime) {
        return 'Active';
      } else {
        return 'Completed';
      }
    };

    // Methods
    const getCurrentUser = () => {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          currentUser.value = JSON.parse(userStr);
        }
      } catch (error) {
        console.error('Error getting current user:', error);
      }
    };

    const checkAuth = () => {
      const isLoggedIn = localStorage.getItem('isLoggedIn');
      const accessToken = localStorage.getItem('access_token');
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      
      console.log('Auth check:', {
        isLoggedIn,
        hasToken: !!accessToken,
        userRole: user?.role,
        userId: user?.id
      });

      if (!isLoggedIn || isLoggedIn !== 'true' || !accessToken || !user?.id) {
        showMessage('Please log in to access the dashboard', 'error');
        router.push('/login');
        return false;
      }
      
      return true;
    };

    const fetchParkingLots = async () => {
      loading.value.lots = true;
      try {
        const response = await api.getParkingLots();
        parkingLots.value = response.lots || response;
      } catch (error) {
        console.error('Error fetching parking lots:', error);
        showMessage('Error loading parking lots', 'error');
      } finally {
        loading.value.lots = false;
      }
    };

    const fetchUserReservations = async () => {
      if (!currentUser.value?.id) {
        console.log('No user ID available, skipping reservation fetch');
        userReservations.value = []; // Set empty array to avoid undefined issues
        return;
      }
      
      console.log('Fetching reservations for user:', currentUser.value);
      console.log('User ID:', currentUser.value.id, 'Type:', typeof currentUser.value.id);
      
      loading.value.reservations = true;
      try {
        const response = await api.getUserReservations(currentUser.value.id);
        userReservations.value = response.reservations || response || [];
        console.log('User reservations loaded:', userReservations.value);
      } catch (error) {
        console.error('Error fetching user reservations:', error);
        console.error('Error details:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
          message: error.message
        });
        
        // Set empty array on error to avoid undefined issues
        userReservations.value = [];
        
        // Only show error if it's a real authentication/permission issue
        if (error.response?.status === 403 || error.response?.status === 401) {
          showMessage('Access denied. Please log in again.', 'error');
        } else if (error.response?.status !== 404) {
          // Don't show error for 404 (no reservations found) - that's normal for new users
          const errorMsg = error.response?.data?.msg || error.message || 'Error loading reservations';
          showMessage(errorMsg, 'error');
        }
      } finally {
        loading.value.reservations = false;
      }
    };

    const selectParkingLot = async (lot) => {
      if (!checkAuth()) return;
      
      if (!currentUser.value?.id) {
        showMessage('Please log in to make a reservation', 'error');
        return;
      }

      if (activeReservations.value.length > 0) {
        showMessage('You already have an active parking session', 'error');
        return;
      }

      // Check if user has a vehicle number
      if (!currentUser.value.vehicle_number || currentUser.value.vehicle_number.trim() === '') {
        // Store the lot to book after vehicle number is provided
        pendingLot.value = lot;
        vehicleForm.value.vehicle_number = '';
        showVehicleModal.value = true;
        return;
      }

      // Proceed with booking if vehicle number exists
      await proceedWithBooking(lot);
    };

    const proceedWithBooking = async (lot) => {
      booking.value = true;
      try {
        console.log('Starting booking process for lot:', lot.id);
        
        // Use the new simplified booking API that automatically assigns a spot
        const response = await api.bookParkingSpot(lot.id);
        console.log('Booking response:', response);
        
        const reservation = response.reservation;
        showMessage(`Parking spot #${reservation.spot_id} booked successfully at ${reservation.lot_name}!`, 'success');
        
        // Refresh data
        await Promise.all([fetchParkingLots(), fetchUserReservations()]);
        
      } catch (error) {
        console.error('Error booking parking spot:', error);
        let errorMessage = 'Failed to book parking spot';
        
        if (error.response?.data?.msg) {
          errorMessage = error.response.data.msg;
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        showMessage(errorMessage, 'error');
      } finally {
        booking.value = false;
      }
    };

    const releaseParkingSpot = async (reservation) => {
      console.log('🔥 releaseParkingSpot function called!');
      console.log('Reservation data:', reservation);
      
      if (releasing.value) {
        console.log('Already releasing, returning');
        return;
      }
      
      // Show custom confirmation modal
      showConfirmation(
        'Release Parking Spot',
        `Are you sure you want to release parking spot #${reservation.spot_id}?`,
        () => {
          console.log('Calculating parking cost...');
          // Calculate parking cost
          const parkingCost = calculateParkingCost(reservation);
          console.log('Calculated cost:', parkingCost);
          
          // Show payment modal
          console.log('Setting current reservation and showing modal...');
          currentReservation.value = { ...reservation, parking_cost: parkingCost };
          showPaymentModal.value = true;
          console.log('Modal should be visible now. showPaymentModal.value:', showPaymentModal.value);
          console.log('currentReservation.value:', currentReservation.value);
        }
      );
    };

    const calculateEstimatedCost = (reservation) => {
      if (!reservation.parking_time) return 20; // Default minimum cost
      
      const startTime = new Date(reservation.parking_time);
      const now = new Date();
      const diffMs = now - startTime;
      const diffHours = Math.ceil(diffMs / (1000 * 60 * 60)); // Round up to next hour
      
      // Use the actual lot price from the reservation data, fallback to ₹10 per hour
      const costPerHour = reservation.lot_price || 10;
      // Keep minimum cost as ₹20 regardless of hourly rate
      const totalCost = Math.max(diffHours * costPerHour, 20);
      
      return totalCost;
    };

    const calculateParkingCost = (reservation) => {
      return calculateEstimatedCost(reservation);
    };

    const handlePaymentSuccess = async (paymentData) => {
      releasing.value = true;
      
      try {
        console.log('Calling API to release parking spot:', currentReservation.value.id);
        console.log('Payment data:', paymentData);
        
        // Prepare transaction data for backend
        const transactionData = {
          transactionId: paymentData.transactionId,
          paymentMethod: paymentData.paymentMethod
        }
        
        // Call the actual API to release the parking spot with transaction details
        const response = await api.releaseParkingSpot(currentReservation.value.id, transactionData);
        console.log('Release API response:', response);
        
        // Close payment modal
        showPaymentModal.value = false;
        currentReservation.value = null;
        
        // Show success message with transaction details
        showMessage(`Parking spot released successfully! Payment completed.\nTransaction ID: ${response.reservation?.transaction_id || paymentData.transactionId}`, 'success');
        
        // Refresh data to get updated state from backend
        await Promise.all([fetchParkingLots(), fetchUserReservations()]);
        
      } catch (err) {
        console.error('Error releasing parking spot:', err);
        
        // Close payment modal even on error
        showPaymentModal.value = false;
        currentReservation.value = null;
        
        // Show appropriate error message
        let errorMessage = 'Payment successful but failed to release booking. Please contact support.';
        if (err.response?.data?.msg) {
          errorMessage = `Payment successful but release failed: ${err.response.data.msg}`;
        } else if (err.message) {
          errorMessage = `Payment successful but release failed: ${err.message}`;
        }
        
        showMessage(errorMessage, 'error');
      } finally {
        releasing.value = false;
      }
    };

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

    const closePaymentModal = () => {
      showPaymentModal.value = false;
      currentReservation.value = null;
    };

    const refreshData = async () => {
      await Promise.all([fetchParkingLots(), fetchUserReservations()]);
      showMessage('Data refreshed successfully!', 'success');
    };

    const formatDateTime = (dateTime) => {
      if (!dateTime) return '-';
      try {
        return new Date(dateTime).toLocaleString('en-IN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        return '-';
      }
    };

    const calculateDuration = (startTime) => {
      if (!startTime) return '-';
      try {
        const start = new Date(startTime);
        const now = new Date();
        const diffMs = now - start;
        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        return `${hours}h ${minutes}m`;
      } catch (error) {
        return '-';
      }
    };

    const calculateCompletedDuration = (startTime, endTime) => {
      if (!startTime || !endTime) return '-';
      try {
        const start = new Date(startTime);
        const end = new Date(endTime);
        const diffMs = end - start;
        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        return `${hours}h ${minutes}m`;
      } catch (error) {
        return '-';
      }
    };

    const showMessage = (text, type = 'info') => {
      message.value = { text, type };
      setTimeout(() => {
        message.value = { text: '', type: '' };
      }, 5000);
    };

    const handleLogout = () => {
      showLogoutModal.value = true;
    };

    const confirmLogout = () => {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('access_token');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      localStorage.removeItem('email');
      localStorage.removeItem('role');
      showMessage('Logged out successfully', 'success');
      router.push('/login');
      showLogoutModal.value = false;
    };

    const cancelLogout = () => {
      showLogoutModal.value = false;
    };

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false;
    };

    // Vehicle Modal Functions
    const closeVehicleModal = () => {
      showVehicleModal.value = false;
      pendingLot.value = null;
      vehicleForm.value.vehicle_number = '';
    };

    const submitVehicleNumber = async () => {
      if (!vehicleForm.value.vehicle_number || !currentUser.value?.id) {
        showMessage('Please enter a valid vehicle number', 'error');
        return;
      }

      submittingVehicle.value = true;
      try {
        // Update user's vehicle number
        const updateData = {
          vehicle_number: vehicleForm.value.vehicle_number.trim().toUpperCase()
        };
        
        console.log('Updating user vehicle number:', updateData);
        const response = await api.updateUser(currentUser.value.id, updateData);
        console.log('Update response:', response);
        
        // Update local user data
        currentUser.value.vehicle_number = updateData.vehicle_number;
        localStorage.setItem('user', JSON.stringify(currentUser.value));
        
        showMessage('Vehicle number saved successfully!', 'success');
        
        // Close modal
        showVehicleModal.value = false;
        
        // Proceed with booking the pending lot
        if (pendingLot.value) {
          await proceedWithBooking(pendingLot.value);
          pendingLot.value = null;
        }
        
        vehicleForm.value.vehicle_number = '';
        
      } catch (error) {
        console.error('Error updating vehicle number:', error);
        let errorMessage = 'Failed to save vehicle number';
        
        if (error.response?.data?.msg) {
          errorMessage = error.response.data.msg;
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        showMessage(errorMessage, 'error');
      } finally {
        submittingVehicle.value = false;
      }
    };

    // Initialize component
    onMounted(async () => {
      console.log('UserDashboard mounted');
      
      // Check authentication first
      if (!checkAuth()) {
        return;
      }
      
      // Get current user info first
      getCurrentUser();
      console.log('User after getCurrentUser:', currentUser.value);
      
      // Wait a bit for user to be loaded, then fetch data
      setTimeout(async () => {
        try {
          console.log('Starting data fetch, user:', currentUser.value);
          await fetchParkingLots();
          
          // Only fetch reservations if we have a valid user ID
          if (currentUser.value?.id) {
            console.log('User ID is valid, fetching reservations for:', currentUser.value.id);
            await fetchUserReservations();
          } else {
            console.log('No valid user ID found, skipping reservation fetch');
          }
        } catch (error) {
          console.error('Error during data loading:', error);
        }
      }, 200); // Increased timeout to give more time for user loading
    });

    return {
      currentUser,
      parkingLots,
      userReservations,
      loading,
      booking,
      releasing,
      message,
      availableLots,
      activeReservations,
      totalReservations,
      sortedReservations,
      totalSpentMoney,
      selectParkingLot,
      releaseParkingSpot,
      refreshData,
      formatDateTime,
      calculateDuration,
      calculateCompletedDuration,
      getReservationStatus,
      handleLogout,
      confirmLogout,
      cancelLogout,
      toggleMobileMenu,
      closeMobileMenu,
      checkAuth,
      // Mobile menu
      isMobileMenuOpen,
      // Vehicle modal
      showVehicleModal,
      submittingVehicle,
      vehicleForm,
      closeVehicleModal,
      submitVehicleNumber,
      // Logout modal
      showLogoutModal,
      // Payment modal - ADDED THESE MISSING VARIABLES
      showPaymentModal,
      currentReservation,
      handlePaymentSuccess,
      closePaymentModal,
      calculateEstimatedCost,
      calculateParkingCost,
      // Custom confirmation modal
      showConfirmModal,
      confirmTitle,
      confirmMessage,
      confirmAction,
      cancelConfirmation
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Base Container */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.user-dashboard-container {
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
  background-color: rgba(0, 0, 0, 0.8);
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
  line-height: 1.1;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
  margin-bottom: 0.5rem;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 300;
}

/* Stats Section */
.stats-section {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
  text-align: center;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 168, 232, 0.6);
  box-shadow: 0 15px 35px rgba(0, 168, 232, 0.2);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
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
}

.stat-details .stat-number {
  font-size: 2.5rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 0.25rem;
  line-height: 1;
}

.stat-details .stat-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
}

/* Section Container */
.section-container {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
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
  background: linear-gradient(90deg, transparent, #00a8e8, transparent);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-actions {
  display: flex;
  gap: 0.75rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
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

/* Active Parking Cards */
.active-parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.active-parking-card {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
}

.active-parking-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);
}

.parking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.parking-location h3 {
  color: #ffffff;
  font-size: 1.3rem;
  margin-bottom: 0.25rem;
}

.parking-location p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.parking-details {
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
}

.detail-item i {
  color: #00a8e8;
  width: 16px;
}

.parking-actions {
  text-align: center;
}

/* Parking Lots Grid */
.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.lot-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
}

.lot-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 168, 232, 0.6);
  box-shadow: 0 15px 35px rgba(0, 168, 232, 0.2);
}

.lot-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.lot-name {
  color: #ffffff;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.lot-address {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.lot-pincode {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
}

.lot-price {
  text-align: right;
}

.price-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4ecdc4;
}

.price-unit {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.lot-stats {
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.75rem;
}

.stat-item i {
  color: #00a8e8;
}

.availability-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.availability-fill {
  height: 100%;
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  transition: width 0.3s ease;
}

/* CTA Buttons */
.cta-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
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

.cta-button.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.35);
  background: linear-gradient(135deg, #005fa3, #0094d1);
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.cta-button.secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.cta-button.full-width {
  width: 100%;
  justify-content: center;
}

.cta-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'Poppins', sans-serif;
}

.action-btn.release {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
}

.action-btn.release:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35);
}

/* Table Styles */
.table-container {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.data-table {
  overflow-x: auto;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
  color: #ffffff;
}

.data-table th {
  background: linear-gradient(135deg, rgba(0, 119, 190, 0.15), rgba(0, 168, 232, 0.05));
  padding: 1.5rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #00a8e8;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
}

.data-table td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  vertical-align: middle;
}

.data-table tr:hover {
  background: rgba(0, 168, 232, 0.05);
}

.location-cell {
  max-width: 200px;
}

.location-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.location-name {
  font-weight: 600;
  color: #ffffff;
}

.location-address {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

/* Badges */
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
}

.status-badge {
  text-transform: capitalize;
}

.status-badge.occupied,
.status-badge.active {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
}

.status-badge.available,
.status-badge.completed {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #ffffff;
}

.status-badge.cancelled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.spot-badge {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
}

.duration-badge {
  background: linear-gradient(135deg, #ffd93d, #ff9a3c);
  color: #000;
}

.ongoing-badge {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
}

.price-badge {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #ffffff;
  font-weight: 600;
}

/* Loading and Empty States */
.loading-state {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 168, 232, 0.3);
  border-left: 4px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.7);
}

.empty-state i {
  font-size: 3rem;
  color: #00a8e8;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
}

/* Message Toast */
.message-toast {
  position: fixed;
  top: 100px;
  right: 2rem;
  z-index: 10000;
  padding: 1rem 1.5rem;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  animation: slideIn 0.3s ease-out;
}

.message-toast.success {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #ffffff;
}

.message-toast.error {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: modalFadeIn 0.3s ease-out;
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
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.4s ease-out;
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
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-title-section h3 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.5rem;
}

.modal-title-section p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
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

/* Form Styles */
.modal-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #00a8e8;
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(0, 168, 232, 0.2);
  border-radius: 15px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #00a8e8;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(0, 168, 232, 0.2);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-hint {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  margin-top: 0.5rem;
  display: block;
}

.modal-footer {
  padding: 1.5rem 2rem 2rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Logout Modal Specific Styles */
.logout-modal {
  max-width: 450px;
}

.logout-modal-content {
  padding: 2rem;
  text-align: center;
}

.logout-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: logoutIconPulse 2s ease-in-out infinite;
}

.logout-icon i {
  font-size: 2.5rem;
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
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.logout-message p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
}

.logout-confirm-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f) !important;
  border-color: #ff6b6b !important;
}

.logout-confirm-btn:hover {
  background: linear-gradient(135deg, #ff5252, #e53e3e) !important;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35) !important;
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
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .lots-grid {
    grid-template-columns: 1fr;
  }
  
  .active-parking-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .data-table {
    font-size: 0.85rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.75rem 0.5rem;
  }
  
  .message-toast {
    right: 1rem;
    left: 1rem;
  }
  
  .modal-container {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-header {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .modal-form {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem 1.5rem;
    flex-direction: column;
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
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .section-container {
    padding: 1.5rem;
  }
  
  .lot-card,
  .active-parking-card {
    padding: 1.5rem;
  }
}

/* Custom Confirmation Modal */
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

.alert-header.warning {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
  border-bottom-color: rgba(255, 193, 7, 0.2);
}

.alert-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ffc107;
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
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

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
</style>