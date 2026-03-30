import os
import requests
import traceback

def send_otp_email(email, otp_code):
    """
    Sends an OTP email using the Brevo (Sendinblue) API.
    Reference Working Logic applied.
    """
    url = "https://api.brevo.com/v3/smtp/email"
    
    api_key = os.environ.get("BREVO_API_KEY")
    # Using the verified sender provided in the reference
    sender_email = os.environ.get("BREVO_SENDER") or "dhanishkanth1122@gmail.com"
    
    subject = "Your Login OTP"
    html_content = f"<h2>Your WebOS Authentication OTP is: {otp_code}</h2><p>This code will expire in 5 minutes.</p>"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    data = {
        "sender": {"email": sender_email},
        "to": [{"email": email}],
        "subject": subject,
        "htmlContent": html_content
    }

    print("DEBUG → BREVO_API_KEY:", "FOUND" if api_key else "MISSING (None)")
    print("DEBUG → BREVO_SENDER:", sender_email)
    print("DEBUG → RECEIVER EMAIL:", email)

    try:
        print("DEBUG → Sending request to Brevo API...")
        response = requests.post(url, json=data, headers=headers)
        
        # Brevo returns 201 for success
        print(f"BREVO RESPONSE [{response.status_code}]: {response.text}")
        
        return response.status_code == 201
            
    except Exception as e:
        print("🔥 BREVO ERROR (Exception in send_otp_email):")
        traceback.print_exc()
        return False
