from flask import Blueprint, request, jsonify
from models import db, User, OTP, verify_and_clear_otp
from email_service import send_otp_email
import random
from datetime import datetime, timedelta
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/send-otp', methods=['POST'])
def handle_send_otp():
    print("🚀 ROUTE HIT: /api/auth/send-otp")
    try:
        data = request.get_json(force=True, silent=True)
        print("DATA RECEIVED:", data)

        if not data:
            print("ERROR: No JSON data received or invalid format")
            return jsonify({"success": False, "error": "Invalid request - No JSON data"}), 400

        reg_number = data.get('registration_number')
        email = data.get('email')
        print("REG NUMBER:", reg_number)
        print("EMAIL:", email)

        if not reg_number or not email:
            print("ERROR: Missing reg_number or email")
            return jsonify({"success": False, "error": "Registration number and email are required"}), 400

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        print("OTP GENERATED:", otp_code)
        
        expires = datetime.utcnow() + timedelta(minutes=5)
        
        # Save to db
        new_otp = OTP(email=email, code=otp_code, expires_at=expires)
        db.session.add(new_otp)
        db.session.commit()
        print("DB SUCCESS: OTP saved")

        # Send email
        print("---- SENDING EMAIL VIA BREVO ----")
        success = send_otp_email(email, otp_code)
        print("EMAIL SENT STATUS:", success)
        
        if success:
            return jsonify({
                "success": True,
                "message": "OTP sent"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Failed to send OTP via Brevo API. Check backend logs."
            }), 500

    except Exception as e:
        print("🔥 FULL ERROR TRACEBACK:")
        traceback.print_exc()   # THIS IS THE KEY LINE
        return jsonify({
            "success": False,
            "error": f"Backend crash: {str(e)}"
        }), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def handle_verify_otp():
    data = request.json
    reg_number = data.get('registration_number')
    email = data.get('email')
    code = data.get('otp')

    if not all([reg_number, email, code]):
        return jsonify({"error": "Missing required fields"}), 400

    is_valid = verify_and_clear_otp(email, code)

    if is_valid:
        # Auth successful, login or register user
        user = User.query.filter_by(registration_number=reg_number).first()
        
        # Check if email is already used by another account
        existing_email_user = User.query.filter_by(email=email).first()
        if existing_email_user and (not user or existing_email_user.id != user.id):
            return jsonify({"error": "This email is already associated with a different registration number."}), 400

        if not user:
            # Register them
            user = User(registration_number=reg_number, email=email)
            db.session.add(user)
            db.session.commit()
        else:
            if user.email != email:
                user.email = email
                db.session.commit()

        # Returning user details. In a real app, generate a JWT token here.
        return jsonify({"message": "Authentication successful", "user_id": user.id}), 200
    else:
        return jsonify({"error": "Invalid or expired OTP"}), 401
