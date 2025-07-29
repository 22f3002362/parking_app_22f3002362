<template>
  <div class="find-parking-container">
    <!-- Navigation Bar -->
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
        
        <div class="navbar-menu desktop-menu">
          <div class="nav-links">
            <router-link to="/user-dashboard" class="nav-link">
              <i class="bi bi-house"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/find-parking" class="nav-link active">
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
          <h1 class="main-title">Find Your Perfect Parking Spot</h1>
          <p class="hero-subtitle">Search and book from our extensive network of parking facilities</p>
        </div>
      </div>

      <!-- Search Section -->
      <div class="search-section">
        <div class="search-container">
          <div class="search-header">
            <h2 class="search-title">
              <i class="bi bi-search"></i>
              Search Parking Lots
            </h2>
            <p class="search-subtitle">Find parking by location or availability</p>
          </div>
          
          <div class="search-filters">
            <div class="filter-group">
              <label for="location-search">Location</label>
              <div class="search-input-group">
                <i class="bi bi-geo-alt"></i>
                <input 
                  type="text" 
                  id="location-search"
                  v-model="searchFilters.location" 
                  placeholder="Search by location name or pincode..."
                  @input="handleSearch"
                />
              </div>
            </div>
            
            <div class="filter-group">
              <label for="availability">Availability</label>
              <div class="select-group">
                <select v-model="searchFilters.availability" @change="handleSearch">
                  <option value="">All Lots</option>
                  <option value="available">Available Only</option>
                  <option value="full">Full Lots</option>
                </select>
              </div>
            </div>
            
            <div class="filter-actions">
              <button class="clear-btn" @click="clearFilters">
                <i class="bi bi-x-circle"></i>
                Clear
              </button>
              <button class="search-btn" @click="handleSearch">
                <i class="bi bi-search"></i>
                Search
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Summary -->
      <div class="results-summary" v-if="!loading">
        <div class="summary-info">
          <h3>
            <i class="bi bi-list-ul"></i>
            {{ filteredLots.length }} Parking {{ filteredLots.length === 1 ? 'Lot' : 'Lots' }} Found
          </h3>
          <p v-if="isFiltering">Showing filtered results</p>
          <p v-else>Showing all available parking lots</p>
        </div>
        
        <div class="sort-options">
          <label>Sort by:</label>
          <select v-model="sortBy" @change="handleSort">
            <option value="distance">Distance</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="availability">Availability</option>
            <option value="name">Name</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Searching for parking lots...</p>
      </div>

      <!-- Parking Lots Grid -->
      <div v-else-if="filteredLots.length > 0" class="lots-grid">
        <div v-for="lot in sortedLots" :key="lot.id" class="lot-card detailed">
          <div class="lot-header">
            <div class="lot-main-info">
              <h3 class="lot-name">{{ lot.location_name }}</h3>
              <div class="lot-location">
                <i class="bi bi-geo-alt"></i>
                <span class="address">{{ lot.address }}</span>
                <span class="pincode-badge">{{ lot.pincode }}</span>
              </div>
            </div>
            <div class="lot-price-section">
              <div class="price-display">
                <span class="price-amount">₹{{ lot.price }}</span>
                <span class="price-unit">/hour</span>
              </div>
              <div class="availability-status" :class="getAvailabilityClass(lot)">
                <i :class="getAvailabilityIcon(lot)"></i>
                <span>{{ getAvailabilityText(lot) }}</span>
              </div>
            </div>
          </div>

          <div class="lot-details">
            <div class="detail-row">
              <div class="detail-item">
                <i class="bi bi-car-front"></i>
                <span class="detail-label">Total Spots:</span>
                <span class="detail-value">{{ lot.number_of_slots }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-check-circle"></i>
                <span class="detail-label">Available:</span>
                <span class="detail-value available-count">{{ lot.available_slots }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-x-circle"></i>
                <span class="detail-label">Occupied:</span>
                <span class="detail-value occupied-count">{{ lot.number_of_slots - lot.available_slots }}</span>
              </div>
            </div>
            
            <div class="availability-visual">
              <div class="availability-bar">
                <div 
                  class="availability-fill"
                  :style="{ width: (lot.available_slots / lot.number_of_slots * 100) + '%' }"
                ></div>
              </div>
              <div class="availability-text">
                {{ Math.round((lot.available_slots / lot.number_of_slots) * 100) }}% Available
              </div>
            </div>
          </div>

          <div class="lot-actions">
            <div class="action-info">
              <div class="booking-info" v-if="lot.available_slots > 0">
                <i class="bi bi-info-circle"></i>
                <span>Instant booking available</span>
              </div>
              <div class="booking-info unavailable" v-else>
                <i class="bi bi-exclamation-triangle"></i>
                <span>Currently full</span>
              </div>
            </div>
            
            <button 
              class="book-btn"
              :class="{ 'primary': lot.available_slots > 0, 'disabled': lot.available_slots === 0 }"
              @click="bookParkingSpot(lot)"
              :disabled="lot.available_slots === 0 || booking"
            >
              <i class="bi bi-car-front-fill"></i>
              {{ lot.available_slots === 0 ? 'Full' : (booking ? 'Booking...' : 'Book Now') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <i class="bi bi-search"></i>
        <h3>No parking lots found</h3>
        <p v-if="isFiltering">Try adjusting your search filters</p>
        <p v-else>No parking lots are currently available</p>
        <button class="cta-button primary" @click="clearFilters" v-if="isFiltering">
          <i class="bi bi-arrow-clockwise"></i>
          Clear Filters
        </button>
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
  name: 'FindParking',
  setup() {
    const router = useRouter();
    
    // Reactive data
    const currentUser = ref(null);
    const parkingLots = ref([]);
    const loading = ref(false);
    const booking = ref(false);
    const message = ref({ text: '', type: '' });
    const isMobileMenuOpen = ref(false);
    
    // Search and filter state
    const searchFilters = ref({
      location: '',
      availability: ''
    });
    const sortBy = ref('distance');

    // Computed properties
    const isFiltering = computed(() => {
      return searchFilters.value.location || 
             searchFilters.value.availability;
    });

    const filteredLots = computed(() => {
      let filtered = [...parkingLots.value];

      // Filter by location (name, address, or pincode)
      if (searchFilters.value.location) {
        const searchTerm = searchFilters.value.location.toLowerCase();
        filtered = filtered.filter(lot => 
          lot.location_name.toLowerCase().includes(searchTerm) ||
          lot.address.toLowerCase().includes(searchTerm) ||
          lot.pincode.includes(searchTerm)
        );
      }

      // Filter by availability
      if (searchFilters.value.availability === 'available') {
        filtered = filtered.filter(lot => lot.available_slots > 0);
      } else if (searchFilters.value.availability === 'full') {
        filtered = filtered.filter(lot => lot.available_slots === 0);
      }

      return filtered;
    });

    const sortedLots = computed(() => {
      let sorted = [...filteredLots.value];

      switch (sortBy.value) {
        case 'price-low':
          sorted.sort((a, b) => a.price - b.price);
          break;
        case 'price-high':
          sorted.sort((a, b) => b.price - a.price);
          break;
        case 'availability':
          sorted.sort((a, b) => b.available_slots - a.available_slots);
          break;
        case 'name':
          sorted.sort((a, b) => a.location_name.localeCompare(b.location_name));
          break;
        case 'distance':
        default:
          // For now, keep original order (could implement geolocation later)
          break;
      }

      return sorted;
    });

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
      
      if (!isLoggedIn || isLoggedIn !== 'true' || !accessToken || !user?.id) {
        showMessage('Please log in to access parking search', 'error');
        router.push('/login');
        return false;
      }
      
      return true;
    };

    const fetchParkingLots = async () => {
      loading.value = true;
      try {
        const response = await api.getParkingLots();
        parkingLots.value = response.lots || response;
      } catch (error) {
        console.error('Error fetching parking lots:', error);
        showMessage('Error loading parking lots', 'error');
      } finally {
        loading.value = false;
      }
    };

    const handleSearch = () => {
      // Search is reactive through computed properties
      console.log('Search filters applied:', searchFilters.value);
    };

    const handleSort = () => {
      console.log('Sorting by:', sortBy.value);
    };

    const clearFilters = () => {
      searchFilters.value = {
        location: '',
        availability: ''
      };
      sortBy.value = 'distance';
    };

    const getAvailabilityClass = (lot) => {
      if (lot.available_slots === 0) return 'full';
      if (lot.available_slots <= lot.number_of_slots * 0.2) return 'low';
      return 'available';
    };

    const getAvailabilityIcon = (lot) => {
      if (lot.available_slots === 0) return 'bi bi-x-circle-fill';
      if (lot.available_slots <= lot.number_of_slots * 0.2) return 'bi bi-exclamation-triangle-fill';
      return 'bi bi-check-circle-fill';
    };

    const getAvailabilityText = (lot) => {
      if (lot.available_slots === 0) return 'Full';
      if (lot.available_slots <= lot.number_of_slots * 0.2) return 'Limited';
      return 'Available';
    };

    const bookParkingSpot = async (lot) => {
      if (!checkAuth()) return;
      
      if (!currentUser.value?.id) {
        showMessage('Please log in to make a reservation', 'error');
        return;
      }

      if (lot.available_slots === 0) {
        showMessage('This parking lot is currently full', 'error');
        return;
      }

      booking.value = true;
      try {
        console.log('Starting booking process for lot:', lot.id);
        
        const response = await api.bookParkingSpot(lot.id);
        console.log('Booking response:', response);
        
        const reservation = response.reservation;
        showMessage(`Parking spot #${reservation.spot_id} booked successfully at ${reservation.lot_name}!`, 'success');
        
        // Refresh parking lots data
        await fetchParkingLots();
        
        // Optionally redirect to dashboard after booking
        setTimeout(() => {
          router.push('/user-dashboard');
        }, 2000);
        
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
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    const closeMobileMenu = () => {
      isMobileMenuOpen.value = false;
    };

    // Initialize component
    onMounted(async () => {
      console.log('FindParking component mounted');
      
      if (!checkAuth()) {
        return;
      }
      
      getCurrentUser();
      await fetchParkingLots();
    });

    return {
      currentUser,
      parkingLots,
      loading,
      booking,
      message,
      searchFilters,
      sortBy,
      isFiltering,
      filteredLots,
      sortedLots,
      isMobileMenuOpen,
      handleSearch,
      handleSort,
      clearFilters,
      getAvailabilityClass,
      getAvailabilityIcon,
      getAvailabilityText,
      bookParkingSpot,
      handleLogout,
      toggleMobileMenu,
      closeMobileMenu
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

.find-parking-container {
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

/* Search Section */
.search-section {
  margin-bottom: 3rem;
}

.search-container {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
}

.search-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00a8e8, transparent);
}

.search-header {
  text-align: center;
  margin-bottom: 2rem;
}

.search-title {
  font-size: 2rem;
  font-weight: 600;
  color: #00a8e8;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.search-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.search-filters {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1.5rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #ffffff;
  font-size: 0.9rem;
}

.search-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input-group i {
  position: absolute;
  left: 1rem;
  color: #00a8e8;
  z-index: 2;
}

.search-input-group input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
}

.search-input-group input:focus {
  outline: none;
  border-color: #00a8e8;
  box-shadow: 0 0 0 2px rgba(0, 168, 232, 0.2);
}

.search-input-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.select-group select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-group select:focus {
  outline: none;
  border-color: #00a8e8;
  box-shadow: 0 0 0 2px rgba(0, 168, 232, 0.2);
}

.select-group select option {
  background: #1a2d43;
  color: #ffffff;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
}

.clear-btn,
.search-btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'Poppins', sans-serif;
}

.clear-btn {
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid rgba(255, 107, 107, 0.25);
  color: #ff6b6b;
}

.clear-btn:hover {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
  transform: translateY(-1px);
}

.search-btn {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.2);
}

.search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.35);
}

/* Results Summary */
.results-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-info h3 {
  color: #ffffff;
  font-size: 1.3rem;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.summary-info p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
}

.sort-options select {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
}

.sort-options select option {
  background: #1a2d43;
  color: #ffffff;
}

/* Parking Lots Grid */
.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.lot-card.detailed {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  padding: 2rem;
  transition: all 0.3s ease;
}

.lot-card.detailed:hover {
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

.lot-main-info .lot-name {
  color: #ffffff;
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.lot-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.lot-location i {
  color: #00a8e8;
}

.lot-location .address {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.lot-location .pincode-badge {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
}

.lot-price-section {
  text-align: right;
}

.price-display {
  margin-bottom: 0.5rem;
}

.price-amount {
  font-size: 1.8rem;
  font-weight: 700;
  color: #4ecdc4;
}

.price-unit {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.availability-status {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.availability-status.available {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #ffffff;
}

.availability-status.low {
  background: linear-gradient(135deg, #ffd93d, #ff9a3c);
  color: #000;
}

.availability-status.full {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
}

/* Lot Details */
.lot-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}

.detail-item i {
  color: #00a8e8;
  width: 16px;
}

.detail-label {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.detail-value {
  color: #ffffff;
  font-weight: 600;
}

.detail-value.available-count {
  color: #4ecdc4;
}

.detail-value.occupied-count {
  color: #ff6b6b;
}

.availability-visual {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.availability-bar {
  flex: 1;
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

.availability-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  min-width: 80px;
}

/* Lot Actions */
.lot-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-info {
  display: flex;
  align-items: center;
}

.booking-info {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
}

.booking-info:not(.unavailable) {
  background: rgba(78, 205, 196, 0.15);
  color: #4ecdc4;
}

.booking-info.unavailable {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
}

.book-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Poppins', sans-serif;
  min-width: 120px;
  justify-content: center;
}

.book-btn.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.2);
}

.book-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.35);
}

.book-btn.disabled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  cursor: not-allowed;
}

.book-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Loading and Empty States */
.loading-state {
  text-align: center;
  padding: 4rem;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(0, 168, 232, 0.3);
  border-left: 4px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 4rem;
  color: rgba(255, 255, 255, 0.7);
}

.empty-state i {
  font-size: 4rem;
  color: #00a8e8;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.empty-state p {
  margin-bottom: 1.5rem;
}

.cta-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Poppins', sans-serif;
  text-decoration: none;
}

.cta-button.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.2);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.35);
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
@media (max-width: 1024px) {
  .search-filters {
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  .filter-actions {
    grid-column: span 2;
    justify-content: center;
  }
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
  
  .user-info {
    display: none;
  }
  
  .logout-btn span {
    display: none;
  }
  
  .main-content {
    padding: 1rem;
    padding-top: 80px;
  }
  
  .search-filters {
    grid-template-columns: 1fr;
  }
  
  .filter-actions {
    grid-column: span 1;
  }
  
  .lots-grid {
    grid-template-columns: 1fr;
  }
  
  .results-summary {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .message-toast {
    right: 1rem;
    left: 1rem;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .lot-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .lot-price-section {
    text-align: left;
  }
  
  .lot-actions {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
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
  
  .search-container {
    padding: 1.5rem;
  }
  
  .lot-card.detailed {
    padding: 1.5rem;
  }
}
</style>
