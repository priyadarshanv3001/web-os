import requests
import os

def send_otp_email(email, otp_code):
    """
    Sends an OTP email using the Brevo (Sendinblue) API.
    """
    api_key = os.environ.get("BREVO_API_KEY")
    sender_email = os.environ.get("Bpriyadarshan3001@gmail.com")
    
    if not api_key or not sender_email:
        print(f"[WARNING] BREVO_API_KEY or BREVO_SENDER not set in environment variables.")
        print(f"---------- [DEV MODE LOG] ----------")
        print(f" Simulating sending OTP to: {email}")
        print(f" Simulated OTP Code: {otp_code}")
        print(f"------------------------------------")
        return True

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
        response = requests.post(url, json=data, headers=headers)
        print("BREVO RESPONSE:", response.status_code, response.text)
        
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"Failed to send email via Brevo: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending email via Brevo API: {str(e)}")
        return False
