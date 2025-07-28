import { createRouter, createWebHistory } from 'vue-router'
// import Login from '../components/Login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/Landing.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/Login.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../components/Register.vue'),
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: () => import('../components/AdminDashboard.vue'),
    },
    {
      path: '/manage-users',
      name: 'manage-users',
      component: () => import('../components/UserManagement.vue'),
    },
    {
      path: '/user-dashboard',
      name: 'user-dashboard',
      component: () => import('../components/UserDashboard.vue'),
    },
    {
      path: '/find-parking',
      name: 'find-parking',
      component: () => import('../components/FindParking.vue'),
    },
    {
      path: '/parking-lots',
      name: 'parking-lots',
      component: () => import('../components/ParkingLots.vue'),
    },
    {
      path: '/my-bookings',
      name: 'my-bookings',
      component: () => import('../components/MyBookings.vue'),
    },
    {
      path: '/admin-reports',
      name: 'admin-reports',
      component: () => import('../components/AdminReports.vue'),
    },
    {
      path: '/user-reports',
      name: 'user-reports',
      component: () => import('../components/UserReports.vue'),
    }
  ],
})

export default router
