from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from models import *
from controllers import (
    UserResource,
    ParkingLotResource,
    ParkingSpotResource,
    AvailableSpotsResource,
    ReserveSpotResource,
    UserReservationsResource,
    LoginResource,
    RegisterResource
)
from flask_cors import CORS
from datetime import timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_app.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12) 
db.init_app(app)
jwt = JWTManager(app)
api = Api(app)
CORS(app)

#endpoints for the user
api.add_resource(UserResource, '/users', '/users/<user_id>')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(UserReservationsResource, '/users/<user_id>/reservations')

#endpoints for parking_lot
api.add_resource(ParkingLotResource, '/parking-lots', '/parking-lots/<lot_id>')
api.add_resource(AvailableSpotsResource, '/parking-lots/<lot_id>/available-spots')

#enpoints for parking_spot
api.add_resource(ParkingSpotResource, '/parking-spots', '/parking-spots/<spot_id>')

#endpoints for reservation
api.add_resource(ReserveSpotResource, '/reservations', '/reservations/<reservation_id>')

# Configure CORS properly
CORS(app, origins=["http://localhost:5174", "http://127.0.0.1:5174"])

@app.route('/', methods=['GET'])
def home():
    return {'msg': 'working fine?'}, 200

@app.route('/debug/tables', methods=['GET'])
def debug_tables():
    """Debug endpoint to check database tables and data"""
    try:
        from sqlalchemy import text
        
        # Check if tables exist
        result = {}
        
        # Check users
        users_count = db.session.execute(text("SELECT COUNT(*) FROM user")).scalar()
        result['users_count'] = users_count
        
        # Check parking lots
        lots_count = db.session.execute(text("SELECT COUNT(*) FROM parking_lot")).scalar()
        result['parking_lots_count'] = lots_count
        
        # Check parking spots
        spots_count = db.session.execute(text("SELECT COUNT(*) FROM parking_spot")).scalar()
        result['parking_spots_count'] = spots_count
        
        # Check reservations
        reservations_count = db.session.execute(text("SELECT COUNT(*) FROM reserve_spot")).scalar()
        result['reservations_count'] = reservations_count
        
        # Get sample user
        sample_user = db.session.execute(text("SELECT id, username, email FROM user LIMIT 1")).fetchone()
        if sample_user:
            result['sample_user'] = {
                'id': sample_user[0],
                'username': sample_user[1], 
                'email': sample_user[2]
            }
        
        return result, 200
        
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #this will help to create an admin user whenever a new database is created
        admin = User.query.filter_by(email='admin@mad2.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@mad2.com',
                role='admin',
                password='Admin@123',
                phone_number='8709186793'
            )
            db.session.add(admin)
        db.session.commit()
        app.run(debug=True)