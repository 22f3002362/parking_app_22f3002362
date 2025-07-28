from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from models import *
from controllers import (
    UserResource,
    ParkingLotResource,
    ParkingSpotResource,
    AvailableSpotsResource,
    ReserveSpotResource,
    UserReservationsResource,
    LoginResource,
    RegisterResource,
    LogoutResource,
    BookingResource,
    ReportsResource,
    UserReportsResource,
    UserBookingHistoryResource,
    ExportResource
)
from flask_cors import CORS
from datetime import timedelta, datetime
from redis import Redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_app.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=12)

# Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Celery configuration
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)
mail = Mail(app)
CORS(app)

# Initialize Celery
# from celery_app import create_celery
# celery = create_celery(app)

# Redis Configuration with error handling
try:
    redis_client = Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=int(os.getenv('REDIS_DB', 0)),
        decode_responses=True,  # Automatically decode responses to strings
        socket_connect_timeout=5,
        socket_timeout=5
    )
    
    # Test Redis connection
    redis_client.ping()
    redis_client.set('app_name', 'Parking Management System', ex=3600)  # Expire in 1 hour
    print(f"✅ Connected to Redis: {redis_client.get('app_name')}")
    
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    print("Application will continue without Redis caching")
    redis_client = None

#endpoints for the user
api.add_resource(UserResource, '/users', '/users/<user_id>')
api.add_resource(LoginResource, '/auth/login')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LogoutResource, '/auth/logout')
api.add_resource(UserReservationsResource, '/users/<user_id>/reservations')

#endpoints for parking_lot
api.add_resource(ParkingLotResource, '/parking-lots', '/parking-lots/<lot_id>')
api.add_resource(AvailableSpotsResource, '/parking-lots/<lot_id>/available-spots')

#enpoints for parking_spot
api.add_resource(ParkingSpotResource, '/parking-spots', '/parking-spots/<spot_id>')

#endpoints for reservation
api.add_resource(ReserveSpotResource, '/reservations', '/reservations/<reservation_id>')

#endpoints for booking
api.add_resource(BookingResource, '/booking/<action>')

#endpoints for reports and analytics
api.add_resource(ReportsResource, '/reports')
api.add_resource(UserReportsResource, '/user-reports')
api.add_resource(UserBookingHistoryResource, '/user-booking-history')
api.add_resource(ExportResource, '/export/<export_type>')

# Configure CORS properly
CORS(app, origins=["http://localhost:5174", "http://127.0.0.1:5174"])

# Make Redis client available to the app context
app.redis_client = redis_client

# Middleware to track API calls and user activity
@app.before_request
def before_request():
    """Track API calls and user activity"""
    if redis_client:
        try:
            # Increment total API calls
            redis_client.incr('total_api_calls')
            
            # Track endpoint-specific calls
            endpoint = request.endpoint
            if endpoint:
                redis_client.incr(f'endpoint_calls:{endpoint}')
                
        except Exception as e:
            print(f"Redis tracking error: {e}")

@app.after_request
def after_request(response):
    """Track response codes"""
    if redis_client:
        try:
            status_code = response.status_code
            redis_client.incr(f'response_codes:{status_code}')
        except Exception as e:
            print(f"Redis response tracking error: {e}")
    return response

@app.route('/', methods=['GET'])
def home():
    return {'msg': 'working fine?'}, 200

@app.route('/health/redis', methods=['GET'])
def redis_health():
    """Check Redis connection health"""
    if redis_client:
        try:
            redis_client.ping()
            stats = {
                'status': 'connected',
                'active_users': redis_client.scard('active_users'),
                'total_logins': int(redis_client.get('total_logins') or 0),
                'total_registrations': int(redis_client.get('total_registrations') or 0),
                'app_name': redis_client.get('app_name')
            }
            return {'msg': 'Redis is healthy', 'stats': stats}, 200
        except Exception as e:
            return {'msg': 'Redis connection failed', 'error': str(e)}, 500
    else:
        return {'msg': 'Redis not configured'}, 503

@app.route('/admin/redis-dashboard', methods=['GET'])
def redis_dashboard():
    """Comprehensive Redis monitoring dashboard"""
    if not redis_client:
        return {'msg': 'Redis not available'}, 503
    
    try:
        dashboard_data = {
            'connection_status': 'connected',
            'server_info': {
                'redis_version': redis_client.info().get('redis_version', 'unknown'),
                'used_memory_human': redis_client.info().get('used_memory_human', 'unknown'),
                'connected_clients': redis_client.info().get('connected_clients', 0)
            },
            'application_metrics': {
                'total_api_calls': int(redis_client.get('total_api_calls') or 0),
                'total_logins': int(redis_client.get('total_logins') or 0),
                'total_logouts': int(redis_client.get('total_logouts') or 0),
                'total_registrations': int(redis_client.get('total_registrations') or 0),
                'active_users_count': redis_client.scard('active_users'),
                'users_created': int(redis_client.get('users_created') or 0),
                'users_deleted': int(redis_client.get('users_deleted') or 0),
                'parking_lots_created': int(redis_client.get('parking_lots_created') or 0),
                'parking_lots_deleted': int(redis_client.get('parking_lots_deleted') or 0),
                'total_reservations': int(redis_client.get('total_reservations') or 0),
                'reservations_cancelled': int(redis_client.get('reservations_cancelled') or 0)
            },
            'daily_metrics': {
                'today_logins': int(redis_client.get(f'daily_logins:{datetime.now().strftime("%Y-%m-%d")}') or 0),
                'today_registrations': int(redis_client.get(f'daily_registrations:{datetime.now().strftime("%Y-%m-%d")}') or 0),
                'today_reservations': int(redis_client.get(f'daily_reservations:{datetime.now().strftime("%Y-%m-%d")}') or 0)
            },
            'response_codes': {
                '200': int(redis_client.get('response_codes:200') or 0),
                '201': int(redis_client.get('response_codes:201') or 0),
                '400': int(redis_client.get('response_codes:400') or 0),
                '401': int(redis_client.get('response_codes:401') or 0),
                '403': int(redis_client.get('response_codes:403') or 0),
                '404': int(redis_client.get('response_codes:404') or 0),
                '500': int(redis_client.get('response_codes:500') or 0)
            },
            'cache_info': {
                'total_keys': len(redis_client.keys('*')),
                'active_sessions': len(redis_client.keys('user_session:*')),
                'cached_parking_lots': len(redis_client.keys('parking_lot:*')),
                'rate_limits_active': len(redis_client.keys('rate_limit:*'))
            }
        }
        
        return {'msg': 'Redis dashboard data', 'data': dashboard_data}, 200
        
    except Exception as e:
        return {'msg': 'Error fetching Redis dashboard data', 'error': str(e)}, 500

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