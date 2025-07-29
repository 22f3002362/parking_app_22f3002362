from flask_restful import Resource, Api
from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, ParkingLot, ParkingSpot, ReserveSpot
from datetime import datetime, timedelta
import calendar
import math
import json

# Redis utility functions
def get_redis_client():
    """Get Redis client from Flask app context"""
    return getattr(current_app, 'redis_client', None)

def cache_set(key, value, expiry_seconds=300):
    """Set cache with expiry"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            redis_client.setex(key, expiry_seconds, json.dumps(value))
            return True
        except Exception as e:
            print(f"Redis cache set error: {e}")
    return False

def cache_get(key):
    """Get cached value"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            cached_data = redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis cache get error: {e}")
    return None

def cache_delete(key):
    """Delete cache key"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis cache delete error: {e}")
    return False

def clear_all_cache():
    """Clear all application cache"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            # Get all cache keys
            cache_keys = redis_client.keys('users:*') + redis_client.keys('user:*') + redis_client.keys('parking_lot*')
            if cache_keys:
                redis_client.delete(*cache_keys)
            print(f"✅ Cleared {len(cache_keys)} cache keys")
            return True
        except Exception as e:
            print(f"Redis cache clear error: {e}")
    return False

def increment_counter(key):
    """Increment counter in Redis"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            return redis_client.incr(key)
        except Exception as e:
            print(f"Redis counter error: {e}")
    return 0

def add_to_set(key, value, expiry_seconds=3600):
    """Add value to Redis set"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            redis_client.sadd(key, value)
            redis_client.expire(key, expiry_seconds)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
    return False

def rate_limit_check(user_id, endpoint, max_requests=100, window_seconds=3600):
    """Check rate limit for user"""
    redis_client = get_redis_client()
    if redis_client:
        try:
            key = f'rate_limit:{user_id}:{endpoint}'
            current_requests = redis_client.get(key)
            
            if current_requests is None:
                redis_client.setex(key, window_seconds, 1)
                return True
            elif int(current_requests) < max_requests:
                redis_client.incr(key)
                return True
            else:
                return False
        except Exception as e:
            print(f"Redis rate limit error: {e}")
    return True  # Allow if Redis is unavailable

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Rate limiting
        if not rate_limit_check(current_user_id, 'get_users', 50, 3600):
            return {'msg': 'Rate limit exceeded. Try again later.'}, 429
        
        # Increment API usage counter
        increment_counter('api_calls:users:get')
        
        if user_id:
            # Only allow users to access their own data or admin to access any
            if current_user.role != 'admin' and current_user_id != user_id:
                return {'msg': 'Access denied'}, 403
            
            # Try to get user from cache first
            cache_key = f'user:{user_id}'
            cached_user = cache_get(cache_key)
            if cached_user:
                return cached_user, 200
                
            user = User.query.get(user_id)
            if user:
                user_data = {
                    'msg': 'User found',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'vehicle_number': user.vehicle_number,
                        'phone_number': user.phone_number if user.phone_number else None
                    }
                }
                # Cache user data for 10 seconds only to prevent stale data
                cache_set(cache_key, user_data, 10)
                return user_data, 200
            return {'msg': 'User not found'}, 404
        
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
        
        cache_key = 'users:all'
        cached_users = cache_get(cache_key)
        if cached_users:
            return cached_users, 200
            
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'vehicle_number': user.vehicle_number,
                'phone_number': user.phone_number
            })
        
        response_data = {'msg': 'Users retrieved successfully', 'users': user_list}
        # Cache users list for 10 seconds only to prevent stale data
        cache_set(cache_key, response_data, 10)
        return response_data, 200
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        vehicle_number = data.get('vehicle_number')
        phone_number = data.get('phone_number', None)
        
        if not email or not username or not password:
            return {'msg': 'Please provide email, username, and password'}, 400
        
        # Normalize email and username
        email = email.lower().strip()
        username = username.strip()
        
        # Check if user already exists (case-insensitive)
        existing_user = User.query.filter(User.email.ilike(email)).first()
        if existing_user:
            return {'msg': f'User with email {email} already exists'}, 400
        
        # Check if username already exists (case-insensitive)
        existing_username = User.query.filter(User.username.ilike(username)).first()
        if existing_username:
            return {'msg': f'Username {username} already exists'}, 400
        
        # Check if vehicle number already exists (only if provided)
        if vehicle_number:
            existing_vehicle = User.query.filter_by(vehicle_number=vehicle_number).first()
            if existing_vehicle:
                return {'msg': 'Vehicle number already exists'}, 400
        
        # Create new user
        user = User(
            email=email,
            username=username,
            password=password,
            role=role,
            vehicle_number=vehicle_number if vehicle_number else None,
            phone_number=phone_number if 'phone_number' in data else None
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Invalidate users cache when new user is created
            cache_delete('users:all')
            increment_counter('users_created')
            
            return {
                'msg': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'vehicle_number': user.vehicle_number,
                    'phone_number': user.phone_number
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            if 'UNIQUE constraint failed: user.email' in error_msg:
                return {'msg': 'Email already exists'}, 400
            elif 'UNIQUE constraint failed: user.username' in error_msg:
                return {'msg': 'Username already exists'}, 400
            elif 'UNIQUE constraint failed: user.vehicle_number' in error_msg:
                return {'msg': 'Vehicle number already exists'}, 400
            else:
                return {'msg': 'Error creating user', 'error': str(e)}, 500
    
    @jwt_required()
    def put(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Convert user_id to int for proper comparison
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return {'msg': 'Invalid user ID'}, 400
        
        # Only allow users to update their own data or admin to update any
        if current_user.role != 'admin' and current_user_id != user_id:
            return {'msg': 'Access denied'}, 403
            
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        
        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'role' in data and current_user.role == 'admin':
            user.role = data['role']
        if 'vehicle_number' in data:
            # Check if vehicle number is unique (only if it's different from current)
            if data['vehicle_number'] and data['vehicle_number'] != user.vehicle_number:
                existing_vehicle = User.query.filter_by(vehicle_number=data['vehicle_number']).first()
                if existing_vehicle:
                    return {'msg': 'Vehicle number already exists'}, 409
            user.vehicle_number = data['vehicle_number']
        if 'phone_number' in data:
            # Check if phone number is unique (only if it's different from current)
            if data['phone_number'] and data['phone_number'] != user.phone_number:
                existing_phone = User.query.filter_by(phone_number=data['phone_number']).first()
                if existing_phone:
                    return {'msg': 'Phone number already exists'}, 409
            user.phone_number = data['phone_number']
        
        try:
            db.session.commit()
            
            # Invalidate user cache when updated
            cache_delete(f'user:{user.id}')
            cache_delete('users:all')
            
            return {
                'msg': 'User updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'vehicle_number': user.vehicle_number,
                    'phone_number': user.phone_number
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error updating user', 'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Only admin can delete users
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
            
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        
        # Prevent deletion of admin users (optional safety check)
        if user.role == 'admin':
            return {'msg': 'Cannot delete admin users for security reasons'}, 403
        
        try:
            # Handle related records before deleting user
            
            # 1. Check for active reservations
            active_reservations = ReserveSpot.query.filter_by(user_id=user_id).filter(
                ReserveSpot.leaving_time.is_(None)
            ).all()
            
            if active_reservations:
                # Release all active parking spots and complete reservations
                for reservation in active_reservations:
                    spot = ParkingSpot.query.get(reservation.spot_id)
                    if spot:
                        spot.status = 'available'
                        spot.user_id = None
                        
                        # Update available slots in the parking lot
                        lot = ParkingLot.query.get(spot.lot_id)
                        if lot:
                            lot.available_slots += 1
                    
                    # Mark reservation as completed with current time
                    reservation.leaving_time = datetime.now()
                    
                    # Calculate final cost if not already set
                    if reservation.parking_cost == 0:
                        lot = ParkingLot.query.get(spot.lot_id) if spot else None
                        if lot:
                            duration_hours = (reservation.leaving_time - reservation.parking_time).total_seconds() / 3600
                            reservation.parking_cost = duration_hours * lot.price
            
            # 2. Clear user_id from any parking spots still assigned to this user
            assigned_spots = ParkingSpot.query.filter_by(user_id=user_id).all()
            for spot in assigned_spots:
                spot.user_id = None
                spot.status = 'available'
                
                # Update available slots
                lot = ParkingLot.query.get(spot.lot_id)
                if lot:
                    lot.available_slots += 1
            
            # 3. Delete ALL reservations (both active and historical) for this user
            # This is necessary to avoid foreign key constraint violations
            all_reservations = ReserveSpot.query.filter_by(user_id=user_id).all()
            for reservation in all_reservations:
                db.session.delete(reservation)
            
            # 4. Now safe to delete the user
            db.session.delete(user)
            db.session.commit()
            
            # Invalidate caches
            cache_delete(f'user:{user_id}')
            cache_delete('users:all')
            cache_delete('parking_lots:all')  # Since we may have updated availability
            increment_counter('users_deleted')
            
            return {'msg': 'User deleted successfully. Any active reservations have been completed, parking spots released, and reservation history removed.'}, 200
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"Error deleting user {user_id}: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return {'msg': 'Error deleting user', 'error': str(e), 'details': traceback.format_exc()}, 500


class ParkingLotResource(Resource):
    
    def get(self, lot_id=None):
        # Increment API usage counter
        increment_counter('api_calls:parking_lots:get')
        
        if lot_id:
            # Try to get parking lot from cache first
            cache_key = f'parking_lot:{lot_id}'
            cached_lot = cache_get(cache_key)
            if cached_lot:
                return cached_lot, 200
                
            lot = ParkingLot.query.get(lot_id)
            if lot:
                lot_data = {
                    'msg': 'Parking lot found',
                    'lot': {
                        'id': lot.id,
                        'location_name': lot.location_name,
                        'price': lot.price,
                        'address': lot.address,
                        'pincode': lot.pincode,
                        'number_of_slots': lot.number_of_slots,
                        'available_slots': lot.available_slots
                    }
                }
                # Cache parking lot data for 10 seconds only to prevent stale data
                cache_set(cache_key, lot_data, 10)
                return lot_data, 200
            return {'msg': 'Parking lot not found'}, 404
        
        # Try to get all parking lots from cache
        cache_key = 'parking_lots:all'
        cached_lots = cache_get(cache_key)
        if cached_lots:
            return cached_lots, 200
        
        lots = ParkingLot.query.all()
        lot_list = []
        for lot in lots:
            lot_list.append({
                'id': lot.id,
                'location_name': lot.location_name,
                'price': lot.price,
                'address': lot.address,
                'pincode': lot.pincode,
                'number_of_slots': lot.number_of_slots,
                'available_slots': lot.available_slots
            })
        
        response_data = {'msg': 'Parking lots retrieved successfully', 'lots': lot_list}
        # Cache parking lots for 10 seconds only (they change frequently)
        cache_set(cache_key, response_data, 10)
        return response_data, 200
    
    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Only admin can create parking lots
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
        
        data = request.get_json()
        location_name = data.get('location_name')
        price = data.get('price')
        address = data.get('address')
        pincode = data.get('pincode')
        number_of_slots = data.get('number_of_slots')
        
        if not all([location_name, price, address, pincode, number_of_slots]):
            return {'msg': 'Please provide all required fields'}, 400
        
        try:
            lot = ParkingLot(
                location_name=location_name,
                price=float(price),
                address=address,
                pincode=pincode,
                number_of_slots=int(number_of_slots),
                available_slots=int(number_of_slots)
            )
            
            db.session.add(lot)
            db.session.commit()
            
            # Create parking spots for this lot
            for i in range(int(number_of_slots)):
                spot = ParkingSpot(
                    lot_id=lot.id,
                    status='available'
                )
                db.session.add(spot)
            
            db.session.commit()
            
            # Invalidate parking lots cache when new lot is created
            cache_delete('parking_lots:all')
            increment_counter('parking_lots_created')
            
            return {
                'msg': 'Parking lot created successfully',
                'lot': {
                    'id': lot.id,
                    'location_name': lot.location_name,
                    'price': lot.price,
                    'address': lot.address,
                    'pincode': lot.pincode,
                    'number_of_slots': lot.number_of_slots,
                    'available_slots': lot.available_slots
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error creating parking lot', 'error': str(e)}, 500
    
    @jwt_required()
    def put(self, lot_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Only admin can update parking lots
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': 'Parking lot not found'}, 404
        
        data = request.get_json()
        if 'location_name' in data:
            lot.location_name = data['location_name']
        if 'price' in data:
            lot.price = float(data['price'])
        if 'address' in data:
            lot.address = data['address']
        if 'pincode' in data:
            lot.pincode = data['pincode']
        if 'number_of_slots' in data:
            lot.number_of_slots = int(data['number_of_slots'])
        if 'available_slots' in data:
            lot.available_slots = int(data['available_slots'])
        
        try:
            db.session.commit()
            
            # Invalidate parking lot cache when updated
            cache_delete(f'parking_lot:{lot_id}')
            cache_delete('parking_lots:all')
            
            return {
                'msg': 'Parking lot updated successfully',
                'lot': {
                    'id': lot.id,
                    'location_name': lot.location_name,
                    'price': lot.price,
                    'address': lot.address,
                    'pincode': lot.pincode,
                    'number_of_slots': lot.number_of_slots,
                    'available_slots': lot.available_slots
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error updating parking lot', 'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, lot_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Only admin can delete parking lots
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': 'Parking lot not found'}, 404
        
        try:
            # Delete all spots in this lot first
            ParkingSpot.query.filter_by(lot_id=lot_id).delete()
            db.session.delete(lot)
            db.session.commit()
            
            # Invalidate parking lot cache when deleted
            cache_delete(f'parking_lot:{lot_id}')
            cache_delete('parking_lots:all')
            increment_counter('parking_lots_deleted')
            
            return {'msg': 'Parking lot deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error deleting parking lot', 'error': str(e)}, 500


class ParkingSpotResource(Resource):
    
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if spot:
                return {
                    'msg': 'Parking spot found',
                    'spot': {
                        'id': spot.id,
                        'lot_id': spot.lot_id,
                        'user_id': spot.user_id,
                        'status': spot.status
                    }
                }, 200
            return {'msg': 'Parking spot not found'}, 404
        
        spots = ParkingSpot.query.all()
        spot_list = []
        for spot in spots:
            spot_list.append({
                'id': spot.id,
                'lot_id': spot.lot_id,
                'user_id': spot.user_id,
                'status': spot.status
            })
        return {'msg': 'Parking spots retrieved successfully', 'spots': spot_list}, 200
    
    def put(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': 'Parking spot not found'}, 404
        
        data = request.get_json()
        if 'user_id' in data:
            spot.user_id = data['user_id']
        if 'status' in data:
            spot.status = data['status']
        
        try:
            db.session.commit()
            return {
                'msg': 'Parking spot updated successfully',
                'spot': {
                    'id': spot.id,
                    'lot_id': spot.lot_id,
                    'user_id': spot.user_id,
                    'status': spot.status
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error updating parking spot', 'error': str(e)}, 500


class AvailableSpotsResource(Resource):
    
    def get(self, lot_id):
        """Get available spots for a specific parking lot"""
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': 'Parking lot not found'}, 404
        
        available_spots = ParkingSpot.query.filter_by(
            lot_id=lot_id,
            status='available'
        ).all()
        
        spot_list = []
        for spot in available_spots:
            spot_list.append({
                'id': spot.id,
                'lot_id': spot.lot_id,
                'status': spot.status
            })
        
        return {
            'msg': 'Available spots retrieved successfully',
            'lot_name': lot.location_name,
            'available_spots': spot_list,
            'count': len(spot_list)
        }, 200


class ReserveSpotResource(Resource):
    
    def get(self, reservation_id=None):
        if reservation_id:
            reservation = ReserveSpot.query.get(reservation_id)
            if reservation:
                return {
                    'msg': 'Reservation found',
                    'reservation': {
                        'id': reservation.id,
                        'spot_id': reservation.spot_id,
                        'user_id': reservation.user_id,
                        'parking_time': reservation.parking_time.isoformat(),
                        'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else None,
                        'parking_cost': reservation.parking_cost
                    }
                }, 200
            return {'msg': 'Reservation not found'}, 404
        
        reservations = ReserveSpot.query.all()
        reservation_list = []
        for reservation in reservations:
            reservation_list.append({
                'id': reservation.id,
                'spot_id': reservation.spot_id,
                'user_id': reservation.user_id,
                'parking_time': reservation.parking_time.isoformat(),
                'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else None,
                'parking_cost': reservation.parking_cost
            })
        return {'msg': 'Reservations retrieved successfully', 'reservations': reservation_list}, 200
    
    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        data = request.get_json()
        spot_id = data.get('spot_id')
        user_id = data.get('user_id', current_user_id)  # Use current user if not specified
        parking_time = data.get('parking_time')
        leaving_time = data.get('leaving_time')
        
        # Users can only make reservations for themselves (unless admin)
        if current_user.role != 'admin' and current_user_id != user_id:
            return {'msg': 'Access denied. You can only make reservations for yourself.'}, 403
        
        if not all([spot_id, parking_time, leaving_time]):
            return {'msg': 'Please provide all required fields'}, 400
        
        # Check if spot exists and is available
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {'msg': 'Parking spot not found'}, 404
        
        if spot.status != 'available':
            return {'msg': 'Parking spot is not available'}, 400
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        
        # Get parking lot to calculate cost
        lot = ParkingLot.query.get(spot.lot_id)
        if not lot:
            return {'msg': 'Parking lot not found'}, 404
        
        try:
            # Parse datetime strings
            parking_dt = datetime.fromisoformat(parking_time)
            leaving_dt = datetime.fromisoformat(leaving_time)
            
            # Calculate parking cost (hours * hourly rate)
            duration_hours = (leaving_dt - parking_dt).total_seconds() / 3600
            parking_cost = duration_hours * lot.price
            
            # Create reservation
            reservation = ReserveSpot(
                spot_id=spot_id,
                user_id=user_id,
                parking_time=parking_dt,
                leaving_time=leaving_dt,
                parking_cost=parking_cost
            )
            
            # Update spot status
            spot.status = 'reserved'
            spot.user_id = user_id
            
            # Update available slots in lot
            lot.available_slots -= 1
            
            db.session.add(reservation)
            db.session.commit()
            
            # Invalidate parking lots cache since availability changed
            cache_delete('parking_lots:all')
            cache_delete(f'parking_lot:{lot.id}')
            
            # Increment reservation counter
            increment_counter('total_reservations')
            increment_counter(f'daily_reservations:{datetime.now().strftime("%Y-%m-%d")}')
            
            return {
                'msg': 'Reservation created successfully',
                'reservation': {
                    'id': reservation.id,
                    'spot_id': reservation.spot_id,
                    'user_id': reservation.user_id,
                    'parking_time': reservation.parking_time.isoformat(),
                    'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else None,
                    'parking_cost': reservation.parking_cost
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error creating reservation', 'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, reservation_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        reservation = ReserveSpot.query.get(reservation_id)
        if not reservation:
            return {'msg': 'Reservation not found'}, 404
        
        # Users can only cancel their own reservations (unless admin)
        if current_user.role != 'admin' and current_user_id != reservation.user_id:
            return {'msg': 'Access denied. You can only cancel your own reservations.'}, 403
        
        try:
            # Get the spot and update its status
            spot = ParkingSpot.query.get(reservation.spot_id)
            if spot:
                spot.status = 'available'
                spot.user_id = None
                
                # Update available slots in lot
                lot = ParkingLot.query.get(spot.lot_id)
                if lot:
                    lot.available_slots += 1
            
            db.session.delete(reservation)
            db.session.commit()
            
            # Invalidate parking lots cache since availability changed
            if spot:
                cache_delete('parking_lots:all')
                cache_delete(f'parking_lot:{spot.lot_id}')
            
            # Increment cancellation counter
            increment_counter('reservations_cancelled')
            
            return {'msg': 'Reservation cancelled successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error cancelling reservation', 'error': str(e)}, 500


class UserReservationsResource(Resource):
    
    @jwt_required()
    def get(self, user_id):
        """Get all reservations for a specific user"""
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Convert user_id to int if it's a string
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return {'msg': 'Invalid user ID format'}, 400
        
        # Users can only view their own reservations (unless admin)
        if current_user.role != 'admin' and current_user_id != user_id:
            return {'msg': 'Access denied. You can only view your own reservations.'}, 403
        
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        
        try:
            reservations = ReserveSpot.query.filter_by(user_id=user_id).all()
            # print(f"Found {len(reservations)} reservations")
        except Exception as e:
            return {'msg': 'Database error occurred', 'error': str(e)}, 500
        
        reservation_list = []
        for reservation in reservations:
            try:
                # Get spot and lot information
                spot = ParkingSpot.query.get(reservation.spot_id)
                lot = ParkingLot.query.get(spot.lot_id) if spot else None
                
                reservation_list.append({
                    'id': reservation.id,
                    'spot_id': reservation.spot_id,
                    'lot_name': lot.location_name if lot else 'Unknown',
                    'lot_address': lot.address if lot else 'Unknown',
                    'lot_price': lot.price if lot else 10,  # Include hourly rate
                    'parking_time': reservation.parking_time.isoformat(),
                    'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else None,
                    'parking_cost': reservation.parking_cost,
                    'transaction_id': reservation.transaction_id,
                    'payment_method': reservation.payment_method
                })
            except Exception as e:
                continue  # Skip this reservation but continue with others
        
        result = {
            'msg': 'User reservations retrieved successfully',
            'user': user.username,
            'reservations': reservation_list
        }
        return result, 200


class LoginResource(Resource):
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'msg': 'Please provide email and password'}, 400
        
        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:
            return {'msg': 'Invalid credentials'}, 401
        
        # Create JWT token with string identity
        access_token = create_access_token(identity=str(user.id))
        
        # Cache user session data for 12 hours
        session_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'vehicle_number': user.vehicle_number,
            'login_time': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        cache_set(f'user_session:{user.id}', session_data, 43200)  # 12 hours
        
        # Add user to active users set
        add_to_set('active_users', user.id, 43200)
        
        # Increment login counter
        increment_counter('total_logins')
        increment_counter(f'daily_logins:{datetime.now().strftime("%Y-%m-%d")}')
        
        return {
            'msg': 'Login successful',
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'vehicle_number': user.vehicle_number
            }
        }, 200


class RegisterResource(Resource):
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        vehicle_number = data.get('vehicle_number')
        phone_number = data.get('phone_number')
        
        if not email or not username or not password:
            return {'msg': 'Please provide email, username, and password'}, 400
        
        # Normalize email to lowercase for consistent checking
        email = email.lower().strip()
        username = username.strip()
        
        try:
            # Check if user already exists (case-insensitive email check)
            existing_user = User.query.filter(User.email.ilike(email)).first()
            if existing_user:
                return {'msg': f'User with email {email} already exists'}, 409
            
            # Check if username already exists (case-insensitive)
            existing_username = User.query.filter(User.username.ilike(username)).first()
            if existing_username:
                return {'msg': f'Username {username} already exists'}, 409
            
            # Check if vehicle number already exists (only if provided)
            if vehicle_number and vehicle_number.strip():
                vehicle_number = vehicle_number.strip()
                existing_vehicle = User.query.filter_by(vehicle_number=vehicle_number).first()
                if existing_vehicle:
                    return {'msg': 'Vehicle number already exists'}, 409
            
            # Check if phone number already exists (only if provided)
            if phone_number and phone_number.strip():
                phone_number = phone_number.strip()
                existing_phone = User.query.filter_by(phone_number=phone_number).first()
                if existing_phone:
                    return {'msg': 'Phone number already exists'}, 409
        except Exception as e:
            print(f"Error during user validation: {str(e)}")
            return {'msg': 'Database error during validation'}, 500
        
        # Create new user
        user = User(
            email=email,
            username=username,
            password=password,
            role=role,
            vehicle_number=vehicle_number if vehicle_number else None,
            phone_number=phone_number if phone_number else None
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Create JWT token for immediate login with string identity
            access_token = create_access_token(identity=str(user.id))
            
            # Cache user session data for 12 hours (auto-login after registration)
            session_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'vehicle_number': user.vehicle_number,
                'login_time': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
            cache_set(f'user_session:{user.id}', session_data, 43200)  # 12 hours
            
            # Add user to active users set
            add_to_set('active_users', user.id, 43200)
            
            # Increment registration counter
            increment_counter('total_registrations')
            increment_counter(f'daily_registrations:{datetime.now().strftime("%Y-%m-%d")}')
            
            # Invalidate users cache
            cache_delete('users:all')
            
            # Send welcome email
            # Email functionality not implemented yet
            
            return {
                'msg': 'User registered successfully',
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'vehicle_number': user.vehicle_number,
                    'phone_number': user.phone_number
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Registration failed. Please try again.'}, 500


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """Handle user logout and clear Redis session"""
        current_user_id = int(get_jwt_identity())
        
        # Clear user session from Redis
        cache_delete(f'user_session:{current_user_id}')
        
        # Remove user from active users set
        redis_client = get_redis_client()
        if redis_client:
            try:
                redis_client.srem('active_users', current_user_id)
            except Exception as e:
                print(f"Redis set removal error: {e}")
        
        # Increment logout counter
        increment_counter('total_logouts')
        
        return {'msg': 'Logged out successfully'}, 200


class BookingResource(Resource):
    
    @jwt_required()
    def post(self, action):
        """Handle parking spot booking operations"""
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return {'msg': 'User not found'}, 404
        
        data = request.get_json()
        
        if action == 'book-spot':
            return self._book_spot(current_user, data)
        elif action == 'occupy-spot':
            return self._occupy_spot(current_user, data)
        elif action == 'release-spot':
            return self._release_spot(current_user, data)
        else:
            return {'msg': 'Invalid action'}, 400
    
    def _book_spot(self, user, data):
        """Book a parking spot automatically"""
        lot_id = data.get('lot_id')
        
        if not lot_id:
            return {'msg': 'Parking lot ID is required'}, 400
        
        # Check if lot exists
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {'msg': 'Parking lot not found'}, 404
        
        # Check if user already has an active reservation (one with no leaving_time or future leaving_time)
        active_reservation = ReserveSpot.query.filter_by(user_id=user.id).filter(
            (ReserveSpot.leaving_time.is_(None)) | (ReserveSpot.leaving_time > datetime.now())
        ).first()
        
        if active_reservation:
            return {'msg': 'You already have an active parking reservation'}, 400
        
        # Find first available spot
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id,
            status='available'
        ).first()
        
        if not available_spot:
            return {'msg': 'No available parking spots in this lot'}, 400
        
        try:
            # Create reservation with current time as parking time
            now = datetime.now()
            # Set leaving_time to None (unlimited until manual release)
            leaving_time = None
            
            # Initial cost is 0, will be calculated when user releases the spot
            parking_cost = 0.0
            
            # Create reservation
            reservation = ReserveSpot(
                spot_id=available_spot.id,
                user_id=user.id,
                parking_time=now,
                leaving_time=leaving_time,
                parking_cost=parking_cost
            )
            
            # Update spot status to occupied (user immediately starts parking)
            available_spot.status = 'occupied'
            available_spot.user_id = user.id
            
            # Update available slots
            lot.available_slots -= 1
            
            db.session.add(reservation)
            db.session.commit()
            
            # Invalidate parking lots cache since availability changed
            cache_delete('parking_lots:all')
            cache_delete(f'parking_lot:{lot.id}')
            
            # Increment reservation counter
            increment_counter('total_reservations')
            increment_counter(f'daily_reservations:{datetime.now().strftime("%Y-%m-%d")}')
            
            # Send booking confirmation email synchronously (for immediate delivery)
            try:
                from tasks import send_booking_confirmation_email
                # Call directly instead of using .delay() for immediate email sending
                result = send_booking_confirmation_email(reservation.id)
                print(f"✅ Booking confirmation email sent: {result}")
            except Exception as email_error:
                print(f"⚠️ Failed to send booking confirmation email: {email_error}")
            
            return {
                'msg': 'Parking spot booked successfully',
                'reservation': {
                    'id': reservation.id,
                    'spot_id': reservation.spot_id,
                    'lot_name': lot.location_name,
                    'parking_time': reservation.parking_time.isoformat(),
                    'leaving_time': None,
                    'parking_cost': reservation.parking_cost,
                    'status': 'active'
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            print(f"Booking error: {str(e)}")  # Add debug logging
            return {'msg': 'Error booking parking spot', 'error': str(e)}, 500
    
    def _occupy_spot(self, user, data):
        """Mark parking spot as occupied when user parks"""
        reservation_id = data.get('reservation_id')
        
        if not reservation_id:
            return {'msg': 'Reservation ID is required'}, 400
        
        reservation = ReserveSpot.query.get(reservation_id)
        if not reservation:
            return {'msg': 'Reservation not found'}, 404
        
        if reservation.user_id != user.id:
            return {'msg': 'Access denied - not your reservation'}, 403
        
        try:
            # Get the parking spot
            spot = ParkingSpot.query.get(reservation.spot_id)
            if spot:
                spot.status = 'occupied'
                
                # Update parking time to current time (actual parking time)
                reservation.parking_time = datetime.now()
                
                db.session.commit()
                
                return {
                    'msg': 'Parking spot marked as occupied',
                    'reservation': {
                        'id': reservation.id,
                        'spot_id': reservation.spot_id,
                        'parking_time': reservation.parking_time.isoformat(),
                        'status': 'occupied'
                    }
                }, 200
            else:
                return {'msg': 'Parking spot not found'}, 404
                
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error updating parking spot', 'error': str(e)}, 500
    
    def _release_spot(self, user, data):
        """Release parking spot when user leaves"""
        reservation_id = data.get('reservation_id')
        transaction_id = data.get('transaction_id')  # Get transaction ID from payment
        payment_method = data.get('payment_method')  # Get payment method
        
        if not reservation_id:
            return {'msg': 'Reservation ID is required'}, 400
        
        reservation = ReserveSpot.query.get(reservation_id)
        if not reservation:
            return {'msg': 'Reservation not found'}, 404
        
        if reservation.user_id != user.id:
            return {'msg': 'Access denied - not your reservation'}, 403
        
        try:
            # Get the parking spot and lot
            spot = ParkingSpot.query.get(reservation.spot_id)
            lot = ParkingLot.query.get(spot.lot_id) if spot else None
            
            if spot and lot:
                # Update leaving time to current time (actual leaving time)
                now = datetime.now()
                reservation.leaving_time = now
                
                # Calculate duration in hours
                duration_seconds = (now - reservation.parking_time).total_seconds()
                duration_hours = duration_seconds / 3600
                
                # Calculate cost based on full hourly rates:
                if duration_hours <= 1:
                    # Any parking up to 1 hour is charged as 1 full hour
                    charged_hours = 1
                else:
                    # More than 1 hour: round up to next full hour
                    import math
                    charged_hours = math.ceil(duration_hours)
                
                # Calculate final cost
                reservation.parking_cost = float(charged_hours * lot.price)
                
                # Store transaction details
                if transaction_id:
                    reservation.transaction_id = transaction_id
                if payment_method:
                    # Map frontend payment method to standardized values
                    method_mapping = {
                        'qr': 'UPI',
                        'card': 'Card',
                        'upi': 'UPI',
                        'cash': 'Cash'
                    }
                    reservation.payment_method = method_mapping.get(payment_method, payment_method)
                
                # Release the spot
                spot.status = 'available'
                spot.user_id = None
                
                # Update available slots
                lot.available_slots += 1
                
                db.session.commit()
                
                # Invalidate parking lots cache since availability changed
                cache_delete('parking_lots:all')
                cache_delete(f'parking_lot:{lot.id}')
                
                # Send parking release receipt email synchronously (for immediate delivery)
                try:
                    from tasks import send_parking_release_email
                    # Call directly instead of using .delay() for immediate email sending
                    result = send_parking_release_email(reservation.id)
                    print(f"✅ Parking release email sent: {result}")
                except Exception as email_error:
                    print(f"⚠️ Failed to send parking release email: {email_error}")
                
                return {
                    'msg': 'Parking spot released successfully',
                    'reservation': {
                        'id': reservation.id,
                        'spot_id': reservation.spot_id,
                        'parking_time': reservation.parking_time.isoformat(),
                        'leaving_time': reservation.leaving_time.isoformat(),
                        'actual_duration_hours': round(duration_hours, 2),
                        'charged_hours': charged_hours,
                        'parking_cost': round(reservation.parking_cost, 2),
                        'hourly_rate': lot.price,
                        'transaction_id': reservation.transaction_id,
                        'payment_method': reservation.payment_method,
                        'status': 'completed'
                    }
                }, 200
            else:
                return {'msg': 'Parking spot or lot not found'}, 404
                
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error releasing parking spot', 'error': str(e)}, 500


class ReportsResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Only admin can access reports
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
        
        try:
            # Get parking lot statistics
            lots = ParkingLot.query.all()
            lot_stats = []
            
            for lot in lots:
                total_spots = lot.number_of_slots
                occupied_spots = total_spots - lot.available_slots
                
                # Get reservations for this lot
                lot_reservations = db.session.query(ReserveSpot).join(ParkingSpot).filter(
                    ParkingSpot.lot_id == lot.id
                ).count()
                
                # Calculate revenue for this lot
                lot_revenue = db.session.query(db.func.sum(ReserveSpot.parking_cost)).join(ParkingSpot).filter(
                    ParkingSpot.lot_id == lot.id,
                    ReserveSpot.leaving_time.isnot(None)  # Only completed reservations
                ).scalar() or 0
                
                lot_stats.append({
                    'id': lot.id,
                    'location_name': lot.location_name,
                    'total_spots': total_spots,
                    'occupied_spots': occupied_spots,
                    'available_spots': lot.available_slots,
                    'occupancy_rate': round((occupied_spots / total_spots) * 100, 2) if total_spots > 0 else 0,
                    'total_reservations': lot_reservations,
                    'total_revenue': round(float(lot_revenue), 2)
                })
            
            # Get user statistics
            total_users = User.query.count()
            admin_users = User.query.filter_by(role='admin').count()
            regular_users = User.query.filter_by(role='user').count()
            
            # Get reservation statistics
            total_reservations = ReserveSpot.query.count()
            active_reservations = ReserveSpot.query.filter_by(leaving_time=None).count()
            completed_reservations = ReserveSpot.query.filter(ReserveSpot.leaving_time.isnot(None)).count()
            
            # Calculate total revenue
            total_revenue = db.session.query(db.func.sum(ReserveSpot.parking_cost)).filter(
                ReserveSpot.leaving_time.isnot(None)
            ).scalar() or 0
            
            # Get monthly reservation trends (last 12 months)
            monthly_trends = []
            for i in range(12):
                month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
                month_end = month_start + timedelta(days=30)
                
                month_reservations = ReserveSpot.query.filter(
                    ReserveSpot.parking_time >= month_start,
                    ReserveSpot.parking_time < month_end
                ).count()
                
                monthly_trends.append({
                    'month': month_start.strftime('%B %Y'),
                    'reservations': month_reservations
                })
            
            monthly_trends.reverse()  # Show oldest to newest
            
            # Daily revenue trends (last 30 days)
            daily_revenue = []
            for i in range(30):
                day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
                day_end = day_start + timedelta(days=1)
                
                day_revenue = db.session.query(db.func.sum(ReserveSpot.parking_cost)).filter(
                    ReserveSpot.parking_time >= day_start,
                    ReserveSpot.parking_time < day_end,
                    ReserveSpot.leaving_time.isnot(None)
                ).scalar() or 0
                
                daily_revenue.append({
                    'date': day_start.strftime('%Y-%m-%d'),
                    'revenue': round(float(day_revenue), 2)
                })
            
            daily_revenue.reverse()  # Show oldest to newest
            
            # Monthly revenue trends (last 12 months)
            monthly_revenue = []
            for i in range(12):
                month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
                month_end = month_start + timedelta(days=30)
                
                month_revenue_amount = db.session.query(db.func.sum(ReserveSpot.parking_cost)).filter(
                    ReserveSpot.parking_time >= month_start,
                    ReserveSpot.parking_time < month_end,
                    ReserveSpot.leaving_time.isnot(None)
                ).scalar() or 0
                
                monthly_revenue.append({
                    'month': month_start.strftime('%B %Y'),
                    'revenue': round(float(month_revenue_amount), 2)
                })
            
            monthly_revenue.reverse()  # Show oldest to newest
            
            # Payment method distribution
            payment_methods = db.session.query(
                ReserveSpot.payment_method,
                db.func.count(ReserveSpot.payment_method)
            ).filter(
                ReserveSpot.payment_method.isnot(None)
            ).group_by(ReserveSpot.payment_method).all()
            
            payment_distribution = [
                {'method': method, 'count': count} for method, count in payment_methods
            ]
            
            # Get Redis analytics
            redis_stats = {}
            redis_client = get_redis_client()
            if redis_client:
                try:
                    redis_stats = {
                        'total_api_calls': int(redis_client.get('api_calls:users:get') or 0) + int(redis_client.get('api_calls:parking_lots:get') or 0),
                        'total_logins': int(redis_client.get('total_logins') or 0),
                        'total_logouts': int(redis_client.get('total_logouts') or 0),
                        'total_registrations': int(redis_client.get('total_registrations') or 0),
                        'active_users_count': redis_client.scard('active_users'),
                        'users_created': int(redis_client.get('users_created') or 0),
                        'users_deleted': int(redis_client.get('users_deleted') or 0),
                        'parking_lots_created': int(redis_client.get('parking_lots_created') or 0),
                        'parking_lots_deleted': int(redis_client.get('parking_lots_deleted') or 0),
                        'reservations_cancelled': int(redis_client.get('reservations_cancelled') or 0),
                        'today_logins': int(redis_client.get(f'daily_logins:{datetime.now().strftime("%Y-%m-%d")}') or 0),
                        'today_registrations': int(redis_client.get(f'daily_registrations:{datetime.now().strftime("%Y-%m-%d")}') or 0),
                        'today_reservations': int(redis_client.get(f'daily_reservations:{datetime.now().strftime("%Y-%m-%d")}') or 0)
                    }
                except Exception as e:
                    print(f"Error getting Redis stats: {e}")
                    redis_stats = {'error': 'Unable to fetch Redis statistics'}
            else:
                redis_stats = {'error': 'Redis not available'}
            
            return {
                'msg': 'Reports data retrieved successfully',
                'data': {
                    'parking_lots': lot_stats,
                    'user_stats': {
                        'total_users': total_users,
                        'admin_users': admin_users,
                        'regular_users': regular_users
                    },
                    'reservation_stats': {
                        'total_reservations': total_reservations,
                        'active_reservations': active_reservations,
                        'completed_reservations': completed_reservations,
                        'total_revenue': round(float(total_revenue), 2)
                    },
                    'monthly_trends': monthly_trends,
                    'daily_revenue': daily_revenue,
                    'monthly_revenue': monthly_revenue,
                    'payment_distribution': payment_distribution,
                    'overall_occupancy': {
                        'total_spots': sum(lot['total_spots'] for lot in lot_stats),
                        'occupied_spots': sum(lot['occupied_spots'] for lot in lot_stats),
                        'available_spots': sum(lot['available_spots'] for lot in lot_stats)
                    },
                    'redis_analytics': redis_stats
                }
            }, 200
            
        except Exception as e:
            return {'msg': 'Error retrieving reports data', 'error': str(e)}, 500


class UserReportsResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Users can only access their own reports
        if not current_user:
            return {'msg': 'User not found'}, 404
        
        try:
            # Get user's reservation statistics
            user_reservations = ReserveSpot.query.filter_by(user_id=current_user_id).all()
            
            if not user_reservations:
                # Return empty data structure if no reservations
                return {
                    'status': 'success',
                    'msg': 'User reports data retrieved successfully',
                    'data': {
                        'stats': {
                            'totalSpent': 0,
                            'totalBookings': 0,
                            'activeBookings': 0,
                            'totalHours': 0,
                            'avgHoursPerBooking': 0,
                            'favoriteLocation': 'N/A',
                            'favoriteLocationCount': 0
                        },
                        'monthlySpending': [],
                        'bookingFrequency': [],
                        'favoriteLocations': [],
                        'dailyUsage': [],
                        'hourlyUsage': [],
                        'durationAnalysis': []
                    }
                }, 200
            
            # Calculate user statistics
            total_spent = sum(float(res.parking_cost or 0) for res in user_reservations if res.leaving_time)
            total_bookings = len(user_reservations)
            active_bookings = len([res for res in user_reservations if not res.leaving_time])
            
            # Calculate total hours
            total_hours = 0
            for res in user_reservations:
                if res.leaving_time and res.parking_time:  # Use parking_time instead of arrival_time
                    duration = res.leaving_time - res.parking_time
                    total_hours += duration.total_seconds() / 3600
            
            avg_hours_per_booking = total_hours / total_bookings if total_bookings > 0 else 0
            
            # Find favorite location
            location_counts = {}
            for res in user_reservations:
                try:
                    # Get the parking spot and lot information
                    spot = ParkingSpot.query.get(res.spot_id)
                    if spot:
                        lot = ParkingLot.query.get(spot.lot_id)
                        if lot:
                            loc_name = lot.location_name
                            location_counts[loc_name] = location_counts.get(loc_name, 0) + 1
                except Exception as e:
                    continue
            
            favorite_location = max(location_counts.items(), key=lambda x: x[1]) if location_counts else ('N/A', 0)
            
            # Monthly spending analysis (last 12 months)
            monthly_spending = []
            monthly_bookings = []
            current_date = datetime.now()
            
            for i in range(12):
                month_start = current_date.replace(day=1) - timedelta(days=i*30)
                month_name = calendar.month_abbr[month_start.month]
                
                month_reservations = [res for res in user_reservations 
                                    if res.parking_time and res.parking_time.month == month_start.month 
                                    and res.parking_time.year == month_start.year]  # Use parking_time
                
                month_total = sum(float(res.parking_cost or 0) for res in month_reservations if res.leaving_time)
                month_count = len(month_reservations)
                
                monthly_spending.insert(0, {'month': month_name, 'amount': round(month_total, 2)})
                monthly_bookings.insert(0, {'month': month_name, 'bookings': month_count})
            
            # Location analysis
            favorite_locations_data = []
            for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                favorite_locations_data.append({'name': location, 'count': count})
            
            # Daily usage pattern
            daily_usage = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 
                          'Friday': 0, 'Saturday': 0, 'Sunday': 0}
            
            for res in user_reservations:
                if res.parking_time:  # Use parking_time instead of arrival_time
                    day_name = res.parking_time.strftime('%A')
                    daily_usage[day_name] += 1
            
            daily_usage_data = [{'day': day, 'sessions': count} for day, count in daily_usage.items()]
            
            # Hourly usage pattern
            hourly_usage = {}
            for hour in range(24):
                hourly_usage[hour] = 0
            
            for res in user_reservations:
                if res.parking_time:  # Use parking_time instead of arrival_time
                    hour = res.parking_time.hour
                    hourly_usage[hour] += 1
            
            hourly_usage_data = []
            for hour in range(6, 24):  # 6 AM to 11 PM
                hour_label = f"{hour % 12 if hour % 12 != 0 else 12} {'AM' if hour < 12 else 'PM'}"
                hourly_usage_data.append({'hour': hour_label, 'sessions': hourly_usage[hour]})
            
            # Duration analysis
            duration_ranges = {
                '< 1 hour': 0, '1-2 hours': 0, '2-4 hours': 0,
                '4-6 hours': 0, '6-8 hours': 0, '> 8 hours': 0
            }
            
            for res in user_reservations:
                if res.leaving_time and res.parking_time:  # Use parking_time instead of arrival_time
                    duration = (res.leaving_time - res.parking_time).total_seconds() / 3600
                    if duration < 1:
                        duration_ranges['< 1 hour'] += 1
                    elif duration < 2:
                        duration_ranges['1-2 hours'] += 1
                    elif duration < 4:
                        duration_ranges['2-4 hours'] += 1
                    elif duration < 6:
                        duration_ranges['4-6 hours'] += 1
                    elif duration < 8:
                        duration_ranges['6-8 hours'] += 1
                    else:
                        duration_ranges['> 8 hours'] += 1
            
            duration_analysis_data = [{'duration': duration, 'count': count} 
                                    for duration, count in duration_ranges.items()]
            
            return {
                'status': 'success',
                'msg': 'User reports data retrieved successfully',
                'data': {
                    'stats': {
                        'totalSpent': round(total_spent, 2),
                        'totalBookings': total_bookings,
                        'activeBookings': active_bookings,
                        'totalHours': round(total_hours, 1),
                        'avgHoursPerBooking': round(avg_hours_per_booking, 1),
                        'favoriteLocation': favorite_location[0],
                        'favoriteLocationCount': favorite_location[1]
                    },
                    'monthlySpending': monthly_spending,
                    'bookingFrequency': monthly_bookings,
                    'favoriteLocations': favorite_locations_data,
                    'dailyUsage': daily_usage_data,
                    'hourlyUsage': hourly_usage_data,
                    'durationAnalysis': duration_analysis_data
                }
            }, 200
            
        except Exception as e:
            return {'msg': 'Error retrieving user reports data', 'error': str(e)}, 500


class UserBookingHistoryResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        # Users can only access their own booking history
        if not current_user:
            return {'msg': 'User not found'}, 404
        
        try:
            # Get user's reservation history
            user_reservations = ReserveSpot.query.filter_by(user_id=current_user_id).order_by(ReserveSpot.parking_time.desc()).all()
            
            booking_history = []
            for res in user_reservations:
                try:
                    # Get the parking spot and lot information
                    spot = ParkingSpot.query.get(res.spot_id)
                    lot = None
                    if spot:
                        lot = ParkingLot.query.get(spot.lot_id)
                    
                    # Calculate duration if available
                    duration_hours = None
                    if res.leaving_time and res.parking_time:
                        duration = res.leaving_time - res.parking_time
                        duration_hours = round(duration.total_seconds() / 3600, 2)
                    
                    booking_data = {
                        'id': res.id,
                        'start_time': res.parking_time.isoformat() if res.parking_time else None,
                        'end_time': res.leaving_time.isoformat() if res.leaving_time else None,
                        'duration_hours': duration_hours,
                        'total_amount': float(res.parking_cost) if res.parking_cost else 0,
                        'status': 'Completed' if res.leaving_time else 'Active',
                        'vehicle_number': current_user.vehicle_number,
                        'parking_space': {
                            'id': spot.id if spot else None,
                            'name': f"{lot.location_name} - Spot {spot.id}" if lot and spot else 'Unknown Location'
                        } if spot else {'id': None, 'name': 'Unknown Location'}
                    }
                    
                    booking_history.append(booking_data)
                    
                except Exception as e:
                    # Add basic reservation info even if there's an error with details
                    booking_history.append({
                        'id': res.id,
                        'start_time': res.parking_time.isoformat() if res.parking_time else None,
                        'end_time': res.leaving_time.isoformat() if res.leaving_time else None,
                        'duration_hours': None,
                        'total_amount': float(res.parking_cost) if res.parking_cost else 0,
                        'status': 'Completed' if res.leaving_time else 'Active',
                        'vehicle_number': current_user.vehicle_number,
                        'parking_space': {'id': None, 'name': 'Unknown Location'}
                    })
            
            return {
                'status': 'success',
                'msg': 'Booking history retrieved successfully',
                'data': booking_history
            }, 200
            
        except Exception as e:
            return {'msg': 'Error retrieving booking history', 'error': str(e)}, 500


class TasksResource(Resource):
    @jwt_required()
    def post(self, task_type):
        """Trigger Celery tasks"""
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return {'msg': 'User not found'}, 404
        
        try:
            if task_type == 'export-csv':
                # User triggered CSV export
                from tasks import export_user_data_csv
                task = export_user_data_csv.delay(current_user_id)
                
                return {
                    'msg': 'CSV export started successfully',
                    'task_id': task.id,
                    'status': 'processing',
                    'message': 'Your export is being processed. You will receive an email when it\'s ready.'
                }, 202
                
            elif task_type == 'test-daily-reminder' and current_user.role == 'admin':
                # Admin can trigger test daily reminder
                try:
                    from tasks import send_daily_reminders
                    
                    # Try async first
                    try:
                        task = send_daily_reminders.delay()
                        return {
                            'msg': 'Daily reminder test started (async)',
                            'task_id': task.id,
                            'status': 'processing'
                        }, 202
                    except Exception as async_error:
                        # If async fails, run synchronously
                        print(f"Async failed, running sync: {async_error}")
                        result = send_daily_reminders()
                        return {
                            'msg': 'Daily reminder test completed (sync)',
                            'result': result,
                            'status': 'completed'
                        }, 200
                        
                except Exception as e:
                    return {'msg': 'Failed to run daily reminder', 'error': str(e)}, 500
                
            elif task_type == 'test-monthly-report' and current_user.role == 'admin':
                # Admin can trigger test monthly report  
                try:
                    from tasks import send_monthly_reports
                    
                    # Try async first
                    try:
                        task = send_monthly_reports.delay()
                        return {
                            'msg': 'Monthly report test started (async)',
                            'task_id': task.id,
                            'status': 'processing'
                        }, 202
                    except Exception as async_error:
                        # If async fails, run synchronously
                        print(f"Async failed, running sync: {async_error}")
                        result = send_monthly_reports()
                        return {
                            'msg': 'Monthly report test completed (sync)',
                            'result': result,
                            'status': 'completed'
                        }, 200
                        
                except Exception as e:
                    return {'msg': 'Failed to run monthly report', 'error': str(e)}, 500
                
            else:
                return {'msg': 'Invalid task type or insufficient permissions'}, 400
                
        except Exception as e:
            return {'msg': 'Failed to start task', 'error': str(e)}, 500
    
    @jwt_required()
    def get(self, task_type):
        """Get task status"""
        task_id = request.args.get('task_id')
        if not task_id:
            return {'msg': 'Task ID is required'}, 400
        
        try:
            from celery.result import AsyncResult
            from tasks import celery
            
            task_result = AsyncResult(task_id, app=celery)
            
            if task_result.state == 'PENDING':
                response = {
                    'state': task_result.state,
                    'status': 'Task is waiting to be processed'
                }
            elif task_result.state == 'PROGRESS':
                response = {
                    'state': task_result.state,
                    'status': task_result.info.get('status', ''),
                    'current': task_result.info.get('current', 0),
                    'total': task_result.info.get('total', 1)
                }
            elif task_result.state == 'SUCCESS':
                response = {
                    'state': task_result.state,
                    'status': 'Task completed successfully',
                    'result': task_result.result
                }
            else:
                # Something went wrong
                response = {
                    'state': task_result.state,
                    'status': 'Task failed',
                    'error': str(task_result.info)
                }
            
            return response, 200
            
        except Exception as e:
            return {'msg': 'Failed to get task status', 'error': str(e)}, 500


class ExportResource(Resource):
    @jwt_required()
    def get(self, export_type):
        try:
            current_user_id = int(get_jwt_identity())
            current_user = User.query.get(current_user_id)
            
            # Only admin can export data
            if current_user.role != 'admin':
                return {'msg': 'Access denied. Admin only.'}, 403
            
        except Exception as e:
            return {'msg': 'Authentication error', 'error': str(e)}, 401
        
        try:
            if export_type == 'parking-details':                
                # Alternative approach: Get reservations and fetch related data separately
                try:
                    # First, try the join approach
                    reservations = db.session.query(
                        ReserveSpot,
                        User.username,
                        User.email,
                        User.vehicle_number,
                        ParkingLot.location_name,
                        ParkingSpot.id.label('spot_number')
                    ).join(
                        User, ReserveSpot.user_id == User.id
                    ).join(
                        ParkingSpot, ReserveSpot.spot_id == ParkingSpot.id
                    ).join(
                        ParkingLot, ParkingSpot.lot_id == ParkingLot.id
                    ).all()
                    
                except Exception as join_error:
                    # Fallback: Get data separately
                    all_reservations = ReserveSpot.query.all()
                    reservations = []
                    
                    for reservation in all_reservations:
                        try:
                            user = User.query.get(reservation.user_id)
                            spot = ParkingSpot.query.get(reservation.spot_id)
                            lot = ParkingLot.query.get(spot.lot_id) if spot else None
                            
                            reservations.append((
                                reservation,
                                user.username if user else 'Unknown',
                                user.email if user else 'Unknown',
                                user.vehicle_number if user else None,
                                lot.location_name if lot else 'Unknown',
                                spot.id if spot else 'Unknown'
                            ))
                        except Exception as e:
                            continue
                    
                export_data = []
                for reservation, username, email, vehicle_number, location_name, spot_number in reservations:
                    try:
                        export_data.append({
                            'reservation_id': reservation.id,
                            'user_name': username,
                            'user_email': email,
                            'vehicle_number': vehicle_number or 'N/A',
                            'parking_lot': location_name,
                            'spot_number': spot_number,
                            'parking_time': reservation.parking_time.isoformat() if reservation.parking_time else None,
                            'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else 'Active',
                            'parking_cost': float(reservation.parking_cost) if reservation.parking_cost else 0,
                            'transaction_id': reservation.transaction_id or 'N/A',
                            'payment_method': reservation.payment_method or 'N/A',
                            'status': 'Completed' if reservation.leaving_time else 'Active'
                        })
                    except Exception as e:
                        continue

                return {
                    'msg': 'Parking details export data generated',
                    'data': export_data,
                    'total_records': len(export_data)
                }, 200
                
            elif export_type == 'monthly-report':
                # Generate monthly summary
                current_month = datetime.now().replace(day=1)
                next_month = current_month + timedelta(days=32)
                next_month = next_month.replace(day=1)
                
                month_reservations = ReserveSpot.query.filter(
                    ReserveSpot.parking_time >= current_month,
                    ReserveSpot.parking_time < next_month
                ).count()
                
                month_revenue = db.session.query(db.func.sum(ReserveSpot.parking_cost)).filter(
                    ReserveSpot.parking_time >= current_month,
                    ReserveSpot.parking_time < next_month,
                    ReserveSpot.leaving_time.isnot(None)
                ).scalar() or 0
                
                return {
                    'msg': 'Monthly report generated',
                    'data': {
                        'month': current_month.strftime('%B %Y'),
                        'total_reservations': month_reservations,
                        'total_revenue': round(float(month_revenue), 2),
                        'report_generated_at': datetime.now().isoformat()
                    }
                }, 200
                
            else:
                return {'msg': 'Invalid export type'}, 400
                
        except Exception as e:
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {'msg': 'Error generating export data', 'error': str(e)}, 500
