# API Integration Guide - Park-IT Frontend

## 🚀 **Overview**
The Park-IT frontend is now fully connected to the Flask backend API using axios for HTTP requests.

## 📁 **File Structure**
```
frontend/src/
├── services/
│   └── api.js          # API service with axios configuration
├── components/
│   ├── Register.vue    # Registration component with API integration
│   ├── Login.vue       # Login component with API integration
│   └── Landing.vue     # Landing page
└── router/
    └── index.js        # Vue router configuration
```

## 🔧 **API Configuration**

### Backend URL
- **Development**: `http://127.0.0.1:5000`
- **Production**: Update `API_BASE_URL` in `src/services/api.js`

### Axios Configuration
- **Timeout**: 10 seconds
- **Headers**: `Content-Type: application/json`
- **Error Handling**: Automatic error message extraction from backend responses

## 📋 **Registration API Integration**

### Form Fields
- **First Name** (required)
- **Last Name** (required)
- **Email** (required, validated)
- **Phone** (required, 10+ digits)
- **Password** (required, 8+ characters with strength indicator)
- **Confirm Password** (required, must match)
- **Vehicle Number** (optional, 3+ characters if provided)
- **Account Type** (required: 'user' for Driver, 'admin' for Parking Owner)
- **Terms Agreement** (required checkbox)
- **Updates Subscription** (optional checkbox)

### Backend Mapping
Frontend data is transformed to match backend User model:
```javascript
{
  username: "First Last",           // Combined first + last name
  email: "user@example.com",
  password: "userpassword",
  role: "user" | "admin",          // Maps to userType selection
  vehicle_number: "ABC123" | null  // Optional vehicle number
}
```

### API Endpoint
- **POST** `/users`
- **Response**: Success message + user object
- **Error Handling**: Displays backend error messages in toast notifications

## 🔐 **Login API Integration**

### Form Fields
- **Email** (required, validated)
- **Password** (required, 6+ characters)
- **Remember Me** (optional checkbox)

### Backend Communication
```javascript
// Request
{
  email: "user@example.com",
  password: "userpassword"
}

// Response
{
  msg: "Login successful",
  user: {
    id: 1,
    username: "John Doe",
    email: "user@example.com",
    role: "user",
    vehicle_number: "ABC123"
  }
}
```

### API Endpoint
- **POST** `/login`
- **Success**: Stores user data in localStorage and redirects based on role
- **Error Handling**: Displays error messages for invalid credentials

## 🎯 **Available API Methods**

### User Management
- `registerUser(userData)` - Create new user account
- `loginUser(credentials)` - User authentication
- `getUser(userId)` - Get user by ID
- `getAllUsers()` - Get all users
- `updateUser(userId, userData)` - Update user information
- `deleteUser(userId)` - Delete user account

### Parking Management
- `getParkingLots()` - Get all parking lots
- `getParkingLot(lotId)` - Get specific parking lot
- `createParkingLot(lotData)` - Create new parking lot
- `getAvailableSpots(lotId)` - Get available spots in a lot

### Reservations
- `createReservation(reservationData)` - Create new reservation
- `getUserReservations(userId)` - Get user's reservations
- `cancelReservation(reservationId)` - Cancel reservation

## 🚨 **Error Handling**

### Network Errors
- Automatic retry suggestions
- Connection timeout handling
- Server unavailability messages

### Validation Errors
- Real-time form validation
- Backend error message display
- Field-specific error highlighting

### Success Handling
- Toast notifications for successful operations
- Automatic form clearing after registration
- Smart redirects based on user role

## 🔄 **Usage Examples**

### Registration
```javascript
import apiService from '../services/api.js';

const registerUser = async () => {
  try {
    const response = await apiService.registerUser({
      username: "John Doe",
      email: "john@example.com",
      password: "securepass123",
      role: "user",
      vehicle_number: "KA01AB1234"
    });
    console.log('User registered:', response.user);
  } catch (error) {
    console.error('Registration failed:', error.message);
  }
};
```

### Login
```javascript
const loginUser = async () => {
  try {
    const response = await apiService.loginUser({
      email: "john@example.com",
      password: "securepass123"
    });
    localStorage.setItem('user', JSON.stringify(response.user));
  } catch (error) {
    console.error('Login failed:', error.message);
  }
};
```

## 🛠 **Development Setup**

1. **Backend**: Ensure Flask backend is running on `http://127.0.0.1:5000`
2. **Frontend**: Install dependencies and start dev server
```bash
cd frontend
npm install
npm run dev
```

3. **CORS**: Backend includes CORS configuration for frontend communication

## 📝 **Testing**

### Manual Testing
1. Start the Flask backend server
2. Open the frontend in browser
3. Test registration with various scenarios:
   - Valid data registration
   - Duplicate email handling
   - Form validation errors
   - Password strength validation

4. Test login with:
   - Valid credentials
   - Invalid credentials
   - Remember me functionality

### Network Tab Monitoring
- Check browser DevTools Network tab for API calls
- Verify request/response data structure
- Monitor error responses for debugging

## 🔒 **Security Features**

- Password strength indicator
- Client-side validation before API calls
- Secure password transmission
- Error message sanitization
- Automatic logout on token expiry (when implemented)

## 🚀 **Next Steps**

1. **Authentication Tokens**: Implement JWT tokens for session management
2. **Route Guards**: Add authentication guards to protected routes
3. **User Dashboard**: Create dashboard component with API integration
4. **Real-time Updates**: Add WebSocket support for live data
5. **Offline Support**: Implement service worker for offline functionality

---

**Note**: Make sure your Flask backend is running before testing the frontend integration!
