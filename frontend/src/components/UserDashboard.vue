<template>
  <div class="user-dashboard-container">
    <!-- User Navbar -->
    <nav class="user-navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <div class="brand-logo">P</div>
          <div class="brand-info">
            <h3 class="brand-name">ParkEase</h3>
            <span class="brand-subtitle">User Portal</span>
          </div>
        </div>
        
        <div class="navbar-menu">
          <div class="nav-links">
            <router-link to="/user-dashboard" class="nav-link active">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <a href="#parking-lots" class="nav-link">
              <i class="bi bi-geo-alt-fill"></i>
              <span>Find Parking</span>
            </a>
            <a href="#my-bookings" class="nav-link">
              <i class="bi bi-bookmark-check"></i>
              <span>My Bookings</span>
            </a>
          </div>
          
          <div class="navbar-actions">
            <div class="user-profile">
              <div class="profile-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
              <div class="profile-info">
                <span class="profile-name">{{ currentUser?.username || 'User' }}</span>
                <span class="profile-role">Member</span>
              </div>
            </div>
            <button class="logout-btn" @click="handleLogout" title="Logout">
              <i class="bi bi-box-arrow-right"></i>
            </button>
          </div>
        </div>
        
        <div class="mobile-menu-toggle" @click="toggleMobileMenu">
          <i class="bi bi-list"></i>
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
          <h1 class="main-title">Welcome to ParkEase</h1>
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
                <span>Expires: {{ formatDateTime(reservation.leaving_time) }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-currency-rupee"></i>
                <span>Cost: ₹{{ reservation.parking_cost || '0' }}</span>
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
          <button class="cta-button primary" @click="refreshData">
            <i class="bi bi-arrow-clockwise"></i>
            Refresh
          </button>
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
                  <td>{{ reservation.leaving_time ? formatDateTime(reservation.leaving_time) : '-' }}</td>
                  <td>
                    <span v-if="reservation.leaving_time" class="badge duration-badge">
                      {{ calculateCompletedDuration(reservation.parking_time, reservation.leaving_time) }}
                    </span>
                    <span v-else class="badge ongoing-badge">Ongoing</span>
                  </td>
                  <td>
                    <span class="badge price-badge">
                      ₹{{ reservation.parking_cost || '0' }}
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
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api.js';

export default {
  name: 'UserDashboard',
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

    // Computed properties
    const availableLots = computed(() => {
      return parkingLots.value.filter(lot => lot.available_slots > 0);
    });

    const activeReservations = computed(() => {
      const active = userReservations.value.filter(reservation => {
        // A reservation is active if the leaving time is in the future
        // This allows users to release their parking anytime before the scheduled end
        const now = new Date();
        const leavingTime = new Date(reservation.leaving_time);
        
        const isActive = leavingTime > now;
        console.log(`Reservation ${reservation.id}: leaving=${reservation.leaving_time}, now=${now.toISOString()}, active=${isActive}`);
        
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

    const getReservationStatus = (reservation) => {
      const now = new Date();
      const parkingTime = new Date(reservation.parking_time);
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

      booking.value = true;
      try {
        console.log('Starting reservation process for lot:', lot.id);
        
        // First, get available spots for this parking lot
        const availableSpotsResponse = await api.getAvailableSpots(lot.id);
        console.log('Available spots response:', availableSpotsResponse);
        
        const availableSpots = availableSpotsResponse.available_spots || [];
        
        if (availableSpots.length === 0) {
          showMessage('No parking spots available in this lot', 'error');
          return;
        }

        // Get the first available spot
        const selectedSpot = availableSpots[0];
        console.log('Selected spot:', selectedSpot);

        // Create reservation with proper format expected by backend
        const now = new Date();
        const parkingTime = now.toISOString();
        // Set a default leaving time (e.g., 8 hours from now) to give users plenty of time
        const leavingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000).toISOString();

        const reservationData = {
          spot_id: selectedSpot.id,
          user_id: currentUser.value.id,
          parking_time: parkingTime,
          leaving_time: leavingTime
        };

        console.log('Creating reservation with data:', reservationData);
        const response = await api.createReservation(reservationData);
        console.log('Reservation response:', response);
        
        showMessage(`Parking spot #${selectedSpot.id} reserved successfully!`, 'success');
        
        // Refresh data
        await Promise.all([fetchParkingLots(), fetchUserReservations()]);
        
      } catch (error) {
        console.error('Error creating reservation:', error);
        let errorMessage = 'Failed to reserve parking spot';
        
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
      if (!checkAuth()) return;
      
      releasing.value = true;
      try {
        console.log('Releasing reservation:', reservation);
        
        // Cancel the reservation
        const response = await api.cancelReservation(reservation.id);
        console.log('Cancel reservation response:', response);
        
        showMessage('Parking spot released successfully!', 'success');
        
        // Refresh data
        await Promise.all([fetchParkingLots(), fetchUserReservations()]);
        
      } catch (error) {
        console.error('Error releasing parking spot:', error);
        console.error('Error details:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
          message: error.message
        });
        
        let errorMessage = 'Failed to release parking spot';
        if (error.response?.data?.msg) {
          errorMessage = error.response.data.msg;
        } else if (error.response?.status === 404) {
          errorMessage = 'Reservation not found';
        } else if (error.response?.status === 403) {
          errorMessage = 'Access denied - you can only release your own reservations';
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        showMessage(errorMessage, 'error');
      } finally {
        releasing.value = false;
      }
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
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('access_token');
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      localStorage.removeItem('email');
      localStorage.removeItem('role');
      router.push('/login');
    };

    const toggleMobileMenu = () => {
      // Mobile menu toggle functionality
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
      selectParkingLot,
      releaseParkingSpot,
      refreshData,
      formatDateTime,
      calculateDuration,
      calculateCompletedDuration,
      getReservationStatus,
      handleLogout,
      toggleMobileMenu,
      checkAuth
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-brand .brand-logo {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 900;
  color: #ffffff;
  box-shadow: 0 8px 16px rgba(0, 168, 232, 0.3);
}

.brand-info .brand-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.brand-info .brand-subtitle {
  font-size: 0.8rem;
  color: #00a8e8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link:hover, .nav-link.active, .nav-link.router-link-active {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 168, 232, 0.3);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-avatar {
  font-size: 1.3rem;
  color: #00a8e8;
}

.profile-info .profile-name {
  font-weight: 600;
  color: #ffffff;
  display: block;
  font-size: 0.8rem;
}

.profile-info .profile-role {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logout-btn {
  padding: 0.5rem;
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid rgba(255, 107, 107, 0.25);
  color: #ff6b6b;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
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
  font-weight: 800;
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

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
    padding-top: 80px;
  }
  
  .navbar-content {
    padding: 0.5rem 1rem;
  }
  
  .nav-links {
    display: none;
  }
  
  .mobile-menu-toggle {
    display: flex;
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
}

@media (max-width: 480px) {
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
</style>