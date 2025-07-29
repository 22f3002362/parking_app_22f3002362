<template>
  <div class="admin-dashboard-container">
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
            <router-link to="/admin-dashboard" class="nav-link active">
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
            <router-link to="/admin-reports" class="nav-link">
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

    <!-- My Custom Wallpaper is under this div -->
    <div class="bg-animation">
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">Admin Dashboard</h1>
        </div>
      </div>

      <!-- Dashboard Stats -->
      <div class="stats-section">
        <div class="section-header">
          <h2 class="section-title">Performance Overview</h2>
          <p class="section-subtitle">Real-time metrics and key performance indicators</p>
        </div>
        <div class="stats-grid">
          <div v-for="(stat, idx) in summaryCards" :key="stat.title" class="stat-card" :style="{ animationDelay: `${idx * 0.1}s` }">
            <div class="stat-content">
              <div class="stat-icon">
                <i :class="stat.icon"></i>
              </div>
              <div class="stat-details">
                <div class="stat-number">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.title }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Parking Lots Section -->
      <div class="section-container" id="lots">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-geo-alt-fill"></i>
              Parking Lots Management
            </h2>
            <p class="section-subtitle">Control and monitor all your parking facilities with advanced management tools</p>
          </div>
          <button class="cta-button primary" @click="openAddLotModal">
            <i class="bi bi-plus-circle-fill"></i>
            Add New Lot
          </button>
        </div>

        <div class="table-container">
          <div v-if="loading.lots" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading parking lots...</p>
          </div>
          <div v-else-if="lots.length === 0" class="empty-state">
            <i class="bi bi-geo-alt"></i>
            <h3>No parking lots found</h3>
            <p>Start by adding your first parking lot</p>
          </div>
          <div v-else class="data-table">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Location</th>
                  <th>Address</th>
                  <th>Pincode</th>
                  <th>Price/hr</th>
                  <th>Total Spots</th>
                  <th>Available</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(lot, idx) in lots" :key="lot.id">
                  <td>{{ String(idx + 1).padStart(2, '0') }}</td>
                  <td class="location-cell">
                    <div class="location-info">
                      <span class="location-name">{{ lot.location_name }}</span>
                    </div>
                  </td>
                  <td>{{ lot.address }}</td>
                  <td>
                    <span class="badge pincode-badge">{{ lot.pincode }}</span>
                  </td>
                  <td>
                    <span class="badge price-badge">₹{{ lot.price }}</span>
                  </td>
                  <td>
                    <span class="badge count-badge">{{ lot.number_of_slots }}</span>
                  </td>
                  <td>
                    <span class="badge available-badge" :class="{ 'low': lot.available_slots < 5 }">
                      {{ lot.available_slots }}
                    </span>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button class="action-btn edit" @click="openEditLotModal(lot)" title="Edit">
                        <i class="bi bi-pencil-square"></i>
                      </button>
                      <button class="action-btn delete" @click="deleteLot(lot.id)" title="Delete">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Users Section -->
      <div class="section-container" id="users">
        <div class="section-header">
          <div class="section-title-area">
            <h2 class="section-title">
              <i class="bi bi-people-fill"></i>
              User Management
            </h2>
            <p class="section-subtitle">Monitor and manage your registered users with comprehensive user analytics</p>
          </div>
          <button class="cta-button primary" @click="openAddUserModal">
            <i class="bi bi-person-plus"></i>
            Add User
          </button>
        </div>

        <div class="table-container">
          <div v-if="loading.users" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading users...</p>
          </div>
          <div v-else-if="users.length === 0" class="empty-state">
            <i class="bi bi-people"></i>
            <h3>No users found</h3>
            <p>No users have registered yet</p>
          </div>
          <div v-else class="data-table">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>User</th>
                  <th>Email</th>
                  <th>Vehicle</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, idx) in users" :key="user.id">
                  <td>{{ String(idx + 1).padStart(2, '0') }}</td>
                  <td class="user-cell">
                    <div class="user-info">
                      <div class="user-avatar">
                        <i class="bi bi-person-circle"></i>
                      </div>
                      <span class="username">{{ user.username }}</span>
                    </div>
                  </td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span v-if="user.vehicle_number" class="badge vehicle-badge">
                      {{ user.vehicle_number }}
                    </span>
                    <span v-else class="no-vehicle">—</span>
                  </td>
                  <td>
                    <span class="badge role-badge" :class="user.role">
                      <i :class="user.role === 'admin' ? 'bi bi-shield-check' : 'bi bi-person'"></i>
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <div class="action-buttons" v-if="user.role !== 'admin'">
                      <button class="action-btn edit" @click="editUser(user)" title="Edit">
                        <i class="bi bi-pencil-square"></i>
                      </button>
                      <button class="action-btn delete" @click="deleteUser(user.id)" title="Delete">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Adding/Editing Lots -->
    <div v-if="showLotModal" class="modal-overlay" @click="closeLotModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>{{ isEditMode ? 'Edit Parking Lot' : 'Add New Parking Lot' }}</h3>
            <p>{{ isEditMode ? 'Update parking lot details' : 'Create a new parking facility' }}</p>
          </div>
          <button class="close-btn" @click="closeLotModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <form @submit.prevent="submitLot" class="modal-form">
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
                <i class="bi bi-mailbox"></i>
                Pincode
              </label>
              <input
                v-model="lotForm.pincode"
                type="text"
                class="form-input"
                placeholder="000000"
                maxlength="6"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-currency-rupee"></i>
                Price per Hour
              </label>
              <input
                v-model.number="lotForm.price"
                type="number"
                step="0.01"
                min="0"
                class="form-input"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div class="form-group" v-if="!isEditMode">
            <label class="form-label">
              <i class="bi bi-grid-3x3-gap"></i>
              Number of Parking Spots
            </label>
            <input
              v-model.number="lotForm.number_of_slots"
              type="number"
              min="1"
              class="form-input"
              placeholder="Total parking spots"
              required
            />
            <small class="form-hint">This cannot be changed after creation</small>
          </div>

          <div class="modal-footer">
            <button type="button" class="cta-button secondary" @click="closeLotModal">
              Cancel
            </button>
            <button type="submit" class="cta-button primary" :disabled="submitting">
              <span v-if="submitting" class="loading-spinner"></span>
              {{ isEditMode ? 'Update Lot' : 'Create Lot' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal for Adding/Editing Users -->
    <div v-if="showUserModal" class="modal-overlay" @click="closeUserModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <div class="modal-title-section">
            <h3>{{ isUserEditMode ? 'Edit User' : 'Add New User' }}</h3>
            <p>{{ isUserEditMode ? 'Update user details' : 'Create a new user account' }}</p>
          </div>
          <button class="close-btn" @click="closeUserModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <form @submit.prevent="submitUser" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-person"></i>
                Username
              </label>
              <input
                v-model="userForm.username"
                type="text"
                class="form-input"
                placeholder="Enter username"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-envelope"></i>
                Email
              </label>
              <input
                v-model="userForm.email"
                type="email"
                class="form-input"
                placeholder="Enter email address"
                required
              />
            </div>
          </div>

          <div class="form-row" v-if="!isUserEditMode">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-lock"></i>
                Password
              </label>
              <input
                v-model="userForm.password"
                type="password"
                class="form-input"
                placeholder="Enter password"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-telephone"></i>
                Phone Number
              </label>
              <input
                v-model="userForm.phone_number"
                type="tel"
                class="form-input"
                placeholder="Enter phone number"
              />
            </div>
          </div>

          <div class="form-row" v-if="isUserEditMode">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-telephone"></i>
                Phone Number
              </label>
              <input
                v-model="userForm.phone_number"
                type="tel"
                class="form-input"
                placeholder="Enter phone number"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-car-front"></i>
                Vehicle Number
              </label>
              <input
                v-model="userForm.vehicle_number"
                type="text"
                class="form-input"
                placeholder="Enter vehicle number"
              />
            </div>
          </div>

          <div class="form-row" v-if="!isUserEditMode">
            <div class="form-group">
              <label class="form-label">
                <i class="bi bi-car-front"></i>
                Vehicle Number
              </label>
              <input
                v-model="userForm.vehicle_number"
                type="text"
                class="form-input"
                placeholder="Enter vehicle number"
              />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="cta-button secondary" @click="closeUserModal">
              Cancel
            </button>
            <button type="submit" class="cta-button primary" :disabled="submitting">
              <span v-if="submitting" class="loading-spinner"></span>
              {{ isUserEditMode ? 'Update User' : 'Create User' }}
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

const router = useRouter();
const toast = useToast();

// Reactive data
const lots = ref([]);
const users = ref([]);
const loading = reactive({ lots: true, users: true });
const submitting = ref(false);
const currentUser = ref(null);
const isMobileMenuOpen = ref(false);

// Modal state
const showLotModal = ref(false);
const showUserModal = ref(false);
const showLogoutModal = ref(false);
const isEditMode = ref(false);
const isUserEditMode = ref(false);
const lotForm = ref({
  id: null,
  location_name: "",
  address: "",
  pincode: "",
  price: 0,
  number_of_slots: 1
});

const userForm = ref({
  id: null,
  username: "",
  email: "",
  password: "",
  phone: "",
  vehicle_number: "",
  role: "user"
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
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const accessToken = localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  
  console.log('Auth check:', {
    isLoggedIn,
    hasToken: !!accessToken,
    userRole: user?.role
  });

  if (!isLoggedIn || isLoggedIn !== 'true' || !accessToken) {
    toast.error('Please log in to access the admin dashboard');
    router.push('/login');
    return false;
  }

  if (user?.role !== 'admin') {
    toast.error('Access denied. Admin privileges required.');
    router.push('/user-dashboard');
    return false;
  }

  return true;
};

// Fetch data with proper error handling
const fetchData = async () => {
  if (!checkAuth()) return;

  // Fetch parking lots
  try {
    loading.lots = true;
    console.log('Fetching parking lots...');
    const lotsResponse = await api.getParkingLots();
    console.log('Parking lots response:', lotsResponse);
    lots.value = lotsResponse.lots || [];
    toast.success('Parking lots loaded successfully');
  } catch (error) {
    console.error("Error fetching parking lots:", error);
    handleApiError(error, 'Failed to load parking lots');
  } finally {
    loading.lots = false;
  }

  // Fetch users
  try {
    loading.users = true;
    console.log('Fetching users...');
    const usersResponse = await api.getAllUsers();
    console.log('Users response:', usersResponse);
    users.value = usersResponse.users || [];
    toast.success('Users loaded successfully');
  } catch (error) {
    console.error("Error fetching users:", error);
    handleApiError(error, 'Failed to load users');
  } finally {
    loading.users = false;
  }
};

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

// Summary cards computed property
const summaryCards = computed(() => [
  {
    icon: "bi bi-geo-alt-fill",
    value: lots.value.length,
    title: "Parking Lots"
  },
  {
    icon: "bi bi-grid-3x3-gap-fill",
    value: lots.value.reduce((sum, lot) => sum + (lot.number_of_slots || 0), 0),
    title: "Total Spots"
  },
  {
    icon: "bi bi-check-circle-fill",
    value: lots.value.reduce((sum, lot) => sum + (lot.available_slots || 0), 0),
    title: "Available Spots"
  },
  {
    icon: "bi bi-people-fill",
    value: users.value.length - 1,  // THis -1 will exclude the admin
    title: "Registered Users"
  }
]);

// Modal controls
const openAddLotModal = () => {
  isEditMode.value = false;
  lotForm.value = {
    id: null,
    location_name: "",
    address: "",
    pincode: "",
    price: 0,
    number_of_slots: 10
  };
  showLotModal.value = true;
};

const openEditLotModal = (lot) => {
  isEditMode.value = true;
  lotForm.value = { ...lot };
  showLotModal.value = true;
};

const closeLotModal = () => {
  showLotModal.value = false;
  isEditMode.value = false;
};

// CRUD Operations for Parking Lots
const submitLot = async () => {
  if (!checkAuth()) return;
  
  submitting.value = true;
  
  try {
    if (isEditMode.value) {
      console.log('Updating lot:', lotForm.value);
      await api.updateParkingLot(lotForm.value.id, lotForm.value);
      toast.success('Parking lot updated successfully!');
    } else {
      console.log('Creating lot:', lotForm.value);
      await api.createParkingLot(lotForm.value);
      toast.success('Parking lot created successfully!');
    }
    
    await fetchData(); // Refresh data
    closeLotModal();
  } catch (error) {
    console.error("Error submitting lot:", error);
    handleApiError(error, `Failed to ${isEditMode.value ? 'update' : 'create'} parking lot`);
  } finally {
    submitting.value = false;
  }
};

const deleteLot = async (id) => {
  if (!checkAuth()) return;
  
  if (!confirm("Are you sure you want to delete this parking lot? This action cannot be undone.")) {
    return;
  }
  
  try {
    await api.deleteParkingLot(id);
    toast.success('Parking lot deleted successfully!');
    await fetchData(); // Refresh data
  } catch (error) {
    console.error("Error deleting lot:", error);
    handleApiError(error, 'Failed to delete parking lot');
  }
};

// User Management Functions
const openAddUserModal = () => {
  isUserEditMode.value = false;
  userForm.value = {
    id: null,
    username: "",
    email: "",
    password: "",
    phone_number: "",
    vehicle_number: "",
    role: "user"
  };
  showUserModal.value = true;
};

const editUser = (user) => {
  isUserEditMode.value = true;
  userForm.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    password: "", // Don't populate password for editing
    phone_number: user.phone_number || "",
    vehicle_number: user.vehicle_number || "",
    role: user.role
  };
  showUserModal.value = true;
};

const closeUserModal = () => {
  showUserModal.value = false;
  isUserEditMode.value = false;
  userForm.value = {
    id: null,
    username: "",
    email: "",
    password: "",
    phone_number: "",
    vehicle_number: "",
    role: "user"
  };
};

const submitUser = async () => {
  if (!checkAuth()) return;
  
  submitting.value = true;
  try {
    if (isUserEditMode.value) {
      console.log('Updating user:', userForm.value);
      // Create a copy of the form data and exclude password if it's empty
      const updateData = { ...userForm.value };
      if (!updateData.password || updateData.password.trim() === '') {
        delete updateData.password;
      }
      await api.updateUser(userForm.value.id, updateData);
      toast.success('User updated successfully!');
    } else {
      console.log('Creating user:', userForm.value);
      await api.createUser(userForm.value);
      toast.success('User created successfully!');
    }
    
    await fetchData(); // Refresh data
    closeUserModal();
  } catch (error) {
    console.error("Error submitting user:", error);
    handleApiError(error, `Failed to ${isUserEditMode.value ? 'update' : 'create'} user`);
  } finally {
    submitting.value = false;
  }
};

const deleteUser = async (id) => {
  if (!checkAuth()) return;
  
  if (!confirm("Are you sure you want to delete this user? This action cannot be undone.")) {
    return;
  }
  
  try {
    await api.deleteUser(id);
    toast.success('User deleted successfully!');
    await fetchData(); // Refresh data
  } catch (error) {
    console.error("Error deleting user:", error);
    handleApiError(error, 'Failed to delete user');
  }
};

// Initialize component
onMounted(() => {
  console.log('AdminDashboard mounted');
  getCurrentUser();
  fetchData();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Base Container - Landing Page Inspired */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Base Container */
.admin-dashboard-container {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
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

/* Stats Section */
.stats-section {
  margin-bottom: 4rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(252, 252, 252, 0.079);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: slideUpFade 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(30px);
  text-align: center;
}

@keyframes slideUpFade {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(96, 181, 245, 0.159), transparent);
  transition: left 0.6s;
}

.stat-card:hover::before {
  left: 100%;
}

.stat-card:hover {
  transform: translateY(-10px);
  border-color: rgba(13, 179, 230, 0.6);
  box-shadow: 0 20px 40px rgba(106, 159, 238, 0.2);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
  color: #00a8e8;
  margin-bottom: 1rem;
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

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0.5rem 0;
}

.stat-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
}


/* Section Container */
.section-container {
  background: rgba(255, 255, 255, 0.03);
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
  background: linear-gradient(90deg, transparent, #00a8e8, transparent);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
  text-align: center;
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
  /* transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); */
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

/* Table Styles */
.table-container {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(0, 102, 255, 0.1);
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
  background: rgba(21, 76, 165, 0.05);
}

/* Table Cell Components */
.location-info, .user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.location-name, .username {
  font-weight: 600;
  color: #ffffff;
}

.user-avatar {
  font-size: 1.5rem;
  color: #00a8e8;
}

/* Badges */
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
}

.pincode-badge {
  background:  linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
}

.price-badge {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #fff;
  font-weight: 600;
}

.count-badge {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.available-badge {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  color: #fff;
  font-weight: 600;
}

.available-badge.low {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
}

.vehicle-badge {
  background: rgba(56, 127, 226, 0.2);
  color: #00a8e8;
  font-family: 'Courier New', monospace;
}

.role-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.role-badge.admin {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #fff;
}

.role-badge.user {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.no-vehicle {
  color: rgba(255, 255, 255, 0.4);
  font-style: italic;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn.edit {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
}

.action-btn.edit:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.action-btn.delete {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: #fff;
}

.action-btn.delete:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

/* Loading and Empty States */
.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 215, 0, 0.2);
  border-top: 3px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state i {
  font-size: 3rem;
  color: rgba(255, 215, 0, 0.3);
  margin-bottom: 1rem;
  display: block;
}

.empty-state h3 {
  color: #667eea;
  margin-bottom: 0.5rem;
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
  overflow: hidden;
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
  max-width: 500px;
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
  overflow-x: hidden;
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
  min-width: 0;
  margin-right: 1rem;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
  border: 2px solid rgba(0, 34, 158, 0.2);
  border-radius: 15px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
  resize: vertical;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(90, 114, 219, 0.2);
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
  
  .main-content { 
    padding: 1rem; 
    padding-top: 80px; 
    overflow-x: hidden;
  }
  .main-title { font-size: 2rem; }
  .hero-section { padding: 2rem 1rem; }
  .stats-grid { grid-template-columns: 1fr; gap: 1rem; }
  .stat-card { padding: 1.5rem; }
  .section-container { 
    padding: 2rem 1.5rem; 
    overflow-x: hidden;
  }
  .section-header, .modal-footer { flex-direction: column; }
  .form-row { grid-template-columns: 1fr; }
  .modal-header { 
    padding: 1rem; 
    flex-direction: column; 
    text-align: center; 
    gap: 1rem; 
  }
  .cta-button { width: 100%; justify-content: center; }
  .hero-stats { gap: 2rem; }
  
  /* Modal specific mobile fixes */
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-container {
    max-width: calc(100vw - 1rem);
    margin: 0;
  }
  
  .modal-title-section {
    margin-right: 0;
  }
  
  .modal-footer {
    padding: 1rem;
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
  
  .admin-dashboard-container { 
    padding: 0; 
    overflow-x: hidden;
    width: 100vw;
  }
  .main-title { font-size: 1.8rem; }
  .main-content { 
    padding: 0.5rem; 
    padding-top: 60px; 
    overflow-x: hidden;
    width: 100%;
    padding-top: 80px;
  }
  .hero-section { padding: 1.5rem 1rem;  }
  .section-container { 
    padding: 1.5rem 1rem; 
    margin-left: 0;
    margin-right: 0;
    overflow-x: hidden;
  }
  .stat-card { padding: 1.5rem; }
  
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
}
</style>
