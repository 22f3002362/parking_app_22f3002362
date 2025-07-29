<template>
  <div class="register-container">
    <!-- Animated Background Elements -->
    <div class="bg-animation">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="register-section">
        <div class="brand-header">
          <div class="brand-logo">P</div>
          <h1 class="brand-title">ParkSmart</h1>
          <p class="brand-subtitle">Create your account and start parking smart!</p>
        </div>

        <div class="register-form-container">
          <form @submit.prevent="handleRegister" class="register-form">
            <!-- Full Name -->
            <div class="form-group">
              <label for="username" class="form-label">Full Name</label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                class="form-input"
                :class="{ 'error': errors.username }"
                placeholder="Enter your full name"
                required
              />
              <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
            </div>

            <!-- Email -->
            <div class="form-group">
              <label for="email" class="form-label">Email Address</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-input"
                :class="{ 'error': errors.email }"
                placeholder="Enter your email"
                required
              />
              <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            </div>
            <!-- Phone Number -->
            <div class="form-group">
              <label for="phone" class="form-label">Phone Number</label>
              <input
              id="phone"
              v-model="form.phone_number"
              type="tel"
              class="form-input"
              :class="{ 'error': errors.phone_number }"
              placeholder="Enter your phone number"
              required
              />
              <span v-if="errors.phone_number" class="error-message">{{ errors.phone_number }}</span>
            </div>
            
            <!-- Password -->
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <div class="password-wrapper">
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  :class="{ 'error': errors.password }"
                  placeholder="Create a password"
                  required
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="password-toggle"
                >
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            </div>

            <!-- Confirm Password -->
            <div class="form-group">
              <label for="confirmPassword" class="form-label">Confirm Password</label>
              <div class="password-wrapper">
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-input"
                  :class="{ 'error': errors.confirmPassword }"
                  placeholder="Confirm your password"
                  required
                />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="password-toggle"
                >
                  <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
            </div>

            <!-- Terms Checkbox -->
            <div class="form-options">
              <label class="remember-me">
                <input v-model="form.agreeToTerms" type="checkbox" />
                <span class="checkmark"></span>
                I agree to the Terms of Service and Privacy Policy
              </label>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="register-button"
              :class="{ 'loading': loading }"
              :disabled="loading"
            >
              <span v-if="loading" class="loading-spinner"></span>
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>

            <div class="form-divider"></div>

            <!-- Footer -->
            <div class="form-footer">
              <p>
                Already have an account?
                <router-link to="/login" class="login-link">Sign in</router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toast-notification'

const router = useRouter()
const toast = useToast()

// Form State
const form = reactive({
  username: '',
  email: '',
  phone_number: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false
})

const errors = reactive({
  username: '',
  email: '',
  phone_number: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// Validation Logic
const validateForm = () => {
  let isValid = true

  // Reset errors
  errors.username = ''
  errors.email = ''
  errors.phone_number = ''
  errors.password = ''
  errors.confirmPassword = ''

  if (!form.username) {
    errors.username = 'Full name is required'
    isValid = false
  } else if (form.username.length < 2) {
    errors.username = 'Name must be at least 2 characters'
    isValid = false
  }

  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  if (!form.phone_number) {
    errors.phone_number = 'Phone number is required'
    isValid = false
  } else if (!/^[0-9+\-\s()]{10,15}$/.test(form.phone_number.replace(/\s/g, ''))) {
    errors.phone_number = 'Please enter a valid phone number (10-15 digits)'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(form.password)) {
    errors.password = 'Password must contain at least one uppercase letter, one lowercase letter, and one number'
    isValid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (!form.agreeToTerms) {
    toast.error('Please agree to the Terms of Service and Privacy Policy')
    isValid = false
  }

  return isValid
}

// Submit Handler
const handleRegister = async () => {
  if (!validateForm()) return
  loading.value = true

  try {
    const response = await axios.post('/api/auth/register', {
      username: form.username,
      email: form.email,
      phone_number: form.phone_number,
      password: form.password
    });

    const { user, token } = response.data;

    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', token);

    toast.success('Account created successfully! Welcome to ParkSmart!');

    router.push(user.role === 'admin' ? '/admin-dashboard' : '/user-dashboard');
  } catch (error) {
    console.error('Registration error:', error);

    if (error.response?.data?.message) {
      toast.error(error.response.data.message);
    } else if (error.response?.status === 409) {
      toast.error('An account with this email already exists');
    } else {
      toast.error('Registration failed. Please try again.');
    }
  } finally {
    loading.value = false;
  }
}

// Animation setup
onMounted(() => {
  // Add animation class to trigger CSS animations
  const registerForm = document.querySelector('.register-form-container');
  if (registerForm) {
    registerForm.classList.add('animate-entrance');
  }
})
</script>
<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css');

* {
  box-sizing: border-box;
}

.register-container {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95), rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95));
  color: #ffffff;
}

/* Background Animation */
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
  filter: brightness(0.3);
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.shape-1 {
  width: 120px;
  height: 120px;
  background: linear-gradient(45deg, #ffd700, #ffed4a);
  top: 20%;
  left: 10%;
}

.shape-2 {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #ffffff, #f8f9fa);
  top: 60%;
  right: 15%;
}

.shape-3 {
  width: 100px;
  height: 100px;
  background: linear-gradient(45deg, #ffd700, #ffffff);
  bottom: 20%;
  left: 70%;
}

/* Main Layout */
.main-content {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-section {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 4rem;
}

/* Brand Header */
.brand-header {
  width: 40%;
  text-align: center;
}

.brand-logo {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #ffffff;
  font-weight: bold;
  margin: 0 0 1rem 7.6rem;
  box-shadow: 0 10px 20px rgba(0, 119, 190, 0.4);
}

.brand-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #00a8e8, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  color: #e5e5e5;
  font-size: 1rem;
}

/* Form */
.register-form-container {
  width: 55%;
}

.register-form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #ffffff;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.form-input::placeholder {
  color: #cccccc;
}

.form-input:focus {
  outline: none;
  border-color: #00a8e8;
  box-shadow: 0 0 0 3px rgba(0, 168, 232, 0.2);
}

.form-input.error {
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.2);
}

.error-message {
  color: #ff4757;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}

/* Password Field with Toggle */
.password-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #cccccc;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.25rem;
  border-radius: 4px;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #00a8e8;
}

/* Checkbox (Terms) */
.form-options {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.remember-me {
  display: flex;
  align-items: flex-start;
  font-size: 0.9rem;
  color: #e5e5e5;
  cursor: pointer;
  user-select: none;
  line-height: 1.4;
}

.remember-me input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  margin-right: 0.5rem;
  margin-top: 0.1rem;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.remember-me input:checked + .checkmark {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  border-color: #00a8e8;
}

.remember-me input:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #000000;
  font-weight: bold;
  font-size: 0.8rem;
}

/* Submit Button */
.register-button {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 168, 232, 0.4);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Divider & Footer */
.form-divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
  color: #cccccc;
}

.form-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
}

.form-divider span {
  background: rgba(255, 255, 255, 0.1);
  padding: 0 1rem;
  backdrop-filter: blur(10px);
}

.form-footer {
  text-align: center;
  margin-top: 2.5rem;
}

.form-footer p {
  color: #e5e5e5;
  font-size: 0.9rem;
  margin: 0;
}

.login-link {
  color: #00a8e8;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #0077be;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .register-section {
    flex-direction: column;
    gap: 2rem;
    padding: 2rem;
  }

  .brand-header {
    width: 100%;
    text-align: center;
  }

  .register-form-container {
    width: 100%;
  }

  .brand-title {
    font-size: 1.5rem;
  }

  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .register-section {
    padding: 1.5rem;
  }

  .brand-logo {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }

  .brand-title {
    font-size: 1.3rem;
  }
}

/* CSS Animations to replace GSAP */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float1 {
  0%, 100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) translateX(10px) rotate(180deg);
  }
}

@keyframes float2 {
  0%, 100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  50% {
    transform: translateY(15px) translateX(-15px) rotate(-180deg);
  }
}

@keyframes float3 {
  0%, 100% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) translateX(20px) rotate(90deg);
  }
}

/* Apply animations */
.register-form-container {
  opacity: 0;
  transform: translateY(50px);
}

.animate-entrance {
  animation: fadeInUp 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

/* Floating shapes animations */
.shape-1 {
  animation: float1 8s ease-in-out infinite;
}

.shape-2 {
  animation: float2 12s ease-in-out infinite;
}

.shape-3 {
  animation: float3 10s ease-in-out infinite;
}
</style>

