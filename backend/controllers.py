from flask_restful import Resource, Api
from flask import request
from models import db, User, ParkingLot, ParkingSpot, ReserveSpot
from datetime import datetime

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {
                    'msg': 'User found',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'vehicle_number': user.vehicle_number
                    }
                }, 201
            return {'msg': 'User not found'}, 404
        
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'vehicle_number': user.vehicle_number
            })
        return {'msg': 'Users retrieved successfully', 'users': user_list}, 200
    
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
            return {'msg': 'User already exists'}, 400
        
        # Create new user
        user = User(
            email=email,
            username=username,
            password=password,
            role=role,
            vehicle_number=vehicle_number
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
                    'vehicle_number': user.vehicle_number
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error creating user', 'error': str(e)}, 500
    
    def put(self, user_id):
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
        if 'role' in data:
            user.role = data['role']
        if 'vehicle_number' in data:
            user.vehicle_number = data['vehicle_number']
        
        try:
            db.session.commit()
            return {
                'msg': 'User updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'vehicle_number': user.vehicle_number
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'msg': 'Error updating user', 'error': str(e)}, 500
    
    def delete(self, user_id):
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
    
    def post(self):
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
    
    def put(self, lot_id):
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
    
    def delete(self, lot_id):
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
    
    def post(self):
        data = request.get_json()
        spot_id = data.get('spot_id')
        user_id = data.get('user_id')
        parking_time = data.get('parking_time')
        leaving_time = data.get('leaving_time')
        
        if not all([spot_id, user_id, parking_time, leaving_time]):
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
    
    def delete(self, reservation_id):
        reservation = ReserveSpot.query.get(reservation_id)
        if not reservation:
            return {'msg': 'Reservation not found'}, 404
        
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
    
    def get(self, user_id):
        """Get all reservations for a specific user"""
        user = User.query.get(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        
        reservations = ReserveSpot.query.filter_by(user_id=user_id).all()
        reservation_list = []
        for reservation in reservations:
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
        
        return {
            'msg': 'User reservations retrieved successfully',
            'user': user.username,
            'reservations': reservation_list
        }, 200


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
        
        return {
            'msg': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'vehicle_number': user.vehicle_number
            }
        }, 200
