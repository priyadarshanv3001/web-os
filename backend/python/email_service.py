import requests
import os

def send_otp_email(email, otp_code):
    """
    Sends an OTP email using the Brevo (Sendinblue) API.
    """
    api_key = os.environ.get("BREVO_API_KEY")
    sender_email = os.environ.get("BREVO_SENDER")

    print("DEBUG → BREVO_API_KEY:", "FOUND" if api_key else "MISSING (None)")
    print("DEBUG → BREVO_SENDER:", sender_email)
    print("DEBUG → RECEIVER EMAIL:", email)

    if not api_key:
        print("ERROR: BREVO_API_KEY IS MISSING IN ENVIRONMENT")
        return False
        
    if not sender_email:
        print("ERROR: BREVO_SENDER IS MISSING IN ENVIRONMENT")
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    data = {
        "sender": {"email": sender_email},
        "to": [{"email": email}],
        "subject": "Your Login OTP",
        "htmlContent": f"<h2>Your WebOS Authentication OTP is: {otp_code}</h2><p>This code will expire in 5 minutes.</p>"
    }

    try:
        print("DEBUG → Sending request to Brevo API...")
        response = requests.post(url, json=data, headers=headers)
        print("BREVO RESPONSE:", response.status_code, response.text)
        
        # Return True for 200/201 (Success)
        return response.status_code in [200, 201]
            
    except Exception as e:
        import traceback
        print("🔥 EXCEPTION IN send_otp_email:")
        traceback.print_exc()
        return False
