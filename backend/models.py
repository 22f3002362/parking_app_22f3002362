from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    password = db.Column(db.String(200), nullable=False)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=True)


class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    number_of_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)


class ParkingSpot(db.Model):  # Fixed: Capital P in ParkingSpot
    __tablename__ = 'parking_spot'  # Added explicit table name
    id = db.Column(db.Integer, primary_key=True)  # Fixed: db.Column (capital C)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='available')


class ReserveSpot(db.Model):
    __tablename__ = 'reserve_spot'  # Added explicit table name
    id = db.Column(db.Integer, primary_key=True)  # Fixed: db.Column (capital C)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_time = db.Column(db.DateTime, nullable=False)
    leaving_time = db.Column(db.DateTime, nullable=False)
    parking_cost = db.Column(db.Float, nullable=False)


