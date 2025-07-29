<template>
  <div class="landing-container">
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
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="main-title">Premium Parking Made Simple</h1>
          <p class="main-description">Book your perfect parking spot in seconds. Premium locations, guaranteed availability, and seamless experiences across the city.</p>
          <div class="cta-buttons">
            <button @click="navigateToLogin" class="cta-button primary">Get Started</button>
            <button class="cta-button secondary">How It Works</button>
          </div>
          <div class="features">
            <div class="feature-item">Secure Booking</div>
            <div class="feature-item">24/7 Access</div>
            <div class="feature-item">Prime Locations</div>
          </div>
        </div>
      </div>

<!-- Features Section -->
      <div class="features-section">
        <h2 class="features-title">Why Choose ParkEase</h2>
        <p class="features-description">Experience the future of parking with our premium features designed for modern urban living.</p>
        <div class="features-grid">
          <div class="feature-item">
            <h3>Prime Locations</h3>
            <p>Access to premium parking spots in the heart of the city, close to your destination.</p>
          </div>
          <div class="feature-item">
            <h3>Secure & Safe</h3>
            <p>24/7 security monitoring and well-lit facilities ensure your vehicle's safety.</p>
          </div>
          <div class="feature-item">
            <h3>Real-time Availability</h3>
            <p>Live updates on parking spot availability with instant booking confirmation.</p>
          </div>
          <div class="feature-item">
            <h3>Flexible Pricing</h3>
            <p>Transparent pricing with hourly, daily, and monthly options to suit your needs.</p>
          </div>
          <div class="feature-item">
            <h3>Mobile First</h3>
            <p>Seamless experience across all devices with our responsive mobile application.</p>
          </div>
          <div class="feature-item">
            <h3>Smart Notifications</h3>
            <p>Get notified about booking confirmations, reminders, and exclusive offers.</p>
          </div>
        </div>
      </div>

      <!-- Stats Section -->
      <div class="stats-section">
        <div class="stats-grid">
          <div 
            v-for="(stat, idx) in stats" 
            :key="idx"
            class="stat-card"
          >
            <div class="stat-number">{{ stat.number }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="footer">
        <div class="footer-container">
          <!-- Footer Bottom -->
          <div class="footer-bottom">
            <div class="footer-bottom-content">
              <p>&copy; 2025 PARKEASE. All rights reserved.</p>
              <p class="crafted-text">Crafted with precision for the modern world</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Features data
const features = [
  {
    icon: "bi bi-phone-vibrate",
    title: "Smart Booking",
    desc: "AI-powered spot recommendations with real-time availability and instant booking confirmation."
  },
  {
    icon: "bi bi-geo-alt-fill",
    title: "Prime Locations", 
    desc: "Exclusive access to premium parking spots in the heart of the city with guaranteed security."
  },
  {
    icon: "bi bi-shield-check",
    title: "Secure & Reliable",
    desc: "24/7 monitoring, secure payments, and comprehensive insurance coverage for your peace of mind."
  },
  {
    icon: "bi bi-lightning-charge",
    title: "Electric Vehicle Ready",
    desc: "Dedicated EV charging stations with fast charging capabilities and mobile notifications."
  }
];

const navigateToLogin = () => {
  console.log('Navigating to login...');
  router.push('/login');
};

// Stats data
const stats = [
  { number: "1000+", label: "Parking Spots" },
  { number: "50K+", label: "Happy Customers" },
  { number: "25+", label: "City Locations" },
  { number: "99.9%", label: "Uptime" }
];

onMounted(() => {
  console.log('Landing page mounted');
  
  // Add entrance animations class to trigger CSS animations
  const heroContent = document.querySelector('.hero-content');
  if (heroContent) {
    heroContent.classList.add('animate-entrance');
    console.log('Added animate-entrance class');
  }
  
  // Use correct class name for feature items
  const featureCards = document.querySelectorAll('.feature-item');
  featureCards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add('animate-feature');
    }, index * 150);
  });

  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add('animate-stat');
    }, index * 100 + 800);
  });
  
  console.log('Landing page animations initialized');
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.landing-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.95) 0%, rgba(45, 64, 89, 0.95) 50%, rgba(64, 83, 111, 0.95) 100%);
  color: #ffffff;
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
  filter: brightness(0.4);
  pointer-events: none;
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

/* Main Content */
.main-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Hero Section */
.hero-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(0,0,0,0.3) 0%, rgba(26,45,67,0.6) 100%);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  padding-top: 5rem;
}

.main-title {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 2rem;
  color: #ffffff;
  line-height: 1.1;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
}

.main-title::first-line {
  color: #00d4ff;
  font-size: 4.5rem;
}

.main-description {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  color: #e5e5e5;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 4rem;
}

.cta-button {
  padding: 1rem 2rem;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button.primary {
  background: linear-gradient(135deg, #0077be, #00a8e8);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 168, 232, 0.3);
}

.cta-button.secondary {
  background: transparent;
  color: #ffffff;
  border: 2px solid #ffffff;
  backdrop-filter: blur(10px);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
}

.features {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.features .feature-item {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-size: 0.9rem;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 2rem;
}

.logo-icon {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #ffd700, #ffed4a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #000000;
  box-shadow: 0 20px 40px rgba(255, 215, 0, 0.4);
  position: relative;
  z-index: 2;
}

.logo-pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffd700, #ffed4a);
  border-radius: 50%;
  z-index: 1;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #ffd700, #ffed4a, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  margin-bottom: 1.5rem;
  color: #ffd700;
  letter-spacing: 1px;
}

.hero-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  color: #e5e5e5;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-container {
  margin-top: 2rem;
}

.btn-icon {
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.cta-button:hover .btn-icon {
  transform: translateX(5px);
}

/* Features Section */
.features-section {
  padding: 6rem 2rem;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  color: #1a2d43;
}

.features-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

.features-description {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  max-width: 600px;
  margin: 0 auto 4rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #e5e5e5;
  max-width: 500px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid .feature-item {
  background: #ffffff;
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e5e5e5;
}

.features-grid .feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.features-grid .feature-item h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #333;
}

.features-grid .feature-item p {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 20px;
  padding: 2.5rem;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ffd700, #ffed4a, #ffffff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.8);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  color: #ffd700;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  color: #ffffff;
  transform: scale(1.1);
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #ffffff;
}

.feature-description {
  color: #e5e5e5;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Stats Section */
.stats-section {
  padding: 4rem 2rem;
  background: rgba(26,45,67,0.95);
  backdrop-filter: blur(10px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.stat-card {
  text-align: center;
  padding: 2rem;
  background: transparent;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(255, 255, 255, 0.2);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #00a8e8;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #ffffff;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Footer */
.footer {
  background: linear-gradient(135deg, rgba(26, 45, 67, 0.98) 0%, rgba(0, 0, 0, 0.95) 100%);
  border-top: 2px solid rgba(255, 215, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00a8e8, transparent);
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
}

.footer-bottom {
  padding: 2rem;
  background: rgba(0, 0, 0, 0.3);
}

.footer-bottom-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-bottom-content p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.crafted-text {
  color: #ffd700;
  font-style: italic;
  font-size: 0.85rem !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-title {
    font-size: 2.8rem;
    margin-bottom: 1.5rem;
  }
  
  .main-title::first-line {
    font-size: 3rem;
  }
  
  .main-description {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .hero-content {
    padding-top: 3rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .logo-icon {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .features-title {
    font-size: 2.2rem;
  }
  
  .features-description {
    font-size: 1rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .features-grid .feature-item {
    padding: 1.5rem;
  }
  
  .features-grid .feature-item h3 {
    font-size: 1.3rem;
  }
  
  .features-grid .feature-item p {
    font-size: 0.9rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .feature-card {
    padding: 2rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    gap: 0.8rem;
    align-items: center;
  }
  
  .cta-button {
    padding: 0.8rem 2rem;
    font-size: 0.9rem;
    width: 100%;
    max-width: 250px;
  }
  
  .features {
    gap: 1rem;
  }
  
  .features .feature-item {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }
  
  /* Footer Responsive */
  .footer-bottom {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 2.2rem;
    line-height: 1.2;
  }
  
  .main-title::first-line {
    font-size: 2.4rem;
  }
  
  .main-description {
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 2rem;
  }
  
  .hero-section {
    padding: 1rem;
    min-height: 90vh;
  }
  
  .hero-content {
    padding-top: 2rem;
  }
  
  .features-section {
    padding: 4rem 1rem;
  }
  
  .features-title {
    font-size: 1.8rem;
  }
  
  .features-description {
    font-size: 0.9rem;
  }
  
  .features-grid .feature-item {
    padding: 1.2rem;
  }
  
  .features-grid .feature-item h3 {
    font-size: 1.2rem;
  }
  
  .features-grid .feature-item p {
    font-size: 0.85rem;
  }
  
  .stats-section {
    padding: 3rem 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .stat-number {
    font-size: 1.8rem;
  }
  
  .stat-label {
    font-size: 0.75rem;
  }
  
  .cta-button {
    padding: 0.7rem 1.5rem;
    font-size: 0.85rem;
  }
  
  .features .feature-item {
    font-size: 0.75rem;
    padding: 0.3rem 0.6rem;
  }
  
  /* Footer Mobile */
  .footer-bottom {
    padding: 1rem;
  }
  
  .footer-bottom-content p {
    font-size: 0.85rem;
  }
  
  .crafted-text {
    font-size: 0.8rem !important;
  }
}

/* Ensure elements are visible by default */
.hero-content h1,
.hero-content p,
.cta-buttons,
.feature-item,
.stat-card {
  opacity: 1;
  transform: translateY(0);
}

/* CSS Animations - Clean definitions */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

/* Apply animations when classes are added (optional enhancement) */
.animate-entrance .hero-content h1,
.animate-entrance .hero-content p,
.animate-entrance .cta-buttons {
  animation: fadeInUp 0.8s ease-out forwards;
}

.animate-entrance .hero-content p {
  animation-delay: 0.2s;
}

.animate-entrance .cta-buttons {
  animation-delay: 0.4s;
}

.animate-feature {
  animation: fadeInScale 0.8s ease-out forwards;
}

.animate-stat {
  animation: fadeInUp 0.8s ease-out forwards;
}

.logo-pulse {
  animation: pulse 2s ease-in-out infinite;
}
</style>
