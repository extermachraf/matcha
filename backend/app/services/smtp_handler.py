import resend
from flask import current_app

def send_verification_email(recipient_email: str, verification_url: str):
    """
    Sends the verification link using the Resend API.
    """
    app = current_app._get_current_object()
    
    # Initialize Resend with the API Key from Flask Config
    # Resend automatically looks for resend.api_key if not passed in the constructor
    # We set it globally for simplicity inside the function.
    resend.api_key = app.config.get('RESEND_API_KEY')
    # Define the email parameters
    params: resend.Emails.SendParams = {
        # CRITICAL: Use your verified domain/sender here.
        "from": "Acme <onboarding@resend.dev>", 
        "to": [recipient_email],
        "subject": "Matcha Account Verification Required",
        "html": f"""
            <strong>Welcome to Matcha!</strong><br><br>
            Please click the link below to verify your account:<br><br>
            <a href="{verification_url}">Verify My Account</a><br><br>
            This link is valid for 1 hour.
        """,
    }
    
    try:
        email = resend.Emails.send(params)
        print(f"✅ Resend success. Email ID: {email['id']}")
        return True
    except getattr(resend, 'exceptions', Exception).ResendError as e:
        # Resend raises ResendError on API problems; handle it explicitly.
        # Use getattr above to avoid attribute errors if the package layout differs.
        print(f"❌ Resend API Error: {getattr(e, 'status_code', 'N/A')} - {getattr(e, 'message', str(e))}")
        # In production, you would want to log this and potentially retry.
        return False
    except Exception as e:
        print(f"❌ Unknown Error sending email via Resend: {e}")
        return False
    
def send_password_reset_email(recipient_email: str, reset_url: str):
    """
    Sends the password reset link using the Resend API.
    """
    app = current_app._get_current_object()
    
    # Initialize Resend with the API Key from Flask Config
    resend.api_key = app.config.get('RESEND_API_KEY')
    
    # Define the email parameters
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [recipient_email],
        "subject": "Matcha Password Reset Request",
        "html": f"""
            <strong>Password Reset Request</strong><br><br>
            We received a request to reset your password. Click the link below to proceed:<br><br>
            <a href="{reset_url}">Reset My Password</a><br><br>
            If you did not request this, please ignore this email.<br><br>
            This link is valid for 1 hour.
        """,
    }
    
    try:
        email = resend.Emails.send(params)
        print(f"✅ Resend success. Email ID: {email['id']}")
        return True
    except getattr(resend, 'exceptions', Exception).ResendError as e:
        print(f"❌ Resend API Error: {getattr(e, 'status_code', 'N/A')} - {getattr(e, 'message', str(e))}")
        return False
    except Exception as e:
        print(f"❌ Unknown Error sending email via Resend: {e}")
        return False