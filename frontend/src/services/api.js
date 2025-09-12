import axios from 'axios';

// API Configuration - use relative URLs to work with Vite proxy
const API_BASE_URL = '/api'; // This will be proxied to the Flask backend

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add JWT token if user is logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const accessToken = localStorage.getItem('access_token') || localStorage.getItem('token');

    console.log('API Request Interceptor:', {
      isLoggedIn,
      hasAccessToken: !!accessToken,
      tokenPreview: accessToken ? accessToken.substring(0, 20) + '...' : 'null'
    });

    if (isLoggedIn === 'true' && accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.msg || error.response.data?.message || 'An error occurred';
      error.message = message;
    } else if (error.request) {
      // Request was made but no response received
      error.message = 'Network error - please check your connection';
    }
    return Promise.reject(error);
  }
);

// API Service Functions
const apiService = {
  // User Management APIs
  async registerUser(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async loginUser(credentials) {
    try {
      const response = await apiClient.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUser(userId) {
    try {
      const response = await apiClient.get(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getAllUsers() {
    try {
      const response = await apiClient.get('/users');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async createUser(userData) {
    try {
      const response = await apiClient.post('/users', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async updateUser(userId, userData) {
    try {
      const response = await apiClient.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async deleteUser(userId) {
    try {
      const response = await apiClient.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Parking Lot APIs
  async getParkingLots() {
    try {
      const response = await apiClient.get('/parking-lots');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getParkingLot(lotId) {
    try {
      const response = await apiClient.get(`/parking-lots/${lotId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async createParkingLot(lotData) {
    try {
      const response = await apiClient.post('/parking-lots', lotData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async updateParkingLot(lotId, lotData) {
    try {
      const response = await apiClient.put(`/parking-lots/${lotId}`, lotData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async deleteParkingLot(lotId) {
    try {
      const response = await apiClient.delete(`/parking-lots/${lotId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Parking Spot APIs
  async getParkingSpots() {
    try {
      const response = await apiClient.get('/parking-spots');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getParkingSpot(spotId) {
    try {
      const response = await apiClient.get(`/parking-spots/${spotId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },



  async updateParkingSpot(spotId, spotData) {
    try {
      const response = await apiClient.put(`/parking-spots/${spotId}`, spotData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getAvailableSpots(lotId) {
    try {
      const response = await apiClient.get(`/parking-lots/${lotId}/available-spots`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Reservation APIs
  async createReservation(reservationData) {
    try {
      const response = await apiClient.post('/reservations', reservationData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async bookParkingSpot(lotId) {
    try {
      const response = await apiClient.post('/booking/book-spot', { lot_id: lotId });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async occupyParkingSpot(reservationId) {
    try {
      const response = await apiClient.post('/booking/occupy-spot', { reservation_id: reservationId });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async releaseParkingSpot(reservationId, transactionData = {}) {
    try {
      const payload = {
        reservation_id: reservationId,
        transaction_id: transactionData.transactionId,
        payment_method: transactionData.paymentMethod
      };
      const response = await apiClient.post('/booking/release-spot', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getReservation(reservationId) {
    try {
      const response = await apiClient.get(`/reservations/${reservationId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getAllReservations() {
    try {
      const response = await apiClient.get('/reservations');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async cancelReservation(reservationId) {
    try {
      const response = await apiClient.delete(`/reservations/${reservationId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUserReservations(userId) {
    try {
      console.log('API getUserReservations called with userId:', userId, typeof userId);
      // Ensure userId is a number
      const numericUserId = parseInt(userId);
      console.log('Converted to numeric userId:', numericUserId);

      const response = await apiClient.get(`/users/${numericUserId}/reservations`);
      console.log('getUserReservations API response:', response.data);
      return response.data;
    } catch (error) {
      console.error('getUserReservations API error:', error);
      console.error('Error response:', error.response?.data);
      throw error;
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await apiClient.get('/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Reports and Analytics APIs
  async getReportsData() {
    try {
      const response = await apiClient.get('/reports');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUserReportsData() {
    try {
      const response = await apiClient.get('/user-reports');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getUserBookingHistory() {
    try {
      const response = await apiClient.get('/user-booking-history');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async exportParkingDetails() {
    try {
      const response = await apiClient.get('/export/parking-details');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async generateMonthlyReport() {
    try {
      const response = await apiClient.get('/export/monthly-report');
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default apiService;

// Export individual functions for convenience
export const {
  registerUser,
  loginUser,
  getUser,
  getAllUsers,
  updateUser,
  deleteUser,
  getParkingLots,
  getParkingLot,
  createParkingLot,
  updateParkingLot,
  deleteParkingLot,
  getParkingSpots,
  getParkingSpot,
  updateParkingSpot,
  getAvailableSpots,
  createReservation,
  bookParkingSpot,
  occupyParkingSpot,
  releaseParkingSpot,
  getReservation,
  getAllReservations,
  cancelReservation,
  getUserReservations,
  healthCheck,
  getReportsData,
  getUserReportsData,
  getUserBookingHistory,
  exportParkingDetails,
  generateMonthlyReport
} = apiService;
