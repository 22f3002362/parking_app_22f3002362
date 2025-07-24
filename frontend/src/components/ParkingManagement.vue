<template>
  <div class="parking-management-container">
    <!-- Animated Background -->
    <div class="bg-animation">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <div class="container-fluid py-5">
      <!-- Header Section -->
      <div class="header-section text-center mb-5">
        <div class="logo-container mb-4">
          <div class="admin-logo">
            <i class="bi bi-geo-alt-fill"></i>
          </div>
        </div>
        <h1 class="page-title">Parking Lots Management</h1>
        <p class="page-subtitle">Manage all parking facilities and their operations</p>
      </div>

      <!-- Action Bar -->
      <div class="action-bar mb-4">
        <button class="premium-button" @click="openAddModal">
          <span class="btn-content">
            <i class="bi bi-plus-circle-fill"></i>
            <span>Add New Parking Lot</span>
          </span>
          <div class="btn-shimmer"></div>
        </button>
        <div class="search-container">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search parking lots..." 
            class="search-input"
          >
          <i class="bi bi-search search-icon"></i>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="premium-loading">
          <div class="loading-spinner"></div>
          <p class="loading-text">Loading parking lots...</p>
        </div>
      </div>

      <!-- Parking Lots Grid -->
      <div v-else class="parking-lots-grid">
        <div v-if="filteredLots.length === 0" class="empty-state">
          <i class="bi bi-building-add"></i>
          <h3>No Parking Lots Found</h3>
          <p>{{ searchQuery ? 'No lots match your search criteria' : 'Add your first parking lot to get started' }}</p>
          <button v-if="!searchQuery" class="premium-button" @click="openAddModal">
            <span class="btn-content">
              <i class="bi bi-plus-circle-fill"></i>
              <span>Add First Lot</span>
            </span>
          </button>
        </div>

        <div v-else v-for="lot in filteredLots" :key="lot.id" class="parking-lot-card">
          <div class="card-header">
            <div class="lot-info">
              <h3 class="lot-name">{{ lot.location_name }}</h3>
              <p class="lot-address">{{ lot.address }}</p>
            </div>
            <div class="lot-status" :class="{ 'available': lot.available_slots > 0, 'full': lot.available_slots === 0 }">
              {{ lot.available_slots > 0 ? 'Available' : 'Full' }}
            </div>
          </div>

          <div class="card-body">
            <div class="lot-details">
              <div class="detail-item">
                <i class="bi bi-geo-alt"></i>
                <span>Pincode: {{ lot.pincode }}</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-currency-dollar"></i>
                <span>₹{{ lot.price }}/hour</span>
              </div>
              <div class="detail-item">
                <i class="bi bi-car-front"></i>
                <span>{{ lot.available_slots }}/{{ lot.number_of_slots }} available</span>
              </div>
            </div>

            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${(lot.available_slots / lot.number_of_slots) * 100}%` }"
                ></div>
              </div>
              <span class="progress-text">{{ Math.round((lot.available_slots / lot.number_of_slots) * 100) }}% Available</span>
            </div>
          </div>

          <div class="card-actions">
            <button class="action-btn edit-btn" @click="openEditModal(lot)" title="Edit">
              <i class="bi bi-pencil-square"></i>
              <span>Edit</span>
            </button>
            <button class="action-btn view-btn" @click="viewLotDetails(lot)" title="View Details">
              <i class="bi bi-eye"></i>
              <span>View</span>
            </button>
            <button class="action-btn delete-btn" @click="confirmDelete(lot)" title="Delete">
              <i class="bi bi-trash"></i>
              <span>Delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2>{{ isEditing ? 'Edit Parking Lot' : 'Add New Parking Lot' }}</h2>
          <button class="close-btn" @click="closeModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <form @submit.prevent="saveLot" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label for="location_name">Location Name *</label>
              <input
                id="location_name"
                v-model="form.location_name"
                type="text"
                required
                placeholder="e.g., Downtown Plaza"
              >
            </div>
            <div class="form-group">
              <label for="price">Price per Hour (₹) *</label>
              <input
                id="price"
                v-model="form.price"
                type="number"
                step="0.01"
                min="0"
                required
                placeholder="e.g., 15.50"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="address">Address *</label>
            <textarea
              id="address"
              v-model="form.address"
              required
              placeholder="Enter complete address"
              rows="3"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="pincode">Pincode *</label>
              <input
                id="pincode"
                v-model="form.pincode"
                type="text"
                required
                placeholder="e.g., 400001"
                pattern="[0-9]{6}"
              >
            </div>
            <div class="form-group">
              <label for="number_of_slots">Total Parking Slots *</label>
              <input
                id="number_of_slots"
                v-model="form.number_of_slots"
                type="number"
                min="1"
                required
                placeholder="e.g., 50"
              >
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">Cancel</button>
            <button type="submit" class="save-btn" :disabled="saving">
              <span v-if="saving" class="loading-spinner small"></span>
              {{ saving ? 'Saving...' : (isEditing ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-container small" @click.stop>
        <div class="modal-header">
          <h2>Confirm Delete</h2>
          <button class="close-btn" @click="closeDeleteModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="modal-body">
          <div class="delete-warning">
            <i class="bi bi-exclamation-triangle"></i>
            <p>Are you sure you want to delete <strong>{{ lotToDelete?.location_name }}</strong>?</p>
            <p class="warning-text">This action cannot be undone and will delete all associated parking spots.</p>
          </div>
        </div>

        <div class="modal-actions">
          <button type="button" class="cancel-btn" @click="closeDeleteModal">Cancel</button>
          <button type="button" class="delete-btn" @click="deleteLot" :disabled="deleting">
            <span v-if="deleting" class="loading-spinner small"></span>
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { useToast } from 'vue-toast-notification'

const router = useRouter()
const toast = useToast()

// Reactive state
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const lots = ref([])
const searchQuery = ref('')
const showModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const lotToDelete = ref(null)

const form = reactive({
  id: null,
  location_name: '',
  price: '',
  address: '',
  pincode: '',
  number_of_slots: ''
})

// Computed
const filteredLots = computed(() => {
  if (!searchQuery.value) return lots.value
  
  const query = searchQuery.value.toLowerCase()
  return lots.value.filter(lot => 
    lot.location_name.toLowerCase().includes(query) ||
    lot.address.toLowerCase().includes(query) ||
    lot.pincode.includes(query)
  )
})

// Methods
const fetchLots = async () => {
  loading.value = true
  try {
    const response = await api.getParkingLots()
    lots.value = response.lots || []
  } catch (error) {
    console.error('Error fetching lots:', error)
    toast.error('Failed to fetch parking lots')
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  isEditing.value = false
  resetForm()
  showModal.value = true
}

const openEditModal = (lot) => {
  isEditing.value = true
  Object.assign(form, lot)
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const resetForm = () => {
  Object.assign(form, {
    id: null,
    location_name: '',
    price: '',
    address: '',
    pincode: '',
    number_of_slots: ''
  })
}

const saveLot = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      await api.updateParkingLot(form.id, form)
      toast.success('Parking lot updated successfully!')
    } else {
      await api.createParkingLot(form)
      toast.success('Parking lot created successfully!')
    }
    
    closeModal()
    await fetchLots()
  } catch (error) {
    console.error('Error saving lot:', error)
    toast.error(error.response?.data?.msg || 'Failed to save parking lot')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (lot) => {
  lotToDelete.value = lot
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  lotToDelete.value = null
}

const deleteLot = async () => {
  if (!lotToDelete.value) return
  
  deleting.value = true
  try {
    await api.deleteParkingLot(lotToDelete.value.id)
    toast.success('Parking lot deleted successfully!')
    closeDeleteModal()
    await fetchLots()
  } catch (error) {
    console.error('Error deleting lot:', error)
    toast.error(error.response?.data?.msg || 'Failed to delete parking lot')
  } finally {
    deleting.value = false
  }
}

const viewLotDetails = (lot) => {
  // Navigate to lot details or show detailed modal
  toast.info(`Viewing details for ${lot.location_name}`)
}

// Lifecycle
onMounted(() => {
  fetchLots()
})
</script>

<style scoped>
/* Base Styles */
.parking-management-container {
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
  position: relative;
  overflow-x: hidden;
  padding-top: 120px;
}

/* Animated Background */
.bg-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  animation: float 8s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  background: linear-gradient(45deg, #ffd700, #ffed4a);
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #0077be, #00a8e8);
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #ffffff, #f8f9fa);
  top: 40%;
  left: 60%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-20px) scale(1.1); }
}

/* Header */
.header-section {
  margin-bottom: 3rem;
}

.admin-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #ffd700, #ffed4a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 2rem;
  color: #1a2d43;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  margin: 1rem 0;
  background: linear-gradient(45deg, #ffffff, #00d4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* Action Bar */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.premium-button {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border: none;
  border-radius: 25px;
  padding: 12px 24px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 168, 232, 0.4);
}

.premium-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 25px rgba(0, 168, 232, 0.6);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 1;
}

.btn-shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.premium-button:hover .btn-shimmer {
  left: 100%;
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

/* Loading */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.premium-loading {
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top: 3px solid #00a8e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.loading-spinner.small {
  width: 20px;
  height: 20px;
  border-width: 2px;
  margin: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
}

/* Parking Lots Grid */
.parking-lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.parking-lot-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.parking-lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.lot-name {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
}

.lot-address {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 0.9rem;
}

.lot-status {
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.lot-status.available {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.lot-status.full {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.card-body {
  margin-bottom: 1.5rem;
}

.lot-details {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.detail-item i {
  color: #00a8e8;
  width: 16px;
}

.progress-container {
  margin-top: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

.card-actions {
  display: flex;
  gap: 0.7rem;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 100px;
  padding: 0.7rem 1rem;
  border: none;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.action-btn.edit-btn {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.action-btn.edit-btn:hover {
  background: rgba(255, 193, 7, 0.3);
  transform: translateY(-2px);
}

.action-btn.view-btn {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.action-btn.view-btn:hover {
  background: rgba(33, 150, 243, 0.3);
  transform: translateY(-2px);
}

.action-btn.delete-btn {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.action-btn.delete-btn:hover {
  background: rgba(244, 67, 54, 0.3);
  transform: translateY(-2px);
}

/* Empty State */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.6);
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.3);
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-container {
  background: rgba(26, 45, 67, 0.95);
  border-radius: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-container.small {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  margin: 0;
  color: #ffffff;
  font-size: 1.3rem;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.modal-form {
  padding: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #00a8e8;
  box-shadow: 0 0 20px rgba(0, 168, 232, 0.3);
  background: rgba(255, 255, 255, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.cancel-btn,
.save-btn,
.delete-btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.save-btn {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 168, 232, 0.4);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.delete-btn {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.delete-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(244, 67, 54, 0.4);
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Delete Modal */
.modal-body {
  padding: 2rem;
}

.delete-warning {
  text-align: center;
}

.delete-warning i {
  font-size: 3rem;
  color: #f44336;
  margin-bottom: 1rem;
}

.delete-warning p {
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.warning-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .parking-management-container {
    padding-top: 100px;
  }
  
  .action-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-container {
    max-width: none;
  }
  
  .parking-lots-grid {
    grid-template-columns: 1fr;
    padding: 0;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-container {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .card-actions {
    justify-content: center;
  }
  
  .action-btn {
    flex: 0 1 auto;
    min-width: 80px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 2rem;
  }
  
  .parking-lot-card {
    padding: 1rem;
  }
  
  .modal-header,
  .modal-form,
  .modal-actions {
    padding: 1rem;
  }
}
</style>
