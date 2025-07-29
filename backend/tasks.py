from celery_app import celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Message
from models import db, User, ParkingLot, ReserveSpot, ParkingSpot
import csv
import io
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import json
import requests

def get_app_context():
    """Helper function to get Flask app context"""
    from app import app
    return app

def send_simple_email(to_email, subject, body, html_body=None, attachment_path=None):
    """
    Simple email sender using SMTP - works without verification
    """
    try:
        smtp_server = "localhost"
        smtp_port = 1025
        sender_email = "no-reply@parkease.com" 
        sender_password = "" 
        
        print(f"🔧 Attempting to send email to {to_email}")
        print(f"🔧 Subject: {subject}")
        print(f"🔧 SMTP: {smtp_server}:{smtp_port}")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        
        # Add text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}',
                )
                msg.attach(part)
        
        # Send email using MailHog
        server = smtplib.SMTP(smtp_server, smtp_port)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to MailHog: {to_email} - {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print(f"❌ Make sure MailHog is running on localhost:1025")
        return False

@celery.task(bind=True)
def send_daily_reminders(self):
    """
    Daily scheduled job - Send reminders to users
    Checks if user hasn't visited recently or new parking lots are available
    """
    try:
        with get_app_context().app_context():
            print("🔄 Starting daily reminder job...")
            
            # Get all users
            users = User.query.filter_by(role='user').all()
            seven_days_ago = datetime.now() - timedelta(days=7)
            inactive_users = []
            
            for user in users:
                recent_reservation = ReserveSpot.query.filter(
                    ReserveSpot.user_id == user.id,
                    ReserveSpot.parking_time >= seven_days_ago
                ).first()
                
                if not recent_reservation:
                    inactive_users.append(user)
            
            new_lots = ParkingLot.query.all()  
            
            sent_count = 0
            
            # Send reminders to inactive users
            for user in inactive_users:
                subject = "Parking Reminder - Book Your Spot Today!"
                
                body = f"""
Hello {user.username}!

We noticed you haven't booked a parking spot recently. 

Here are some available parking lots for you:
"""
                
                # Add available lots info
                for lot in new_lots[:3]:  # Show top 3 lots
                    body += f"""
* {lot.location_name}
   Address: {lot.address}
   Price: Rs {lot.price}/hour
   Available Spots: {lot.available_slots}/{lot.number_of_slots}
"""
                
                body += """

Book your parking spot now to secure your place!

Best regards,
Parking Management Team
"""
                
                # Send email
                if send_simple_email(user.email, subject, body):
                    sent_count += 1
            
            # Also notify about new parking lots to all users
            if new_lots:
                active_users = [user for user in users if user not in inactive_users]
                for user in active_users:  # Limit to 5 users for testing
                    subject = "New Parking Lots Available!"
                    
                    body = f"""
Hello {user.username}!

Great news! New parking lots are now available:

"""
                    for lot in new_lots[:2]:
                        body += f"""
* {lot.location_name}
   Address: {lot.address}
   Price: Rs {lot.price}/hour
   Available Spots: {lot.available_slots}/{lot.number_of_slots}

"""
                    
                    body += """
Check out these new locations and book your spot today!

Best regards,
ParkEase-Smart Parking Solutions
"""
                    
                    if send_simple_email(user.email, subject, body):
                        sent_count += 1
            
            print(f"✅ Daily reminder job completed. Sent {sent_count} emails.")
            return f"Sent {sent_count} reminder emails successfully"
            
    except Exception as e:
        print(f"❌ Daily reminder job failed: {str(e)}")
        raise self.retry(countdown=300, max_retries=3)

@celery.task(bind=True)
def send_monthly_reports(self):
    """
    Monthly scheduled job - Send activity reports to users
    Creates HTML report with user's monthly parking activity
    """
    try:
        with get_app_context().app_context():
            print("🔄 Starting monthly report job...")
            
            # Get current month
            now = datetime.now()
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Get all users who had activity this month
            users_with_activity = db.session.query(User).join(ReserveSpot).filter(
                ReserveSpot.parking_time >= first_day
            ).distinct().all()
            
            # If no users with activity, send to all users for demo
            if not users_with_activity:
                users_with_activity = User.query.filter_by(role='user').limit(5).all()
            
            sent_count = 0
            
            for user in users_with_activity:
                # Get user's monthly data
                user_reservations = ReserveSpot.query.filter(
                    ReserveSpot.user_id == user.id,
                    ReserveSpot.parking_time >= first_day
                ).all()
                
                # Calculate statistics
                total_bookings = len(user_reservations)
                total_spent = sum(float(r.parking_cost or 0) for r in user_reservations if r.leaving_time)
                total_hours = 0
                
                lot_usage = {}
                for reservation in user_reservations:
                    if reservation.leaving_time and reservation.parking_time:
                        duration = (reservation.leaving_time - reservation.parking_time).total_seconds() / 3600
                        total_hours += duration
                    
                    # Get lot information
                    spot = ParkingSpot.query.get(reservation.spot_id)
                    if spot:
                        lot = ParkingLot.query.get(spot.lot_id)
                        if lot:
                            lot_name = lot.location_name
                            lot_usage[lot_name] = lot_usage.get(lot_name, 0) + 1
                
                # Find most used lot
                most_used_lot = max(lot_usage.items(), key=lambda x: x[1]) if lot_usage else ("None", 0)
                
                # Create HTML report
                html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
        .stat-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .section {{ margin: 20px 0; }}
        .section h3 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 5px; }}
        .lot-item {{ background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Monthly Parking Report</h1>
            <p>{now.strftime('%B %Y')} Activity Summary for {user.username}</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{total_bookings}</div>
                <div class="stat-label">Total Bookings</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">Rs {total_spent}</div>
                <div class="stat-label">Total Spent</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{total_hours:.1f}h</div>
                <div class="stat-label">Total Hours</div>
            </div>
        </div>
        
        <div class="section">
            <h3>Your Parking Summary</h3>
            <p><strong>Most Used Location:</strong> {most_used_lot[0]} ({most_used_lot[1]} times)</p>
            <p><strong>Average Cost per Booking:</strong> Rs {(total_spent/total_bookings) if total_bookings > 0 else 0:.2f}</p>
            <p><strong>Average Duration per Booking:</strong> {(total_hours/total_bookings) if total_bookings > 0 else 0:.1f} hours</p>
        </div>
        
        <div class="section">
            <h3>Location Usage</h3>
"""
                
                for lot_name, count in sorted(lot_usage.items(), key=lambda x: x[1], reverse=True):
                    html_report += f'<div class="lot-item">* {lot_name}: {count} bookings</div>'
                
                html_report += f"""
        </div>
        
        <div class="section">
            <h3>Tips for Next Month</h3>
            <ul>
                <li>Book in advance to get better rates</li>
                <li>Try different locations to find the best deals</li>
                <li>Check for off-peak hour discounts</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated on {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>ParkEase-Smart Parking Solutions</p>
        </div>
    </div>
</body>
</html>
"""
                
                # Text version for email clients that don't support HTML
                text_report = f"""
Monthly Parking Report - {now.strftime('%B %Y')}
Hello {user.username}!

Your parking activity summary:
* Total Bookings: {total_bookings}
* Total Spent: RS {total_spent:.2f}
* Total Hours: {total_hours:.1f}
* Most Used Location: {most_used_lot[0]} ({most_used_lot[1]} times)

Location Usage:
"""
                for lot_name, count in sorted(lot_usage.items(), key=lambda x: x[1], reverse=True):
                    text_report += f"* {lot_name}: {count} bookings\n"
                
                text_report += """
Thanks for using our parking service!

Best regards,
ParkEase-Smart Parking Solutions
"""
                
                # Send email with HTML report
                subject = f"Your Monthly Parking Report - {now.strftime('%B %Y')}"
                
                if send_simple_email(user.email, subject, text_report, html_report):
                    sent_count += 1
            
            print(f"✅ Monthly report job completed. Sent {sent_count} reports.")
            return f"Sent {sent_count} monthly reports successfully"
            
    except Exception as e:
        print(f"❌ Monthly report job failed: {str(e)}")
        raise self.retry(countdown=300, max_retries=3)

@celery.task(bind=True)
def export_user_data_csv(self, user_id, export_type="full"):
    """
    User triggered async job - Export user parking data as CSV
    """
    try:
        with get_app_context().app_context():
            print(f"🔄 Starting CSV export for user {user_id}...")
            
            # Get user
            user = User.query.get(user_id)
            if not user:
                return {"status": "error", "message": "User not found"}
            
            # Get user's reservations
            reservations = ReserveSpot.query.filter_by(user_id=user_id).order_by(ReserveSpot.parking_time.desc()).all()
            
            # Create CSV data
            csv_data = []
            csv_headers = [
                'Reservation ID', 'Parking Lot', 'Spot ID', 'Start Time', 
                'End Time', 'Duration (Hours)', 'Cost (Rs)', 'Status',
                'Transaction ID', 'Payment Method', 'Vehicle Number'
            ]
            
            for reservation in reservations:
                try:
                    # Get spot and lot info
                    spot = ParkingSpot.query.get(reservation.spot_id)
                    lot_name = "Unknown"
                    if spot:
                        lot = ParkingLot.query.get(spot.lot_id)
                        if lot:
                            lot_name = lot.location_name
                    
                    # Calculate duration
                    duration = 0
                    if reservation.leaving_time and reservation.parking_time:
                        duration = (reservation.leaving_time - reservation.parking_time).total_seconds() / 3600
                    
                    csv_row = [
                        reservation.id,
                        lot_name,
                        reservation.spot_id,
                        reservation.parking_time.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_time else '',
                        reservation.leaving_time.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_time else 'Active',
                        f"{duration:.2f}" if duration > 0 else '0.00',
                        f"{float(reservation.parking_cost):.2f}" if reservation.parking_cost else '0.00',
                        'Completed' if reservation.leaving_time else 'Active',
                        reservation.transaction_id or 'N/A',
                        reservation.payment_method or 'N/A',
                        user.vehicle_number or 'N/A'
                    ]
                    csv_data.append(csv_row)
                    
                except Exception as e:
                    print(f"Error processing reservation {reservation.id}: {e}")
                    continue
            
            # Create CSV file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"parking_history_{user.username}_{timestamp}.csv"
            filepath = os.path.join(os.getcwd(), 'exports', filename)
            
            # Create exports directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Write CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csv_headers)
                writer.writerows(csv_data)
            
            # Send notification email with attachment
            subject = f"🗂️ Your Parking History Export is Ready!"
            
            body = f"""
Hello {user.username}!

Your parking history export has been completed successfully.

Export Details:
* Total Records: {len(csv_data)}
* Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
* File Format: CSV

The file contains all your parking bookings with detailed information including:
- Booking timestamps
- Parking locations
- Duration and costs  
- Payment details
- Transaction history

Best regards,
ParkEase-Smart Parking Solutions
"""
            
            # Send email with CSV attachment
            email_sent = send_simple_email(user.email, subject, body, attachment_path=filepath)
            
            print(f"✅ CSV export completed for user {user_id}. File: {filename}")
            
            return {
                "status": "success",
                "message": f"CSV export completed successfully. {len(csv_data)} records exported.",
                "filename": filename,
                "records_count": len(csv_data),
                "email_sent": email_sent,
                "file_path": filepath
            }
            
    except Exception as e:
        print(f"❌ CSV export failed for user {user_id}: {str(e)}")
        return {
            "status": "error", 
            "message": f"Export failed: {str(e)}"
        }

@celery.task(bind=True)
def send_booking_confirmation_email(self, reservation_id):
    """
    Send booking confirmation email to user
    """
    try:
        with get_app_context().app_context():
            reservation = ReserveSpot.query.get(reservation_id)
            if not reservation:
                print(f"❌ Reservation {reservation_id} not found")
                return f"Reservation {reservation_id} not found"
            
            user = User.query.get(reservation.user_id)
            parking_spot = ParkingSpot.query.get(reservation.spot_id)
            parking_lot = ParkingLot.query.get(parking_spot.lot_id) if parking_spot else None
            
            if not user or not parking_lot or not parking_spot:
                print(f"❌ Missing data for reservation {reservation_id}")
                return f"Missing data for reservation {reservation_id}"
            
            subject = f"Booking Confirmation - {parking_lot.location_name}"
            
            # Calculate duration properly handling None leaving_time
            if reservation.leaving_time:
                duration_hours = (reservation.leaving_time - reservation.parking_time).total_seconds() / 3600
                duration_text = f"{duration_hours:.1f} hours"
                end_time_text = reservation.leaving_time.strftime('%Y-%m-%d %H:%M')
            else:
                duration_text = "Open-ended"
                end_time_text = "Open"
            
            body = f"""
Dear {user.username},

Your parking booking has been confirmed!

Booking Details:
- Parking Lot: {parking_lot.location_name}
- Address: {parking_lot.address}
- Spot ID: {parking_spot.id}
- Start Time: {reservation.parking_time.strftime('%Y-%m-%d %H:%M')}
- End Time: {end_time_text}
- Duration: {duration_text}
- Total Cost: Rs {reservation.parking_cost:.2f}

Please arrive on time and remember your booking details.

Best regards,
ParkEase-Smart Parking Solutions
            """
            
            html_body = f"""
            <html>
            <body>
                <h2>Booking Confirmation</h2>
                <p>Dear <strong>{user.username}</strong>,</p>
                <p>Your parking booking has been confirmed!</p>
                
                <h3>Booking Details:</h3>
                <ul>
                    <li><strong>Parking Lot:</strong> {parking_lot.location_name}</li>
                    <li><strong>Address:</strong> {parking_lot.address}</li>
                    <li><strong>Spot ID:</strong> {parking_spot.id}</li>
                    <li><strong>Start Time:</strong> {reservation.parking_time.strftime('%Y-%m-%d %H:%M')}</li>
                    <li><strong>End Time:</strong> {end_time_text}</li>
                    <li><strong>Duration:</strong> {duration_text}</li>
                    <li><strong>Total Cost:</strong> Rs {reservation.parking_cost:.2f}</li>
                </ul>
                
                <p>Please arrive on time and remember your booking details.</p>
                
                <p>Best regards,<br>
                <strong>Parking Management System</strong></p>
            </body>
            </html>
            """
            
            if send_simple_email(user.email, subject, body, html_body):
                print(f"✅ Booking confirmation email sent to {user.email}")
                return f"Booking confirmation email sent to {user.email}"
            else:
                print(f"❌ Failed to send booking confirmation email to {user.email}")
                return f"Failed to send booking confirmation email to {user.email}"
                
    except Exception as e:
        print(f"❌ Booking confirmation email task failed: {str(e)}")
        return f"Booking confirmation email task failed: {str(e)}"

@celery.task(bind=True)
def send_parking_release_email(self, reservation_id):
    """
    Send parking release/checkout email to user
    """
    try:
        with get_app_context().app_context():
            reservation = ReserveSpot.query.get(reservation_id)
            if not reservation:
                print(f"❌ Reservation {reservation_id} not found")
                return f"Reservation {reservation_id} not found"
            
            user = User.query.get(reservation.user_id)
            parking_spot = ParkingSpot.query.get(reservation.spot_id)
            parking_lot = ParkingLot.query.get(parking_spot.lot_id) if parking_spot else None
            
            if not user or not parking_lot or not parking_spot:
                print(f"❌ Missing data for reservation {reservation_id}")
                return f"Missing data for reservation {reservation_id}"
            
            subject = f"Parking Released - {parking_lot.location_name}"
            actual_end_time = reservation.leaving_time or datetime.now()
            
            body = f"""
Dear {user.username},

Your parking session has been completed and the spot has been released.

Session Summary:
- Parking Lot: {parking_lot.location_name}
- Address: {parking_lot.address}
- Spot ID: {parking_spot.id}
- Start Time: {reservation.parking_time.strftime('%Y-%m-%d %H:%M')}
- End Time: {actual_end_time.strftime('%Y-%m-%d %H:%M')}
- Duration: {(actual_end_time - reservation.parking_time).total_seconds() / 3600:.1f} hours
- Total Cost: Rs {reservation.parking_cost:.2f}

Thank you for using our parking service!

Best regards,
ParkEase-Smart Parking Solutions
            """
            
            html_body = f"""
            <html>
            <body>
                <h2>Parking Session Completed</h2>
                <p>Dear <strong>{user.username}</strong>,</p>
                <p>Your parking session has been completed and the spot has been released.</p>
                
                <h3>Session Summary:</h3>
                <ul>
                    <li><strong>Parking Lot:</strong> {parking_lot.location_name}</li>
                    <li><strong>Address:</strong> {parking_lot.address}</li>
                    <li><strong>Spot ID:</strong> {parking_spot.id}</li>
                    <li><strong>Start Time:</strong> {reservation.parking_time.strftime('%Y-%m-%d %H:%M')}</li>
                    <li><strong>End Time:</strong> {actual_end_time.strftime('%Y-%m-%d %H:%M')}</li>
                    <li><strong>Duration:</strong> {(actual_end_time - reservation.parking_time).total_seconds() / 3600:.1f} hours</li>
                    <li><strong>Total Cost:</strong> Rs {reservation.parking_cost:.2f}</li>
                </ul>
                
                <p>Thank you for using our parking service!</p>
                
                <p>Best regards,<br>
                <strong>ParkEase-Smart Parking Solutions</strong></p>
            </body>
            </html>
            """
            
            if send_simple_email(user.email, subject, body, html_body):
                print(f"✅ Parking release email sent to {user.email}")
                return f"Parking release email sent to {user.email}"
            else:
                print(f"❌ Failed to send parking release email to {user.email}")
                return f"Failed to send parking release email to {user.email}"
                
    except Exception as e:
        print(f"❌ Parking release email task failed: {str(e)}")
        return f"Parking release email task failed: {str(e)}"

if __name__ == '__main__':
   pass
