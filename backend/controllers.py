from flask_restful import Resource, Api
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, ParkingLot, ParkingSpot, ReserveSpot
from datetime import datetime

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
            user.vehicle_number = data['vehicle_number']
        if 'phone_number' in data:
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
                        'leaving_time': reservation.leaving_time.isoformat(),
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
                'leaving_time': reservation.leaving_time.isoformat(),
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
                    'leaving_time': reservation.leaving_time.isoformat(),
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
        
        print(f"UserReservationsResource: user_id parameter: {user_id}, type: {type(user_id)}")
        print(f"Current user ID: {current_user_id}, Current user: {current_user}")
        
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
        
        print(f"Fetching reservations for user: {user.username}")
        
        try:
            reservations = ReserveSpot.query.filter_by(user_id=user_id).all()
            print(f"Found {len(reservations)} reservations")
        except Exception as e:
            print(f"Database error when fetching reservations: {str(e)}")
            return {'msg': 'Database error occurred', 'error': str(e)}, 500
        
        reservation_list = []
        for reservation in reservations:
            try:
                print(f"Processing reservation: {reservation.id}")
                # Get spot and lot information
                spot = ParkingSpot.query.get(reservation.spot_id)
                lot = ParkingLot.query.get(spot.lot_id) if spot else None
                
                reservation_list.append({
                    'id': reservation.id,
                    'spot_id': reservation.spot_id,
                    'lot_name': lot.location_name if lot else 'Unknown',
                    'lot_address': lot.address if lot else 'Unknown',
                    'parking_time': reservation.parking_time.isoformat(),
                    'leaving_time': reservation.leaving_time.isoformat(),
                    'parking_cost': reservation.parking_cost
                })
            except Exception as e:
                print(f"Error processing reservation {reservation.id}: {str(e)}")
                continue  # Skip this reservation but continue with others
        
        result = {
            'msg': 'User reservations retrieved successfully',
            'user': user.username,
            'reservations': reservation_list
        }
        print(f"Returning result: {result}")
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
        
        # Create new user
        user = User(
            email=email,
            username=username,
            password=password,
            role=role,
            vehicle_number=vehicle_number if vehicle_number else None
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
                    'vehicle_number': user.vehicle_number
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Registration failed. Please try again.'}, 500
