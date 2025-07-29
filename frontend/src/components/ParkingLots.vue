<template>
  <div class="parking-lots-container">
    <!-- Admin Navbar -->
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
        
        <!-- Desktop Menu -->
        <div class="navbar-menu desktop-menu">
          <div class="nav-links">
            <router-link to="/admin-dashboard" class="nav-link">
              <i class="bi bi-speedometer2"></i>
              <span>Dashboard</span>
            </router-link>
            <router-link to="/parking-lots" class="nav-link active">
              <i class="bi bi-geo-alt-fill"></i>
              <span>Parking Lots</span>
            </router-link>
            <router-link to="/manage-users" class="nav-link">
              <i class="bi bi-people-fill"></i>
              <span>Users</span>
            </router-link>
            <a href="/admin-reports" class="nav-link">
              <i class="bi bi-graph-up"></i>
              <span>Reports</span>
            </a>
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
            <a href="/admin-reports" class="mobile-nav-link" @click="closeMobileMenu">
              <i class="bi bi-graph-up"></i>
              <span>Reports</span>
            </a>
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

    <!-- My custom background is under this iv -->
    <div class="bg-animation">
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">Parking Lots</h1>
        </div>
      </div>

      <!-- Parking Lots Section -->
      <div class="section-container">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-geo-alt-fill"></i>
              All Parking Lots
            </h2>
            <p class="section-subtitle">View detailed information about each parking facility and slot availability</p>
          </div>
          <div class="section-actions">
            <button class="cta-button primary" @click="refreshLots">
              <i class="bi bi-arrow-clockwise"></i>
              Refresh
            </button>
            <button class="cta-button secondary" @click="openAddLotModal">
              <i class="bi bi-plus-circle"></i>
              Add Parking Lot
            </button>
          </div>
        </div>

        <div class="lots-container">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading parking lots...</p>
          </div>
          
          <div v-else-if="error" class="error-state">
            <i class="bi bi-exclamation-triangle"></i>
            <h3>Error Loading Parking Lots</h3>
            <p>{{ error }}</p>
            <button class="cta-button primary" @click="refreshLots">
              <i class="bi bi-arrow-clockwise"></i>
              Try Again
            </button>
          </div>
          
          <div v-else-if="lots.length === 0" class="empty-state">
            <i class="bi bi-geo-alt"></i>
            <h3>No parking lots found</h3>
            <p>No parking lots have been created yet</p>
          </div>
          
          <div v-else class="lots-grid">
            <div 
              v-for="lot in lots" 
              :key="lot.id" 
              class="lot-card"
              @click="viewLotDetails(lot)"
            >
              <div class="lot-header">
                <div class="lot-icon">
                  <i class="bi bi-geo-alt-fill"></i>
                </div>
                <div class="lot-status" :class="getAvailabilityStatus(lot)">
                  {{ getAvailabilityText(lot) }}
                </div>
              </div>
              
              <div class="lot-info">
                <h3 class="lot-name">{{ lot.location_name }}</h3>
                <p class="lot-address">{{ lot.address }}</p>
                <div class="lot-meta">
                  <span class="pincode">{{ lot.pincode }}</span>
                  <span class="price">₹{{ lot.price }}/hr</span>
                </div>
              </div>
              
              <div class="lot-stats">
                <div class="stat-item">
                  <div class="stat-number">{{ lot.number_of_slots }}</div>
                  <div class="stat-label">Total Spots</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number available">{{ lot.available_slots }}</div>
                  <div class="stat-label">Available</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number occupied">{{ lot.number_of_slots - lot.available_slots }}</div>
                  <div class="stat-label">Occupied</div>
                </div>
              </div>
              
              <div class="lot-visual">
                <div class="slots-preview">
                  <div class="slots-header">Slot Preview</div>
                  <div class="slots-grid">
                    <div 
                      v-for="n in Math.min(lot.number_of_slots, 20)" 
                      :key="n" 
                      class="slot-mini"
                      :class="n <= lot.available_slots ? 'available' : 'occupied'"
                    >
                      <i :class="n <= lot.available_slots ? 'bi bi-car-front' : 'bi bi-car-front-fill'"></i>
                    </div>
                    <div v-if="lot.number_of_slots > 20" class="more-slots">
                      +{{ lot.number_of_slots - 20 }} more
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="lot-actions">
                <button class="action-button primary full-width" @click.stop="viewLotDetails(lot)">
                  <i class="bi bi-eye"></i>
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Parking Lot Modal -->
    <div v-if="showAddLotModal" class="modal-overlay" @click="closeAddLotModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>{{ isEditMode ? 'Edit Parking Lot' : 'Add New Parking Lot' }}</h3>
            <p>{{ isEditMode ? 'Update parking lot details' : 'Create a new parking facility' }}</p>
          </div>
          <button class="close-btn" @click="closeAddLotModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <form @submit.prevent="submitLot" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-geo-alt"></i>
                Location Name
              </label>
              <input
                v-model="lotForm.location_name"
                type="text"
                class="form-input"
                placeholder="Enter location name"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-currency-rupee"></i>
                Price per Hour (₹)
              </label>
              <input
                v-model.number="lotForm.price"
                type="number"
                min="1"
                step="1"
                class="form-input"
                placeholder="Enter price per hour"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <i class="bi bi-map"></i>
              Address
            </label>
            <textarea
              v-model="lotForm.address"
              class="form-input"
              rows="3"
              placeholder="Enter complete address"
              required
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-pin-map"></i>
                Pincode
              </label>
              <input
                v-model="lotForm.pincode"
                type="text"
                pattern="[0-9]{6}"
                maxlength="6"
                class="form-input"
                placeholder="Enter 6-digit pincode"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-car-front"></i>
                Number of Slots
              </label>
              <input
                v-model.number="lotForm.number_of_slots"
                type="number"
                min="1"
                max="500"
                class="form-input"
                placeholder="Enter number of parking slots"
                required
                :disabled="isEditMode"
              />
              <small v-if="isEditMode" class="form-hint">Cannot change slot count when editing</small>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn secondary" @click="closeAddLotModal">
              <i class="bi bi-x-circle"></i>
              Cancel
            </button>
            <button type="submit" class="btn primary" :disabled="lotFormLoading">
              <i v-if="lotFormLoading" class="loading-icon bi bi-arrow-clockwise"></i>
              <i v-else :class="isEditMode ? 'bi bi-check-circle' : 'bi bi-plus-circle'"></i>
              {{ isEditMode ? 'Update Lot' : 'Create Lot' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-container delete-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>Delete Parking Lot</h3>
            <p>This action cannot be undone</p>
          </div>
          <button class="close-btn" @click="closeDeleteModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="modal-content">
          <div class="delete-warning">
            <i class="bi bi-exclamation-triangle warning-icon"></i>
            <h4>Are you sure you want to delete "{{ lotToDelete?.location_name }}"?</h4>
            <p>This will permanently remove the parking lot and all its associated data.</p>
            
            <div class="lot-details">
              <div class="detail-item">
                <strong>Address:</strong> {{ lotToDelete?.address }}
              </div>
              <div class="detail-item">
                <strong>Total Slots:</strong> {{ lotToDelete?.number_of_slots }}
              </div>
              <div class="detail-item">
                <strong>Occupied Slots:</strong> {{ lotToDelete ? (lotToDelete.number_of_slots - lotToDelete.available_slots) : 0 }}
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn secondary" @click="closeDeleteModal">
              <i class="bi bi-x-circle"></i>
              Cancel
            </button>
            <button type="button" class="btn danger" @click="confirmDelete" :disabled="deleteLoading">
              <i v-if="deleteLoading" class="loading-icon bi bi-arrow-clockwise"></i>
              <i v-else class="bi bi-trash"></i>
              Delete Lot
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slot Details Popup -->
    <div v-if="showSlotDetailsModal" class="popup-overlay" @click="closeSlotDetailsModal">
      <div class="slot-popup" @click.stop>
        <div class="popup-header">
          <h4>Slot {{ selectedSlotDetails?.number ? String(selectedSlotDetails.number).padStart(2, '0') : '' }}</h4>
          <button class="popup-close" @click="closeSlotDetailsModal">
            <i class="bi bi-x"></i>
          </button>
        </div>

        <div class="popup-content" v-if="selectedSlotDetails">
          <!-- Loading State -->
          <div v-if="selectedSlotDetails.loading" class="popup-loading">
            <div class="mini-spinner"></div>
            <span>Loading...</span>
          </div>
          
          <!-- Error State -->
          <div v-else-if="selectedSlotDetails.error" class="popup-error">
            <i class="bi bi-exclamation-triangle"></i>
            <span>{{ selectedSlotDetails.error }}</span>
          </div>
          
          <!-- Slot Details -->
          <div v-else class="popup-details">
            <!-- Status Badge -->
            <div class="popup-status" :class="selectedSlotDetails.status">
              <i :class="getStatusIcon(selectedSlotDetails.status)"></i>
              <span>{{ getStatusText(selectedSlotDetails.status) }}</span>
            </div>

            <!-- Available Slot Info -->
            <div v-if="selectedSlotDetails.status === 'available'" class="popup-available">
              <div class="popup-message">This slot is available for booking</div>
              <div class="popup-rate">₹{{ selectedLot?.price || 0 }}/hour</div>
            </div>

            <!-- Occupied Slot Info -->
            <div v-else-if="selectedSlotDetails.status === 'occupied'" class="popup-occupied">
              <!-- Show user details if available -->
              <div v-if="selectedSlotDetails.user" class="user-info">
              <div class="info-row">
                <i class="bi bi-person"></i>
                <span>{{ selectedSlotDetails.user.username || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <i class="bi bi-envelope"></i>
                <span>{{ selectedSlotDetails.user.email || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <i class="bi bi-telephone"></i>
                <span>{{ selectedSlotDetails.user.phone_number || 'N/A' }}</span>
              </div>
              <div class="info-row vehicle">
                <i class="bi bi-car-front"></i>
                <span>{{ selectedSlotDetails.user.vehicle_number || 'N/A' }}</span>
              </div>
              </div>
              
              <!-- Show booking time if available -->
              <div v-if="selectedSlotDetails.booking_time || selectedSlotDetails.created_at" class="booking-time">
              <i class="bi bi-clock"></i>
              <span>Booked: {{ formatBookingTime() }}</span>
              </div>
              
              <!-- Show duration if available -->
              <div v-if="selectedSlotDetails.booking_time || selectedSlotDetails.created_at" class="booking-time">
              <i class="bi bi-stopwatch"></i>
              <span>Duration: {{ calculateDuration() }}</span>
              </div>
              
              <!-- Show generic occupied message if no user details -->
              <div v-if="!selectedSlotDetails.user" class="popup-message">
              This slot is currently occupied
              </div>
              
              <div class="popup-rate">₹{{ selectedLot?.price || 0 }}/hour</div>
            </div>

            <!-- Reserved Slot Info -->
            <div v-else-if="selectedSlotDetails.status === 'reserved'" class="popup-reserved">
              <!-- Show user details if available -->
              <div v-if="selectedSlotDetails.user" class="user-info">
              <div class="info-row">
                <i class="bi bi-person"></i>
                <span>{{ selectedSlotDetails.user.username || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <i class="bi bi-envelope"></i>
                <span>{{ selectedSlotDetails.user.email || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <i class="bi bi-telephone"></i>
                <span>{{ selectedSlotDetails.user.phone_number || 'N/A' }}</span>
              </div>
              <div class="info-row vehicle">
                <i class="bi bi-car-front"></i>
                <span>{{ selectedSlotDetails.user.vehicle_number || 'N/A' }}</span>
              </div>
              </div>
              
              <!-- Show generic reserved message if no user details -->
              <div v-if="!selectedSlotDetails.user" class="popup-message">
              This slot is currently reserved
              </div>
              
              <div class="popup-rate">₹{{ selectedLot?.price || 0 }}/hour</div>
            </div>

            <!-- Fallback for unknown status -->
            <div v-else class="popup-message">
              Status information not available
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lot Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
      <div class="modal-container details-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>{{ selectedLot?.location_name }}</h3>
            <p>Detailed parking lot information and slot management</p>
          </div>
          <div class="modal-actions">
            <button class="modal-action-btn edit-btn" @click="editLot(selectedLot)" title="Edit Parking Lot">
              <i class="bi bi-pencil"></i>
            </button>
            <button 
              class="modal-action-btn delete-btn" 
              @click="deleteLot(selectedLot)"
              :disabled="!canDeleteLot(selectedLot)"
              :title="canDeleteLot(selectedLot) ? 'Delete this parking lot' : 'Cannot delete - parking lot has occupied spots'"
            >
              <i class="bi bi-trash"></i>
            </button>
            <button class="close-btn" @click="closeDetailsModal">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
        </div>

        <div class="modal-content" v-if="selectedLot">
          <div class="details-header">
            <div class="lot-info-detailed">
              <div class="info-item">
                <i class="bi bi-geo-alt"></i>
                <span>{{ selectedLot.address }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-pin-map"></i>
                <span>{{ selectedLot.pincode }}</span>
              </div>
              <div class="info-item">
                <i class="bi bi-currency-rupee"></i>
                <span>₹{{ selectedLot.price }} per hour</span>
              </div>
            </div>
            
            <div class="quick-stats">
              <div class="quick-stat">
                <div class="stat-value">{{ selectedLot.number_of_slots }}</div>
                <div class="stat-name">Total Spots</div>
              </div>
              <div class="quick-stat available">
                <div class="stat-value">{{ selectedLot.available_slots }}</div>
                <div class="stat-name">Available</div>
              </div>
              <div class="quick-stat occupied">
                <div class="stat-value">{{ selectedLot.number_of_slots - selectedLot.available_slots }}</div>
                <div class="stat-name">Occupied</div>
              </div>
              <div class="quick-stat">
                <div class="stat-value">{{ getOccupancyRate(selectedLot) }}%</div>
                <div class="stat-name">Occupancy</div>
              </div>
            </div>
          </div>
          
          <div class="slots-section">
            <h4>All Parking Spots</h4>
            <div class="slots-legend">
              <div class="legend-item">
                <div class="legend-dot available"></div>
                <span>Available</span>
              </div>
              <div class="legend-item">
                <div class="legend-dot occupied"></div>
                <span>Occupied</span>
              </div>
            </div>
            
            <div class="all-slots-grid">
              <div 
                v-for="spot in getDisplaySpots(selectedLot)" 
                :key="spot.id || spot.number" 
                class="slot-detailed"
                :class="spot.status === 'available' ? 'available' : 'occupied'"
                @click="viewSlotDetails(spot)"
              >
                <div class="slot-number">{{ String(spot.number).padStart(2, '0') }}</div>
                <div class="slot-icon">
                  <i :class="spot.status === 'available' ? 'bi bi-car-front' : 'bi bi-car-front-fill'"></i>
                </div>
                <div class="slot-status">
                  {{ spot.status === 'available' ? 'Available' : 'Occupied' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()

// Reactive data
const lots = ref([])
const loading = ref(true)
const showDetailsModal = ref(false)
const selectedLot = ref(null)
const currentUser = ref({ username: 'Admin' })
const error = ref(null)

// Mobile menu state
const isMobileMenuOpen = ref(false)

// Add/Edit Lot Modal
const showAddLotModal = ref(false)
const isEditMode = ref(false)
const lotFormLoading = ref(false)
const lotForm = ref({
  location_name: '',
  price: '',
  address: '',
  pincode: '',
  number_of_slots: ''
})

// Delete Modal
const showDeleteModal = ref(false)
const lotToDelete = ref(null)
const deleteLoading = ref(false)

// Methods
const loadLots = async () => {
  loading.value = true
  error.value = null
  try {
    console.log('Loading parking lots from API...')
    const response = await api.getParkingLots()
    console.log('API Response:', response)
    
    // The API returns { msg: '...', lots: [...] }
    if (response && response.lots) {
      lots.value = response.lots
      console.log('Loaded lots:', lots.value)
    } else {
      console.warn('No lots data in response:', response)
      lots.value = []
    }
  } catch (error) {
    console.error('Error loading parking lots:', error)
    error.value = error.message || 'Failed to load parking lots'
    lots.value = []
    
    // Show user-friendly error message
    if (error.response?.status === 401) {
      error.value = 'You need to be logged in to view parking lots'
    } else if (error.response?.status === 403) {
      error.value = 'You do not have permission to view parking lots'
    } else if (error.response?.status >= 500) {
      error.value = 'Server error. Please try again later.'
    }
  } finally {
    loading.value = false
  }
}

const refreshLots = () => {
  loadLots()
}

const getAvailabilityStatus = (lot) => {
  const rate = (lot.available_slots / lot.number_of_slots) * 100
  if (rate > 50) return 'high'
  if (rate > 20) return 'medium'
  return 'low'
}

const getAvailabilityText = (lot) => {
  const rate = (lot.available_slots / lot.number_of_slots) * 100
  if (rate > 50) return 'Good Availability'
  if (rate > 20) return 'Limited Spots'
  return 'Nearly Full'
}

const getOccupancyRate = (lot) => {
  return Math.round(((lot.number_of_slots - lot.available_slots) / lot.number_of_slots) * 100)
}

const getDisplaySpots = (lot) => {
  // If we have real spot data, use it
  if (lot.spots && lot.spots.length > 0) {
    return lot.spots.map((spot, index) => ({
      ...spot,
      number: index + 1 // Add display number
    }))
  }
  
  // Otherwise, create mock spots based on available/occupied counts
  const spots = []
  for (let i = 1; i <= lot.number_of_slots; i++) {
    spots.push({
      id: `mock-${lot.id}-${i}`,
      number: i,
      lot_id: lot.id,
      status: i <= lot.available_slots ? 'available' : 'occupied',
      user_id: i <= lot.available_slots ? null : 'occupied'
    })
  }
  return spots
}

const viewLotDetails = async (lot) => {
  selectedLot.value = lot
  showDetailsModal.value = true
  
  // Load spot details for this lot
  try {
    console.log('Loading spots for lot:', lot.id)
    const spotsResponse = await api.getAvailableSpots(lot.id)
    console.log('Available spots response:', spotsResponse)
    
    // Also get all spots to show occupied ones
    const allSpotsResponse = await api.getParkingSpots()
    console.log('All spots response:', allSpotsResponse)
    
    if (allSpotsResponse && allSpotsResponse.spots) {
      // Filter spots for this lot
      const lotSpots = allSpotsResponse.spots.filter(spot => spot.lot_id === lot.id)
      selectedLot.value.spots = lotSpots
      console.log('Lot spots:', lotSpots)
    }
  } catch (error) {
    console.error('Error loading spot details:', error)
    // Continue showing modal even if spots fail to load
  }
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedLot.value = null
}

const canDeleteLot = (lot) => {
  // Cannot delete if any slots are occupied
  return lot.available_slots === lot.number_of_slots
}

// Add/Edit Lot Methods
const openAddLotModal = () => {
  isEditMode.value = false
  resetLotForm()
  showAddLotModal.value = true
}

const editLot = (lot) => {
  isEditMode.value = true
  lotForm.value = {
    id: lot.id,
    location_name: lot.location_name,
    price: lot.price,
    address: lot.address,
    pincode: lot.pincode,
    number_of_slots: lot.number_of_slots
  }
  // Close details modal first
  closeDetailsModal()
  showAddLotModal.value = true
}

const closeAddLotModal = () => {
  showAddLotModal.value = false
  resetLotForm()
}

const resetLotForm = () => {
  lotForm.value = {
    location_name: '',
    price: '',
    address: '',
    pincode: '',
    number_of_slots: ''
  }
}

const submitLot = async () => {
  lotFormLoading.value = true
  try {
    let response
    if (isEditMode.value) {
      // Update existing lot
      response = await api.updateParkingLot(lotForm.value.id, {
        location_name: lotForm.value.location_name,
        price: parseFloat(lotForm.value.price),
        address: lotForm.value.address,
        pincode: lotForm.value.pincode
        // Don't update number_of_slots when editing
      })
      console.log('Lot updated:', response)
    } else {
      // Create new lot
      response = await api.createParkingLot({
        location_name: lotForm.value.location_name,
        price: parseFloat(lotForm.value.price),
        address: lotForm.value.address,
        pincode: lotForm.value.pincode,
        number_of_slots: parseInt(lotForm.value.number_of_slots)
      })
      console.log('Lot created:', response)
    }
    
    // Refresh the lots list
    await loadLots()
    closeAddLotModal()
    
    // Show success message
    alert(isEditMode.value ? 'Parking lot updated successfully!' : 'Parking lot created successfully!')
    
  } catch (error) {
    console.error('Error submitting lot:', error)
    alert('Error: ' + (error.message || 'Failed to save parking lot'))
  } finally {
    lotFormLoading.value = false
  }
}

// Delete Methods
const deleteLot = (lot) => {
  if (!canDeleteLot(lot)) {
    alert('Cannot delete this parking lot because it has occupied spots. Please wait for all spots to be available before deleting.')
    return
  }
  
  lotToDelete.value = lot
  // Close details modal first
  closeDetailsModal()
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  lotToDelete.value = null
}

const confirmDelete = async () => {
  if (!lotToDelete.value) return
  
  deleteLoading.value = true
  try {
    console.log('Deleting lot:', lotToDelete.value.id)
    const response = await api.deleteParkingLot(lotToDelete.value.id)
    console.log('Lot deleted:', response)
    
    // Refresh the lots list
    await loadLots()
    closeDeleteModal()
    
    // Show success message
    alert('Parking lot deleted successfully!')
    
  } catch (error) {
    console.error('Error deleting lot:', error)
    alert('Error: ' + (error.message || 'Failed to delete parking lot'))
  } finally {
    deleteLoading.value = false
  }
}

// Slot Details Modal
const showSlotDetailsModal = ref(false)
const selectedSlotDetails = ref(null)

const viewSlotDetails = async (spot) => {
  console.log(`Viewing details for spot ${spot.number} (ID: ${spot.id})`)
  
  // Always show modal for both available and occupied spots
  console.log(`Showing details for ${spot.status} spot`)
  
  if (spot.status === 'available') {
    // Show available slot information
    selectedSlotDetails.value = {
      ...spot,
      loading: false,
      error: null,
      user: null
    }
    showSlotDetailsModal.value = true
    return
  }
  
  // Show loading state while fetching details
  selectedSlotDetails.value = {
    ...spot,
    loading: true,
    error: null
  }
  showSlotDetailsModal.value = true
  
  try {
    if (spot.id && !spot.id.toString().startsWith('mock-')) {
      // Fetch real spot details from API using the correct endpoint
      console.log(`Fetching details for spot ${spot.id}`)
      const spotResponse = await api.getParkingSpot(spot.id)
      console.log('Spot details response:', spotResponse)
      
      // Also fetch user details if spot is occupied/reserved and has user_id
      if (spotResponse.spot && spotResponse.spot.user_id) {
        try {
          console.log(`Fetching user details for user_id: ${spotResponse.spot.user_id}`)
          const userResponse = await api.getUser(spotResponse.spot.user_id)
          console.log('User details response:', userResponse)
          
          selectedSlotDetails.value = {
            ...spot,
            ...spotResponse.spot,
            user: userResponse.user || null,
            loading: false,
            error: null
          }
        } catch (userError) {
          console.error('Error fetching user details:', userError)
          // Show spot details without user info if user fetch fails
          selectedSlotDetails.value = {
            ...spot,
            ...spotResponse.spot,
            user: null,
            loading: false,
            error: `Slot is ${spotResponse.spot.status} but user details unavailable (${userError.response?.status === 401 ? 'Access denied' : 'User not found'})`
          }
        }
      } else {
        selectedSlotDetails.value = {
          ...spot,
          ...spotResponse.spot,
          user: null,
          loading: false,
          error: null
        }
      }
    } else {
      // For mock data, just show the spot as-is
      selectedSlotDetails.value = {
        ...spot,
        loading: false,
        error: null,
        user: null
      }
    }
  } catch (error) {
    console.error('Error fetching slot details:', error)
    selectedSlotDetails.value = {
      ...spot,
      loading: false,
      error: `Failed to load slot details: ${error.response?.data?.msg || error.message || 'Please try again.'}`
    }
  }
}

const closeSlotDetailsModal = () => {
  showSlotDetailsModal.value = false
  selectedSlotDetails.value = null
}

const handleLogout = () => {
  // Handle logout logic
  router.push('/login')
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Helper functions for status display
const getStatusIcon = (status) => {
  switch (status) {
    case 'available':
      return 'bi bi-check-circle'
    case 'occupied':
      return 'bi bi-car-front-fill'
    case 'reserved':
      return 'bi bi-bookmark-fill'
    default:
      return 'bi bi-question-circle'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'available':
      return 'Available'
    case 'occupied':
      return 'Occupied'
    case 'reserved':
      return 'Reserved'
    default:
      return 'Unknown'
  }
}

// Helper functions for time display (placeholders - implement as needed)
const formatBookingTime = () => {
  return 'N/A'
}

const calculateDuration = () => {
  return 'N/A'
}

// Lifecycle
onMounted(() => {
  // Get current user info from localStorage
  const username = localStorage.getItem('username') || 'Admin'
  currentUser.value = { username }
  
  loadLots()
})
</script>

<style scoped>

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.parking-lots-container {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* Admin Navbar */
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
  min-height: 100vh;
  padding-top: 70px;
  margin: 0 auto;
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
  padding: 2.5rem;
  margin-bottom: 3rem;
  position: relative;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
  text-align: left;
}

.section-title-area {
  flex: 1;
}

.section-title {
  font-size: 2rem;
  font-weight: 500;
  margin: 0;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title i {
  color: #00a8e8;
}

.section-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0.5rem 0 0 0;
}

.cta-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  justify-content: center;;
}

.cta-button.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.4);
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  transform: translateY(-2px);
}

.section-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Loading, Error and Empty States */
.loading-state, .empty-state, .error-state {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error-state {
  border-color: rgba(244, 67, 54, 0.3);
  background: rgba(244, 67, 54, 0.05);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 168, 232, 0.3);
  border-top: 3px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.empty-state i, .error-state i {
  font-size: 4rem;
  color: #00a8e8;
  margin-bottom: 1rem;
}

.error-state i {
  color: #f44336;
}

.empty-state h3, .error-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

/* Lots Grid */
.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.lot-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 168, 232, 0.2);
  border-color: rgba(0, 168, 232, 0.3);
}

.lot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.lot-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #ffffff;
}

.lot-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.lot-status.high {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.lot-status.medium {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.lot-status.low {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.lot-info {
  margin-bottom: 1.5rem;
}

.lot-name {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.lot-address {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.lot-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.pincode, .price {
  padding: 0.3rem 0.75rem;
  background: rgba(0, 168, 232, 0.15);
  border: 1px solid rgba(0, 168, 232, 0.25);
  border-radius: 15px;
  color: #00a8e8;
  font-size: 0.85rem;
  font-weight: 600;
}

.lot-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #ffffff;
}

.stat-number.available {
  color: #4caf50;
}

.stat-number.occupied {
  color: #f44336;
}

.stat-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.lot-visual {
  margin-bottom: 1.5rem;
}

.slots-preview {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.slots-header {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.75rem;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 0.25rem;
  align-items: center;
}

.slot-mini {
  aspect-ratio: 1;
  background: rgba(244, 67, 54, 0.3);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.5);
}

.slot-mini.available {
  background: rgba(76, 175, 80, 0.3);
  color: #4caf50;
  border-color: rgba(76, 175, 80, 0.5);
}

.more-slots {
  grid-column: span 3;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
}

.lot-actions {
  display: flex;
  gap: 0.75rem;
}

.action-button.full-width {
  width: 100%;
}

.action-button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.action-button.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
}

.action-button.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.action-button:hover {
  transform: translateY(-1px);
}

.action-button.primary:hover {
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
}

.action-button.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
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
  width: 90%;
  max-width: 600px;
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

.details-modal {
  max-width: 1000px;
}

.modal-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgb(255, 255, 255);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.modal-action-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.modal-action-btn.edit-btn {
  background: rgba(0, 168, 232, 0.15);
  border: 1px solid rgba(0, 168, 232, 0.25);
  color: #00a8e8;
}

.modal-action-btn.edit-btn:hover {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 168, 232, 0.3);
}

.modal-action-btn.delete-btn {
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid rgba(255, 107, 107, 0.25);
  color: #ff6b6b;
}

.modal-action-btn.delete-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.modal-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.modal-action-btn:disabled:hover {
  background: rgba(255, 107, 107, 0.15) !important;
  color: #ff6b6b !important;
  box-shadow: none !important;
}

.modal-title-section h3 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.modal-title-section p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.close-btn {
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid rgba(255, 107, 107, 0.25);
  color: #ff6b6b;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #ff6b6b;
  color: #ffffff;
}

.modal-content {
  padding: 2rem;
}

.details-header {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.lot-info-detailed {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(255, 255, 255, 0.9);
}

.info-item i {
  color: #00a8e8;
  width: 20px;
}

.quick-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.quick-stat {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.quick-stat.available {
  border-color: rgba(76, 175, 80, 0.3);
  background: rgba(76, 175, 80, 0.1);
}

.quick-stat.occupied {
  border-color: rgba(244, 67, 54, 0.3);
  background: rgba(244, 67, 54, 0.1);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.quick-stat.available .stat-value {
  color: #4caf50;
}

.quick-stat.occupied .stat-value {
  color: #f44336;
}

.stat-name {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
}

.slots-section h4 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
}

.slots-legend {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.available {
  background: #4caf50;
}

.legend-dot.occupied {
  background: #f44336;
}

.all-slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.slot-detailed {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slot-detailed.available {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
}

.slot-detailed:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.slot-number {
  font-weight: 600;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.5rem;
}

.slot-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.slot-detailed.available .slot-icon {
  color: #4caf50;
}

.slot-detailed .slot-icon {
  color: #f44336;
}

.slot-status {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
}

/* Form Styles */
.modal-form {
  padding: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.form-label i {
  color: #00a8e8;
  width: 16px;
}

.form-input {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #00a8e8;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 3px rgba(0, 168, 232, 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-hint {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.btn.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
}

.btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn.danger {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #ffffff;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.btn.primary:hover {
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
}

.btn.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.btn.danger:hover {
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

/* Delete Modal Styles */
.delete-modal {
  max-width: 500px;
}

.delete-warning {
  text-align: center;
  padding: 1rem 0;
}

.warning-icon {
  font-size: 4rem;
  color: #f44336;
  margin-bottom: 1rem;
}

.delete-warning h4 {
  color: #ffffff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.delete-warning p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2rem;
}

.lot-details {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: left;
  margin: 1.5rem 0;
}

.detail-item {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-item strong {
  color: #ffffff;
}

/* Compact Slot Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  animation: popupFadeIn 0.2s ease-out;
  padding: 1rem;
  box-sizing: border-box;
}

@keyframes popupFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.slot-popup {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 168, 232, 0.3);
  border-radius: 12px;
  width: 320px;
  max-width: 90vw;
  max-height: 80vh;
  overflow-y: auto;
  animation: popupSlideIn 0.3s ease-out;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

@keyframes popupSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.popup-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
}

.popup-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  font-size: 1.1rem;
}

.popup-close:hover {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.popup-content {
  padding: 1rem;
}

.popup-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 168, 232, 0.3);
  border-top: 2px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.popup-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #f44336;
  font-size: 0.85rem;
}

.popup-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.popup-status.available {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.popup-status.occupied {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.popup-status.reserved {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.popup-available {
  text-align: center;
}

.popup-message {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.popup-rate {
  background: rgba(0, 168, 232, 0.15);
  border: 1px solid rgba(0, 168, 232, 0.3);
  color: #00a8e8;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
}

.popup-occupied {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.popup-reserved {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.9);
  padding: 0.3rem 0;
}

.info-row i {
  color: #00a8e8;
  width: 14px;
  text-align: center;
  font-size: 0.75rem;
}

.info-row.vehicle {
  background: rgba(0, 168, 232, 0.1);
  border: 1px solid rgba(0, 168, 232, 0.3);
  border-radius: 6px;
  padding: 0.5rem;
  font-family: 'Courier New', monospace;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.booking-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  padding: 0.25rem 0;
}

.booking-time i {
  color: #00a8e8;
  width: 14px;
  text-align: center;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
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
    margin: 1rem 0;
  }
  
  .lots-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .lot-card {
    padding: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .section-actions {
    flex-direction: column;
    width: 100%;
    gap: 0.75rem;
  }
  
  .cta-button {
    width: 100%;
    justify-content: center;
  }
  
  .details-header {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .all-slots-grid {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
    gap: 0.75rem;
  }
  
  .slot-item {
    padding: 1rem;
    min-height: 70px;
  }
  
  .slot-number {
    font-size: 0.9rem;
  }
  
  /* Modal Responsiveness */
  .modal-container {
    width: 95%;
    max-width: 500px;
    margin: 1rem;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-header {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .modal-title-section h3 {
    font-size: 1.4rem;
  }
  
  .modal-form {
    padding: 1.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 1rem;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
    padding: 1rem;
  }
  
  /* Details Modal */
  .details-container {
    padding: 1rem;
  }
  
  .details-sections {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .section-card {
    padding: 1.5rem;
  }
  
  /* Slot Details Popup */
  .slot-popup {
    width: 95%;
    max-width: 320px;
    margin: 1rem;
  }
  
  .popup-header h4 {
    font-size: 1rem;
  }
  
  .popup-content {
    padding: 1rem;
  }
  
  .info-row {
    font-size: 0.85rem;
    padding: 0.75rem;
  }
  
  .user-info {
    gap: 0.75rem;
  }
  
  .popup-available,
  .popup-occupied {
    padding: 1rem;
  }
  
  .popup-rate {
    font-size: 1.2rem;
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
    margin: 0.75rem 0;
  }
  
  .section-title {
    font-size: 1.3rem;
  }
  
  .section-subtitle {
    font-size: 0.9rem;
  }
  
  .lot-card {
    padding: 1.25rem;
  }
  
  .lot-name {
    font-size: 1.1rem;
  }
  
  .lot-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
  
  .stat-number {
    font-size: 1.2rem;
  }
  
  .stat-label {
    font-size: 0.75rem;
  }
  
  .slots-grid {
    grid-template-columns: repeat(auto-fill, minmax(25px, 1fr));
    gap: 3px;
  }
  
  .slot-mini {
    width: 25px;
    height: 25px;
    font-size: 0.7rem;
  }
  
  .quick-stats {
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }
  
  .all-slots-grid {
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
    gap: 0.5rem;
  }
  
  .slot-item {
    padding: 0.75rem;
    min-height: 60px;
  }
  
  .slot-number {
    font-size: 0.8rem;
  }
  
  /* Modal Mobile Optimization */
  .modal-container {
    width: 98%;
    margin: 0.5rem;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-title-section h3 {
    font-size: 1.2rem;
  }
  
  .modal-title-section p {
    font-size: 0.85rem;
  }
  
  .modal-form {
    padding: 1rem;
  }
  
  .form-label {
    font-size: 0.9rem;
  }
  
  .form-input,
  .form-textarea {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .btn {
    padding: 0.875rem;
    font-size: 0.9rem;
  }
  
  /* Slot Popup Mobile */
  .slot-popup {
    width: 98%;
    max-width: 300px;
    margin: 0.5rem;
  }
  
  .popup-header {
    padding: 1rem;
  }
  
  .popup-header h4 {
    font-size: 0.95rem;
  }
  
  .popup-content {
    padding: 0.75rem;
  }
  
  .info-row {
    font-size: 0.8rem;
    padding: 0.5rem;
  }
  
  .popup-status {
    padding: 0.75rem;
    font-size: 0.85rem;
  }
  
  .popup-rate {
    font-size: 1.1rem;
  }
  
  .booking-time {
    font-size: 0.8rem;
  }
  
  /* Touch-friendly improvements */
  .close-btn,
  .popup-close {
    padding: 0.75rem;
    min-width: 44px;
    min-height: 44px;
  }
  
  .action-button,
  .cta-button {
    min-height: 44px;
    padding: 0.875rem 1.5rem;
  }
  
  .slot-item {
    min-height: 44px;
    touch-action: manipulation;
  }
}
</style>
