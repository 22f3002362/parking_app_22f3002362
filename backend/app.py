from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import User, db, ParkingLot, ParkingSpot, ReserveSpot
from controllers import (
    UserResource,
    ParkingLotResource,
    ParkingSpotResource,
    AvailableSpotsResource,
    ReserveSpotResource,
    UserReservationsResource,
    LoginResource
)
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_app.db'
db.init_app(app)
api = Api(app)
CORS(app)

#endpoints for the user
api.add_resource(UserResource, '/users', '/users/<user_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(UserReservationsResource, '/users/<user_id>/reservations')

#endpoints for parking_lot
api.add_resource(ParkingLotResource, '/parking-lots', '/parking-lots/<lot_id>')
api.add_resource(AvailableSpotsResource, '/parking-lots/<lot_id>/available-spots')

#enpoints for parking_spot
api.add_resource(ParkingSpotResource, '/parking-spots', '/parking-spots/<spot_id>')

#endpoints for reservation
api.add_resource(ReserveSpotResource, '/reservations', '/reservations/<reservation_id>')

CORS(app, origins=["http://127.0.0.1:5000/users"])

@app.route('/', methods=['GET'])
def home():
    return {'msg': 'working fine?'}, 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #this will help to create an admin user whenever a new database is created
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@gmail.com',
                role='admin',
                password='admin123',
                vehicle_number='KA-01-AB-1234' #just a demo number...
            )
            db.session.add(admin)
        db.session.commit()
        app.run(debug=True)