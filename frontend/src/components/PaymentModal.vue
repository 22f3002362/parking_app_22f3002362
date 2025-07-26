<template>
  <div v-if="isVisible" class="payment-modal-overlay" @click="closeModal">
    <div class="payment-modal" @click.stop>
      <!-- Payment Header -->
      <div class="payment-header">
        <h2>
          <i class="bi bi-credit-card"></i>
          Complete Payment to Release Parking
        </h2>
        <button @click="closeModal" class="close-btn">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <!-- Payment Content -->
      <div class="payment-content">
        <!-- Booking Details -->
        <div class="booking-summary">
          <h3>Booking Summary</h3>
          <div class="summary-item">
            <span class="label">Parking Spot:</span>
            <span class="value">#{{ reservation?.spot_id || 'N/A' }}</span>
          </div>
          <div class="summary-item">
            <span class="label">Location:</span>
            <span class="value">{{ reservation?.lot_name || 'Unknown Location' }}</span>
          </div>
          <div class="summary-item">
            <span class="label">Duration:</span>
            <span class="value">{{ calculatedDuration }}</span>
          </div>
          <div class="summary-item total">
            <span class="label">Total Amount:</span>
            <span class="value amount">₹{{ totalAmount }}</span>
          </div>
        </div>

        <!-- Payment Methods -->
        <div class="payment-methods">
          <h3>Choose Payment Method</h3>
          <div class="method-tabs">
            <button 
              @click="paymentMethod = 'qr'" 
              :class="['method-tab', { active: paymentMethod === 'qr' }]"
            >
              <i class="bi bi-qr-code"></i>
              UPI/QR Code
            </button>
            <button 
              @click="paymentMethod = 'card'" 
              :class="['method-tab', { active: paymentMethod === 'card' }]"
            >
              <i class="bi bi-credit-card"></i>
              Credit/Debit Card
            </button>
          </div>

          <!-- QR Code Payment -->
          <div v-if="paymentMethod === 'qr'" class="payment-section qr-section">
            <div class="qr-container">
              <div class="qr-code">
                <canvas ref="qrCanvas" width="200" height="200"></canvas>
              </div>
              <p class="qr-instructions">
                Scan this QR code with any UPI app to pay ₹{{ totalAmount }}
              </p>
              <div class="upi-apps">
                <span class="upi-label">Accepted UPI Apps:</span>
                <div class="upi-icons">
                  <span class="upi-app">GPay</span>
                  <span class="upi-app">PhonePe</span>
                  <span class="upi-app">Paytm</span>
                  <span class="upi-app">BHIM</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card Payment -->
          <div v-if="paymentMethod === 'card'" class="payment-section card-section">
            <form @submit.prevent="processPayment">
              <div class="form-group">
                <label>Card Number</label>
                <input 
                  type="text" 
                  v-model="cardDetails.number" 
                  placeholder="1234 5678 9012 3456"
                  maxlength="19"
                  @input="formatCardNumber"
                >
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Expiry Date</label>
                  <input 
                    type="text" 
                    v-model="cardDetails.expiry" 
                    placeholder="MM/YY"
                    maxlength="5"
                    @input="formatExpiry"
                  >
                </div>
                <div class="form-group">
                  <label>CVV</label>
                  <input 
                    type="text" 
                    v-model="cardDetails.cvv" 
                    placeholder="123"
                    maxlength="3"
                  >
                </div>
              </div>
              <div class="form-group">
                <label>Cardholder Name</label>
                <input 
                  type="text" 
                  v-model="cardDetails.name" 
                  placeholder="John Doe"
                >
              </div>
            </form>
          </div>
        </div>

        <!-- Payment Actions -->
        <div class="payment-actions">
          <button @click="closeModal" class="cancel-btn">
            <i class="bi bi-x-circle"></i>
            Cancel
          </button>
          <button 
            @click="processPayment" 
            :disabled="processing"
            class="pay-btn"
          >
            <i class="bi bi-credit-card" v-if="!processing"></i>
            <i class="bi bi-arrow-repeat spin" v-if="processing"></i>
            {{ processing ? 'Processing...' : `Pay ₹${totalAmount}` }}
          </button>
        </div>
      </div>

      <!-- Payment Success -->
      <div v-if="paymentSuccess" class="payment-success-overlay">
        <div class="success-content">
          <div class="success-icon">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <h2>Payment Successful!</h2>
          <p>Your payment of ₹{{ totalAmount }} has been processed successfully.</p>
          <div class="transaction-details">
            <div class="detail-item">
              <span>Transaction ID:</span>
              <span class="transaction-id">{{ transactionId }}</span>
            </div>
            <div class="detail-item">
              <span>Payment Method:</span>
              <span>{{ paymentMethod === 'qr' ? 'UPI' : 'Card' }}</span>
            </div>
            <div class="detail-item">
              <span>Time:</span>
              <span>{{ new Date().toLocaleString() }}</span>
            </div>
          </div>
          <button @click="redirectToDashboard" class="success-btn">
            <i class="bi bi-house"></i>
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'PaymentModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    reservation: {
      type: Object,
      default: () => ({})
    },
    amount: {
      type: Number,
      default: 0
    }
  },
  emits: ['close', 'payment-success'],
  setup(props, { emit }) {
    const router = useRouter()
    const qrCanvas = ref(null)
    const paymentMethod = ref('qr')
    const processing = ref(false)
    const paymentSuccess = ref(false)
    const transactionId = ref('')

    const cardDetails = ref({
      number: '',
      expiry: '',
      cvv: '',
      name: ''
    })

    // Calculate total amount with some random fees
    const totalAmount = computed(() => {
      const baseAmount = props.amount || Math.floor(Math.random() * 100) + 20
      const platformFee = Math.ceil(baseAmount * 0.05) // 5% platform fee
      return baseAmount + platformFee
    })

    // Calculate parking duration
    const calculatedDuration = computed(() => {
      if (!props.reservation?.parking_time) return 'N/A'
      
      const startTime = new Date(props.reservation.parking_time)
      const now = new Date()
      const diffMs = now - startTime
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      
      if (diffHours > 0) {
        return `${diffHours}h ${diffMinutes}m`
      } else {
        return `${diffMinutes}m`
      }
    })

    // Generate fake but realistic QR code
    const generateQRCode = () => {
      if (!qrCanvas.value) return
      
      const canvas = qrCanvas.value
      const ctx = canvas.getContext('2d')
      
      // Clear canvas
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(0, 0, 200, 200)
      
      // Generate realistic QR pattern
      ctx.fillStyle = '#000000'
      const moduleSize = 4
      const modules = 50 // 50x50 modules for version 1 QR code
      
      // Create matrix for QR code pattern
      const matrix = Array(modules).fill().map(() => Array(modules).fill(false))
      
      // Add finder patterns (3 corner squares)
      const addFinderPattern = (x, y) => {
        // Outer 7x7 square
        for (let i = 0; i < 7; i++) {
          for (let j = 0; j < 7; j++) {
            if (x + i < modules && y + j < modules) {
              matrix[x + i][y + j] = true
            }
          }
        }
        // Inner 5x5 white square
        for (let i = 1; i < 6; i++) {
          for (let j = 1; j < 6; j++) {
            if (x + i < modules && y + j < modules) {
              matrix[x + i][y + j] = false
            }
          }
        }
        // Center 3x3 black square
        for (let i = 2; i < 5; i++) {
          for (let j = 2; j < 5; j++) {
            if (x + i < modules && y + j < modules) {
              matrix[x + i][y + j] = true
            }
          }
        }
      }
      
      // Add finder patterns at three corners
      addFinderPattern(0, 0)     // Top-left
      addFinderPattern(0, 43)    // Top-right
      addFinderPattern(43, 0)    // Bottom-left
      
      // Add timing patterns
      for (let i = 8; i < 42; i++) {
        matrix[6][i] = (i % 2 === 0)
        matrix[i][6] = (i % 2 === 0)
      }
      
      // Fill data area with semi-random pattern
      for (let x = 0; x < modules; x++) {
        for (let y = 0; y < modules; y++) {
          // Skip finder patterns and timing patterns
          if ((x < 9 && y < 9) || (x < 9 && y > 40) || (x > 40 && y < 9) ||
              x === 6 || y === 6) {
            continue
          }
          
          // Create pseudo-random but structured pattern
          const hash = (x * 7 + y * 13 + totalAmount.value * 17) % 100
          matrix[x][y] = hash > 45
        }
      }
      
      // Draw the matrix on canvas
      for (let x = 0; x < modules; x++) {
        for (let y = 0; y < modules; y++) {
          if (matrix[x][y]) {
            ctx.fillRect(x * moduleSize, y * moduleSize, moduleSize, moduleSize)
          }
        }
      }
    }

    // Format card number input
    const formatCardNumber = (event) => {
      let value = event.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '')
      let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value
      cardDetails.value.number = formattedValue
    }

    // Format expiry date input
    const formatExpiry = (event) => {
      let value = event.target.value.replace(/\D/g, '')
      if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4)
      }
      cardDetails.value.expiry = value
    }

    // Generate transaction ID
    const generateTransactionId = () => {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
      let result = 'TXN'
      for (let i = 0; i < 10; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      return result
    }

    // Process payment
    const processPayment = async () => {
      if (processing.value) return

      // Validate card details if card payment
      if (paymentMethod.value === 'card') {
        if (!cardDetails.value.number || !cardDetails.value.expiry || 
            !cardDetails.value.cvv || !cardDetails.value.name) {
          alert('Please fill in all card details')
          return
        }
      }

      processing.value = true
      
      try {
        // Simulate payment processing delay
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Generate transaction ID
        transactionId.value = generateTransactionId()
        
        // Show success
        paymentSuccess.value = true
        
        // Emit success event after a short delay
        setTimeout(() => {
          emit('payment-success', {
            transactionId: transactionId.value,
            amount: totalAmount.value,
            paymentMethod: paymentMethod.value
          })
        }, 1500)
        
      } catch (error) {
        alert('Payment failed. Please try again.')
      } finally {
        processing.value = false
      }
    }

    // Close modal
    const closeModal = () => {
      if (!processing.value && !paymentSuccess.value) {
        emit('close')
      }
    }

    // Redirect to dashboard
    const redirectToDashboard = () => {
      emit('close')
      router.push('/user-dashboard')
    }

    // Watch for modal visibility to generate QR code
    watch(() => props.isVisible, (newVal) => {
      console.log('🎯 PaymentModal visibility changed to:', newVal)
      console.log('Props reservation:', props.reservation)
      console.log('Props amount:', props.amount)
      if (newVal) {
        // Reset states when modal opens
        paymentSuccess.value = false
        processing.value = false
        paymentMethod.value = 'qr'
        transactionId.value = ''
        
        // Clear card details
        cardDetails.value = {
          number: '',
          expiry: '',
          cvv: '',
          name: ''
        }
        
        setTimeout(() => {
          generateQRCode()
        }, 100)
      }
    })

    onMounted(() => {
      if (props.isVisible) {
        generateQRCode()
      }
    })

    return {
      qrCanvas,
      paymentMethod,
      processing,
      paymentSuccess,
      transactionId,
      cardDetails,
      totalAmount,
      calculatedDuration,
      formatCardNumber,
      formatExpiry,
      processPayment,
      closeModal,
      redirectToDashboard
    }
  }
}
</script>

<style scoped>
.payment-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
  animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.payment-modal {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(23, 83, 148, 0.3);
  border-radius: 25px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
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

.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.payment-header h2 {
  color: #ffffff;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  color: #ffffff;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 107, 107, 0.8);
  transform: scale(1.1);
}

.payment-content {
  padding: 2rem;
}

.booking-summary {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.booking-summary:hover {
  background: rgba(255, 255, 255, 0.08);
}

.booking-summary h3 {
  color: #00a8e8;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  color: #ffffff;
}

.summary-item.total {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 0.75rem;
  margin-top: 0.75rem;
  font-weight: 600;
}

.summary-item .label {
  opacity: 0.8;
}

.summary-item .value {
  font-weight: 500;
}

.summary-item .amount {
  color: #00a8e8;
  font-size: 1.2rem;
  font-weight: 700;
}

.payment-methods h3 {
  color: #ffffff;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.method-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5rem;
  border-radius: 12px;
}

.method-tab {
  flex: 1;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.method-tab:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
}

.method-tab.active {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 168, 232, 0.3);
}

.payment-section {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.payment-section:hover {
  background: rgba(255, 255, 255, 0.08);
}

.qr-container {
  text-align: center;
}

.qr-code {
  display: inline-block;
  padding: 1rem;
  background: #ffffff;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.qr-instructions {
  color: #ffffff;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.upi-apps {
  text-align: center;
}

.upi-label {
  color: #00a8e8;
  font-size: 0.9rem;
  font-weight: 500;
}

.upi-icons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.upi-app {
  background: rgba(0, 168, 232, 0.2);
  color: #00a8e8;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #00a8e8;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(0, 168, 232, 0.1);
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-row {
  display: flex;
  gap: 1rem;
}

.payment-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn, .pay-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.pay-btn {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 168, 232, 0.3);
}

.pay-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #005fa3, #0094d1);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 168, 232, 0.4);
}

.pay-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.payment-success-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 26, 26, 0.98);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 25px;
  animation: successFadeIn 0.5s ease-out;
}

@keyframes successFadeIn {
  from { 
    opacity: 0;
    transform: scale(0.9);
  }
  to { 
    opacity: 1;
    transform: scale(1);
  }
}

.success-content {
  text-align: center;
  padding: 2rem;
}

.success-icon {
  font-size: 4rem;
  color: #28a745;
  margin-bottom: 1rem;
}

.success-content h2 {
  color: #ffffff;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.success-content p {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}

.transaction-details {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.transaction-id {
  font-family: monospace;
  color: #00a8e8;
  font-weight: 600;
}

.success-btn {
  background: linear-gradient(135deg, #28a745, #20692e);
  color: #ffffff;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.success-btn:hover {
  background: linear-gradient(135deg, #20692e, #1e5f2a);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(40, 167, 69, 0.4);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .payment-modal {
    margin: 1rem;
    max-width: none;
    border-radius: 20px;
  }
  
  .payment-header, .payment-content {
    padding: 1.5rem;
  }
  
  .payment-header h2 {
    font-size: 1.5rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .payment-actions {
    flex-direction: column;
  }
  
  .method-tabs {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .method-tab {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .payment-modal {
    margin: 0.5rem;
    max-height: 95vh;
  }
  
  .payment-header, .payment-content {
    padding: 1rem;
  }
  
  .payment-header h2 {
    font-size: 1.3rem;
  }
  
  .booking-summary, .payment-section {
    padding: 1rem;
  }
}
</style>
