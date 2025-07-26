from flask_restful import Resource, Api
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, ParkingLot, ParkingSpot, ReserveSpot
from datetime import datetime, timedelta

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if user_id:
            # Only allow users to access their own data or admin to access any
            if current_user.role != 'admin' and current_user_id != user_id:
                return {'msg': 'Access denied'}, 403
                
            user = User.query.get(user_id)
            if user:
                return {
                    'msg': 'User found',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'vehicle_number': user.vehicle_number,
                        'phone_number': user.phone_number if user.phone_number else None
                    }
                }, 200
            return {'msg': 'User not found'}, 404
        
        # Only admin can get all users
        if current_user.role != 'admin':
            return {'msg': 'Access denied. Admin only.'}, 403
            
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
        return {'msg': 'Users retrieved successfully', 'users': user_list}, 200
    
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
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'msg': 'User with this email already exists'}, 400
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return {'msg': 'Username already exists'}, 400
        
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
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {'msg': 'User deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error deleting user', 'error': str(e)}, 500


class ParkingLotResource(Resource):
    
    def get(self, lot_id=None):
        if lot_id:
            lot = ParkingLot.query.get(lot_id)
            if lot:
                return {
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
                }, 200
            return {'msg': 'Parking lot not found'}, 404
        
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
        return {'msg': 'Parking lots retrieved successfully', 'lots': lot_list}, 200
    
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
        
        # print(f"UserReservationsResource: user_id parameter: {user_id}, type: {type(user_id)}")
        # print(f"Current user ID: {current_user_id}, Current user: {current_user}")
        
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
        
        # print(f"Fetching reservations for user: {user.username}")
        
        try:
            reservations = ReserveSpot.query.filter_by(user_id=user_id).all()
            # print(f"Found {len(reservations)} reservations")
        except Exception as e:
            # print(f"Database error when fetching reservations: {str(e)}")
            return {'msg': 'Database error occurred', 'error': str(e)}, 500
        
        reservation_list = []
        for reservation in reservations:
            try:
                # print(f"Processing reservation: {reservation.id}")
                # Get spot and lot information
                spot = ParkingSpot.query.get(reservation.spot_id)
                lot = ParkingLot.query.get(spot.lot_id) if spot else None
                
                reservation_list.append({
                    'id': reservation.id,
                    'spot_id': reservation.spot_id,
                    'lot_name': lot.location_name if lot else 'Unknown',
                    'lot_address': lot.address if lot else 'Unknown',
                    'parking_time': reservation.parking_time.isoformat(),
                    'leaving_time': reservation.leaving_time.isoformat() if reservation.leaving_time else None,
                    'parking_cost': reservation.parking_cost,
                    'transaction_id': reservation.transaction_id,
                    'payment_method': reservation.payment_method
                })
            except Exception as e:
                # print(f"Error processing reservation {reservation.id}: {str(e)}")
                continue  # Skip this reservation but continue with others
        
        result = {
            'msg': 'User reservations retrieved successfully',
            'user': user.username,
            'reservations': reservation_list
        }
        # print(f"Returning result: {result}")
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
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'msg': 'User with this email already exists'}, 409
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return {'msg': 'Username already exists'}, 409
        
        # Check if vehicle number already exists (only if provided)
        if vehicle_number:
            existing_vehicle = User.query.filter_by(vehicle_number=vehicle_number).first()
            if existing_vehicle:
                return {'msg': 'Vehicle number already exists'}, 409
        
        # Check if phone number already exists (only if provided)
        if phone_number:
            existing_phone = User.query.filter_by(phone_number=phone_number).first()
            if existing_phone:
                return {'msg': 'Phone number already exists'}, 409
        
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
                # - Minimum 1 hour charge regardless of actual time
                # - Any additional time is charged as full hours (rounded up)
                if duration_hours <= 1:
                    # Any parking up to 1 hour is charged as 1 full hour
                    charged_hours = 1
                else:
                    # More than 1 hour: round up to next full hour
                    import math
                    charged_hours = math.ceil(duration_hours)
                
                # Calculate final cost
                reservation.parking_cost = float(charged_hours * lot.price)
                
                # Store transaction details if provided
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
                    }
                }
            }, 200
            
        except Exception as e:
            return {'msg': 'Error retrieving reports data', 'error': str(e)}, 500


class ExportResource(Resource):
    @jwt_required()
    def get(self, export_type):
        try:
            current_user_id = int(get_jwt_identity())
            current_user = User.query.get(current_user_id)
            
            # Only admin can export data
            if current_user.role != 'admin':
                return {'msg': 'Access denied. Admin only.'}, 403
            
            print(f"Export request for type: {export_type}")  # Debug logging
            
        except Exception as e:
            print(f"Authentication error in export: {str(e)}")
            return {'msg': 'Authentication error', 'error': str(e)}, 401
        
        try:
            if export_type == 'parking-details':
                print("Starting parking-details export...")  # Debug logging
                
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
                    
                    print(f"Join approach successful: Found {len(reservations)} reservations")
                    
                except Exception as join_error:
                    print(f"Join approach failed: {str(join_error)}")
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
                            print(f"Error processing reservation {reservation.id}: {str(e)}")
                            continue
                    
                    print(f"Fallback approach: Found {len(reservations)} reservations")
                
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
                        print(f"Error processing reservation {reservation.id}: {str(e)}")
                        continue
                
                print(f"Successfully processed {len(export_data)} records")  # Debug logging
                
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
            print(f"Error in ExportResource: {str(e)}")  # Debug logging
            import traceback
            traceback.print_exc()  # Print full stack trace
            return {'msg': 'Error generating export data', 'error': str(e)}, 500
