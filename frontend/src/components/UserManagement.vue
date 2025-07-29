<template>
  <div class="user-management-container">
    <!-- Admin Navbar -->
    <nav class="admin-navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <div class="brand-logo">
            <img src="../assets/P.png" alt="ParkEase Logo" class="logo-img">
            <div class="brand-text">
              <h1>ParkEase</h1>
              <p>User Management</p>
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
            <router-link to="/parking-lots" class="nav-link">
              <i class="bi bi-geo-alt-fill"></i>
              <span>Parking Lots</span>
            </router-link>
            <router-link to="/manage-users" class="nav-link active">
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

    <!-- Animated Background -->
    <div class="bg-animation">
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">User Management</h1>
        </div>
      </div>

      <!-- Users Section -->
      <div class="section-container">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-people-fill"></i>
              Registered Users
            </h2>
            <p class="section-subtitle">View and manage all registered users in the system</p>
          </div>
          <div class="section-actions">
            <div class="search-container">
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search users..." 
                class="search-input"
              >
              <i class="bi bi-search search-icon"></i>
            </div>
            <button class="cta-button primary" @click="refreshUsers">
              <i class="bi bi-arrow-clockwise"></i>
              Refresh
            </button>
          </div>
        </div>

        <div class="users-container">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading users...</p>
          </div>
          
          <div v-else-if="error" class="error-state">
            <i class="bi bi-exclamation-triangle"></i>
            <h3>Error Loading Users</h3>
            <p>{{ error }}</p>
            <button class="cta-button primary" @click="refreshUsers">
              <i class="bi bi-arrow-clockwise"></i>
              Try Again
            </button>
          </div>
          
          <div v-else-if="filteredUsers.length === 0" class="empty-state">
            <i class="bi bi-person-x"></i>
            <h3>No users found</h3>
            <p>{{ searchQuery ? 'No users match your search' : 'No users have been registered yet' }}</p>
            <router-link to="/admin-dashboard" class="cta-button primary">
              <i class="bi bi-arrow-left"></i>
              Back to Dashboard
            </router-link>
          </div>
          
          <div v-else class="users-grid">
            <div 
              v-for="(user, index) in filteredUsers" 
              :key="user.id" 
              class="user-card"
            >
              <div class="user-card-header">
                <div class="user-avatar-large">
                  {{ user.username.charAt(0).toUpperCase() }}
                </div>
                <div class="user-number">
                  #{{ String(index + 1).padStart(2, '0') }}
                </div>
              </div>
              
              <div class="user-card-body">
                <h3 class="user-name">{{ user.username }}</h3>
                <p class="user-email">{{ user.email }}</p>
                
                <div class="user-details">
                  <div class="detail-item">
                    <i class="bi bi-shield-check"></i>
                    <span class="role-badge" :class="user.role">
                      {{ user.role }}
                    </span>
                  </div>
                  
                  <div class="detail-item">
                    <i class="bi bi-car-front"></i>
                    <span>{{ user.vehicle_number || 'No Vehicle' }}</span>
                  </div>
                  
                  <div v-if="user.phone_number" class="detail-item">
                    <i class="bi bi-telephone"></i>
                    <span>{{ user.phone_number }}</span>
                  </div>
                </div>
              </div>
              
              <div class="user-card-actions">
                <button 
                  class="action-btn view-btn" 
                  @click="viewUserDetails(user)" 
                  title="View Details"
                >
                  <i class="bi bi-eye"></i>
                  <span>View</span>
                </button>
                <button 
                  class="action-btn edit-btn" 
                  @click="editUser(user)" 
                  title="Edit User"
                >
                  <i class="bi bi-pencil"></i>
                  <span>Edit</span>
                </button>
                <button 
                  v-if="user.role !== 'admin'" 
                  class="action-btn delete-btn" 
                  @click="confirmDeleteUser(user)" 
                  title="Delete User"
                >
                  <i class="bi bi-trash"></i>
                  <span>Delete</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Popup -->
    <div v-if="showUserDetailsModal" class="popup-overlay" @click="closeUserDetailsModal">
      <div class="user-details-popup" @click.stop>
        <div class="popup-header">
          <h4>{{ selectedUser?.username }} Details</h4>
          <button class="popup-close" @click="closeUserDetailsModal">
            <i class="bi bi-x"></i>
          </button>
        </div>

        <div class="popup-content" v-if="selectedUser">
          <!-- Loading State -->
          <div v-if="userStatsLoading" class="popup-loading">
            <div class="mini-spinner"></div>
            <span>Loading user statistics...</span>
          </div>
          
          <!-- User Details -->
          <div v-else class="user-details-content">
            <!-- User Basic Info -->
            <div class="user-basic-info">
              <div class="user-avatar-large">
                {{ selectedUser.username.charAt(0).toUpperCase() }}
              </div>
              <div class="user-identity">
                <h5>{{ selectedUser.username }}</h5>
                <p>{{ selectedUser.email }}</p>
                <p>{{ selectedUser.phone_number || 'N/A' }}</p>
                <span class="role-badge" :class="selectedUser.role">
                  {{ selectedUser.role }}
                </span>
              </div>
            </div>

            <!-- User Statistics -->
            <div class="user-stats-grid">
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-calendar-check"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ userStats.totalReservations || 0 }}</span>
                  <span class="stat-label">Total Reservations</span>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-clock"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ formatDuration(userStats.totalHours || 0) }}</span>
                  <span class="stat-label">Total Parked Time</span>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-currency-rupee"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-value">₹{{ userStats.totalSpent || 0 }}</span>
                  <span class="stat-label">Total Money Spent</span>
                </div>
              </div>
              
              <div class="stat-card">
                <div class="stat-icon">
                  <i class="bi bi-car-front"></i>
                </div>
                <div class="stat-info">
                  <span class="stat-value">{{ selectedUser.vehicle_number || 'N/A' }}</span>
                  <span class="stat-label">Vehicle Number</span>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="recent-activity">
              <h6>
                <i class="bi bi-activity"></i>
                Recent Activity
              </h6>
              <div class="activity-list">
                <div v-if="userStats.recentReservations && userStats.recentReservations.length > 0">
                  <div v-for="reservation in userStats.recentReservations.slice(0, 3)" :key="reservation.id" class="activity-item">
                    <div class="activity-icon">
                      <i class="bi bi-geo-alt"></i>
                    </div>
                    <div class="activity-content">
                      <span class="activity-title">{{ reservation.lot_name || reservation.location_name || 'Unknown Location' }}</span>
                      <span class="activity-time">{{ formatDate(reservation.parking_time || reservation.created_at) }}</span>
                    </div>
                    <div class="activity-amount">
                      ₹{{ reservation.parking_cost || reservation.amount || 0 }}
                    </div>
                  </div>
                </div>
                <div v-else class="no-activity">
                  <i class="bi bi-clock-history"></i>
                  <span>No recent activity</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditUserModal" class="popup-overlay" @click="closeEditUserModal">
      <div class="edit-user-popup" @click.stop>
        <div class="popup-header">
          <h4>Edit User - {{ editFormData?.username }}</h4>
          <button class="popup-close" @click="closeEditUserModal">
            <i class="bi bi-x"></i>
          </button>
        </div>

        <div class="popup-content">
          <form @submit.prevent="updateUser" class="edit-form">
            <!-- Loading State -->
            <div v-if="editLoading" class="popup-loading">
              <div class="mini-spinner"></div>
              <span>Updating user...</span>
            </div>
            
            <!-- Edit Form -->
            <div v-else class="form-content">
              <!-- Username Field -->
              <div class="form-group">
                <label for="edit-username">Username</label>
                <input 
                  id="edit-username"
                  v-model="editFormData.username" 
                  type="text" 
                  class="form-input" 
                  placeholder="Enter username"
                  required
                  :disabled="editLoading"
                >
              </div>

              <!-- Email Field -->
              <div class="form-group">
                <label for="edit-email">Email</label>
                <input 
                  id="edit-email"
                  v-model="editFormData.email" 
                  type="email" 
                  class="form-input" 
                  placeholder="Enter email address"
                  required
                  :disabled="editLoading"
                >
              </div>

              <!-- Password Field -->
              <div class="form-group">
                <label for="edit-password">New Password (optional)</label>
                <div class="password-input-group">
                  <input 
                    id="edit-password"
                    v-model="editFormData.password" 
                    :type="showPassword ? 'text' : 'password'"
                    class="form-input" 
                    placeholder="Enter new password (leave blank to keep current)"
                    :disabled="editLoading"
                  >
                  <button 
                    type="button" 
                    class="password-toggle" 
                    @click="showPassword = !showPassword"
                    :disabled="editLoading"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>

              <!-- Vehicle Number Field (for non-admin users) -->
              <div v-if="editFormData.role !== 'admin'" class="form-group">
                <label for="edit-vehicle">Vehicle Number</label>
                <input 
                  id="edit-vehicle"
                  v-model="editFormData.vehicle_number" 
                  type="text" 
                  class="form-input" 
                  placeholder="Enter vehicle number"
                  :disabled="editLoading"
                >
              </div>

              <!-- Form Actions -->
              <div class="form-actions">
                <button 
                  type="button" 
                  class="form-btn secondary" 
                  @click="closeEditUserModal"
                  :disabled="editLoading"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="form-btn primary" 
                  :disabled="editLoading || !editFormData.username || !editFormData.email"
                >
                  <i v-if="editLoading" class="bi bi-arrow-clockwise spinning"></i>
                  <i v-else class="bi bi-check-lg"></i>
                  {{ editLoading ? 'Updating...' : 'Update User' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Mobile menu state
const isMobileMenuOpen = ref(false)

// Reactive state
const loading = ref(false)
const error = ref(null)
const users = ref([])
const searchQuery = ref('')
const currentUser = ref({ username: 'Admin' })

// User Details Modal
const showUserDetailsModal = ref(false)
const selectedUser = ref(null)
const userStatsLoading = ref(false)
const userStats = ref({
  totalReservations: 0,
  totalHours: 0,
  totalSpent: 0,
  recentReservations: []
})

// Edit User Modal
const showEditUserModal = ref(false)
const editFormData = ref({
  id: null,
  username: '',
  email: '',
  password: '',
  role: 'user',
  vehicle_number: ''
})
const editLoading = ref(false)
const showPassword = ref(false)

// Computed
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.role.toLowerCase().includes(query) ||
    (user.vehicle_number && user.vehicle_number.toLowerCase().includes(query))
  )
})

// Methods
const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    console.log('Loading users from API...')
    const response = await api.getAllUsers()
    console.log('API Response:', response)
    
    if (response && response.users) {
      users.value = response.users
      console.log('Loaded users:', users.value)
    } else {
      console.warn('No users data in response:', response)
      users.value = []
    }
  } catch (error) {
    console.error('Error fetching users:', error)
    error.value = error.message || 'Failed to load users'
    users.value = []
  } finally {
    loading.value = false
  }
}

const refreshUsers = () => {
  fetchUsers()
}

const viewUserDetails = async (user) => {
  selectedUser.value = user
  showUserDetailsModal.value = true
  userStatsLoading.value = true
  
  try {
    console.log('Loading user statistics for:', user.id)
    
    // Fetch user reservations
    const reservationsResponse = await api.getUserReservations(user.id)
    console.log('User reservations:', reservationsResponse)
    
    if (reservationsResponse && reservationsResponse.reservations) {
      const reservations = reservationsResponse.reservations
      
      // Calculate statistics
      const totalReservations = reservations.length
      
      // Calculate total hours by checking if we have parking_time and leaving_time
      let totalHours = 0
      let totalSpent = 0
      
      reservations.forEach(res => {
        // Calculate duration if we have both parking and leaving times
        if (res.parking_time && res.leaving_time) {
          const parkingTime = new Date(res.parking_time)
          const leavingTime = new Date(res.leaving_time)
          const durationMs = leavingTime - parkingTime
          const hours = durationMs / (1000 * 60 * 60) // Convert milliseconds to hours
          totalHours += hours
        } else if (res.duration_hours) {
          totalHours += res.duration_hours
        }
        
        // Add to total spent - check multiple possible field names
        if (res.parking_cost) {
          totalSpent += res.parking_cost
        } else if (res.total_amount) {
          totalSpent += res.total_amount
        } else if (res.amount) {
          totalSpent += res.amount
        }
      })
      
      userStats.value = {
        totalReservations,
        totalHours: Math.round(totalHours * 100) / 100, // Round to 2 decimal places
        totalSpent: Math.round(totalSpent * 100) / 100, // Round to 2 decimal places
        recentReservations: reservations.slice(0, 5) // Last 5 reservations
      }
    } else {
      // Mock data for demonstration
      const mockReservations = [
        {
          id: 1,
          lot_name: 'City Mall Parking',
          parking_time: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
          leaving_time: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000 + 2 * 60 * 60 * 1000).toISOString(), // 2 hours later
          parking_cost: 150
        },
        {
          id: 2,
          lot_name: 'Office Complex',
          parking_time: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 1 week ago
          leaving_time: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000 + 8 * 60 * 60 * 1000).toISOString(), // 8 hours later
          parking_cost: 400
        },
        {
          id: 3,
          lot_name: 'Airport Terminal',
          parking_time: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString(), // 2 weeks ago
          leaving_time: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000 + 45 * 60 * 1000).toISOString(), // 45 minutes later
          parking_cost: 50
        }
      ]
      
      // Calculate totals from mock data
      let totalHours = 0
      let totalSpent = 0
      
      mockReservations.forEach(res => {
        const parkingTime = new Date(res.parking_time)
        const leavingTime = new Date(res.leaving_time)
        const durationMs = leavingTime - parkingTime
        const hours = durationMs / (1000 * 60 * 60)
        totalHours += hours
        totalSpent += res.parking_cost
      })
      
      userStats.value = {
        totalReservations: mockReservations.length,
        totalHours: Math.round(totalHours * 100) / 100,
        totalSpent: Math.round(totalSpent * 100) / 100,
        recentReservations: mockReservations
      }
    }
  } catch (error) {
    console.error('Error fetching user statistics:', error)
    // Use mock data on error for demonstration
    const mockReservations = [
      {
        id: 1,
        lot_name: 'Demo Parking Lot',
        parking_time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
        leaving_time: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 minutes ago
        parking_cost: 75
      }
    ]
    
    userStats.value = {
      totalReservations: mockReservations.length,
      totalHours: 1.5, // 1 hour 30 minutes
      totalSpent: 75,
      recentReservations: mockReservations
    }
  } finally {
    userStatsLoading.value = false
  }
}

const closeUserDetailsModal = () => {
  showUserDetailsModal.value = false
  selectedUser.value = null
  userStats.value = {
    totalReservations: 0,
    totalHours: 0,
    totalSpent: 0,
    recentReservations: []
  }
}

const editUser = (user) => {
  console.log('Edit user:', user.username)
  // Populate form with user data
  editFormData.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    password: '', // Always empty for security
    role: user.role,
    vehicle_number: user.vehicle_number || ''
  }
  showEditUserModal.value = true
}

const closeEditUserModal = () => {
  showEditUserModal.value = false
  showPassword.value = false
  editFormData.value = {
    id: null,
    username: '',
    email: '',
    password: '',
    role: 'user',
    vehicle_number: ''
  }
}

const updateUser = async () => {
  editLoading.value = true
  try {
    console.log('Updating user:', editFormData.value.id)
    
    // Prepare update data
    const updateData = {
      username: editFormData.value.username,
      email: editFormData.value.email,
      role: editFormData.value.role
    }
    
    // Only include password if it's provided
    if (editFormData.value.password && editFormData.value.password.trim() !== '') {
      updateData.password = editFormData.value.password
    }
    
    // Only include vehicle_number for non-admin users
    if (editFormData.value.role !== 'admin') {
      updateData.vehicle_number = editFormData.value.vehicle_number
    }
    
    console.log('Update data:', updateData)
    
    const response = await api.updateUser(editFormData.value.id, updateData)
    console.log('Update response:', response)
    
    alert('User updated successfully!')
    closeEditUserModal()
    await fetchUsers() // Refresh the users list
    
  } catch (error) {
    console.error('Error updating user:', error)
    alert('Failed to update user: ' + (error.message || 'Unknown error'))
  } finally {
    editLoading.value = false
  }
}

const confirmDeleteUser = (user) => {
  if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
    deleteUser(user)
  }
}

const deleteUser = async (user) => {
  try {
    console.log('Deleting user:', user.id)
    await api.deleteUser(user.id)
    alert('User deleted successfully!')
    await fetchUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    alert('Failed to delete user: ' + (error.message || 'Unknown error'))
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDuration = (totalHours) => {
  if (!totalHours || totalHours === 0) return '0 min'
  
  const hours = Math.floor(totalHours)
  const minutes = Math.round((totalHours - hours) * 60)
  
  if (hours === 0) {
    return `${minutes} min`
  } else if (minutes === 0) {
    return `${hours}h`
  } else {
    return `${hours}h ${minutes}m`
  }
}

const handleLogout = () => {
  router.push('/login')
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Lifecycle
onMounted(() => {
  // Get current user info from localStorage
  const username = localStorage.getItem('username') || 'Admin'
  const role = localStorage.getItem('role') || 'admin' // Assume admin if not specified
  currentUser.value = { username, role }
  
  fetchUsers()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.user-management-container {
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

.main-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #00a8e8, #ffffff);
  margin: 1rem auto;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
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

.section-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-container {
  position: relative;
  max-width: 300px;
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 12px 20px 12px 45px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.search-input:focus {
  outline: none;
  border-color: #00a8e8;
  box-shadow: 0 0 20px rgba(0, 168, 232, 0.3);
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.6);
}

.cta-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
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
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
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

/* Table */
.table-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.8);
}

.user-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 35px;
  height: 35px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #ffffff;
  font-size: 0.9rem;
}

.username {
  font-weight: 600;
  color: #ffffff;
}

.role-badge {
  padding: 0.4rem 0.9rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border: 1px solid;
  backdrop-filter: blur(10px);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.role-badge.admin {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
  border-color: rgba(255, 107, 107, 0.4);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
}

.role-badge.user {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn.view-btn {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.action-btn.view-btn:hover {
  background: rgba(33, 150, 243, 0.3);
  transform: scale(1.1);
}

.action-btn.edit-btn {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.action-btn.edit-btn:hover {
  background: rgba(255, 193, 7, 0.3);
  transform: scale(1.1);
}

.action-btn.delete-btn {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.action-btn.delete-btn:hover {
  background: rgba(244, 67, 54, 0.3);
  transform: scale(1.1);
}

/* User Details Popup */
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
}

@keyframes popupFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.user-details-popup {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 168, 232, 0.3);
  border-radius: 12px;
  width: 450px;
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
  font-size: 1.1rem;
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
  padding: 2rem;
  text-align: center;
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 168, 232, 0.3);
  border-top: 2px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.user-details-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.user-basic-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar-large {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #ffffff;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.user-identity h5 {
  margin: 0 0 0.25rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffffff;
}

.user-identity p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.user-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(0, 168, 232, 0.3);
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: rgba(0, 168, 232, 0.15);
  border: 1px solid rgba(0, 168, 232, 0.25);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00a8e8;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.recent-activity {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.recent-activity h6 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #ffffff;
}

.recent-activity h6 i {
  color: #00a8e8;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.activity-icon {
  width: 30px;
  height: 30px;
  background: rgba(0, 168, 232, 0.15);
  border: 1px solid rgba(0, 168, 232, 0.25);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00a8e8;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.activity-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.activity-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffffff;
}

.activity-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.activity-amount {
  font-size: 0.9rem;
  font-weight: 600;
  color: #00a8e8;
}

.no-activity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  padding: 1rem;
  text-align: center;
  justify-content: center;
}

/* Edit User Modal */
.edit-user-popup {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 168, 232, 0.3);
  border-radius: 12px;
  width: 500px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  animation: popupSlideIn 0.3s ease-out;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.edit-form {
  width: 100%;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
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

.password-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-group .form-input {
  flex: 1;
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.password-toggle:hover {
  color: #00a8e8;
  background: rgba(0, 168, 232, 0.1);
}

.password-toggle:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.form-btn {
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
  min-width: 120px;
  justify-content: center;
}

.form-btn.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
}

.form-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 168, 232, 0.4);
}

.form-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.form-btn.secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}

.form-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.spinning {
  animation: spin 1s linear infinite;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 1rem;
    height: 70px;
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
  
  .main-title {
    font-size: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .section-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .search-container {
    max-width: none;
  }
  
  .table-container {
    padding: 1rem;
  }
  
  .users-table th,
  .users-table td {
    padding: 0.7rem 0.5rem;
    font-size: 0.85rem;
  }
  
  .user-info {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .action-buttons {
    justify-content: center;
  }
  
  .user-details-popup {
    width: 95%;
    max-width: none;
  }
  
  .user-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .user-basic-info {
    flex-direction: column;
    text-align: center;
  }
  
  .edit-user-popup {
    width: 95%;
    max-width: none;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .form-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .brand-text h1 {
    font-size: 1.4rem;
  }
  
  .brand-text p {
    display: none;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .hero-section {
    padding: 1.5rem 0;
  }
}

/* Users Grid/Tiles Layout */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  padding: 1rem 0;
}

.user-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  position: relative;
  overflow: hidden;
}

.user-card::before {
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

.user-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 168, 232, 0.2);
  border-color: rgba(0, 168, 232, 0.4);
  background: rgba(255, 255, 255, 0.08);
}

.user-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.user-avatar-large {
  width: 55px;
  height: 55px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  font-weight: 700;
  text-transform: uppercase;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.user-number {
  background: rgba(0, 168, 232, 0.15);
  color: #00a8e8;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1px solid rgba(0, 168, 232, 0.3);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.user-card-body {
  flex: 1;
}

.user-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.user-email {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
  font-weight: 400;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-item i {
  color: #00a8e8;
  width: 18px;
  flex-shrink: 0;
  font-size: 1rem;
}

.user-card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-card-actions .action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 1px solid;
  backdrop-filter: blur(10px);
}

.user-card-actions .action-btn span {
  display: inline;
}

.user-card-actions .action-btn.view-btn {
  background: rgba(33, 150, 243, 0.15);
  color: #2196f3;
  border-color: rgba(33, 150, 243, 0.3);
}

.user-card-actions .action-btn.view-btn:hover {
  background: rgba(33, 150, 243, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(33, 150, 243, 0.3);
}

.user-card-actions .action-btn.edit-btn {
  background: rgba(255, 193, 7, 0.15);
  color: #ffc107;
  border-color: rgba(255, 193, 7, 0.3);
}

.user-card-actions .action-btn.edit-btn:hover {
  background: rgba(255, 193, 7, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 193, 7, 0.3);
}

.user-card-actions .action-btn.delete-btn {
  background: rgba(244, 67, 54, 0.15);
  color: #f44336;
  border-color: rgba(244, 67, 54, 0.3);
}

.user-card-actions .action-btn.delete-btn:hover {
  background: rgba(244, 67, 54, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(244, 67, 54, 0.3);
}

/* Mobile Menu Styles */
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

.mobile-nav-section:last-child {
  border-bottom: none;
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
  width: 20px;
  text-align: center;
  font-size: 1.2rem;
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

.mobile-user-avatar {
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.mobile-user-info {
  display: flex;
  flex-direction: column;
}

.mobile-user-name {
  font-weight: 600;
  color: #ffffff;
  font-size: 1.1rem;
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
  
  .search-container {
    width: 100%;
    max-width: none;
  }
  
  .cta-button {
    width: 100%;
    justify-content: center;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .user-card {
    padding: 1.5rem;
  }
  
  .user-card-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .user-card-actions .action-btn {
    width: 100%;
  }
  
  .user-details-popup {
    width: 95%;
    max-width: none;
  }
  
  .user-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .user-basic-info {
    flex-direction: column;
    text-align: center;
  }
  
  .edit-user-popup {
    width: 95%;
    max-width: none;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .form-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 0.75rem;
    padding-top: 80px;
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
  
  .users-grid {
    gap: 1rem;
  }
  
  .user-card {
    padding: 1.25rem;
  }
  
  .user-name {
    font-size: 1.1rem;
  }
  
  .user-card-actions {
    flex-direction: row;
    gap: 0.5rem;
  }
  
  .user-card-actions .action-btn {
    flex: 1;
    min-width: 44px;
    padding: 0.75rem 0.5rem;
  }
  
  .user-card-actions .action-btn span {
    display: none;
  }
  
  .user-card-actions .action-btn i {
    font-size: 1.1rem;
  }
}
</style>
