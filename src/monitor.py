import time
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LOG_FILE = "predictions.log"
ERROR_THRESHOLD = 2  # Trigger alert if more than 2 errors are found
ALERT_COOLDOWN_SECONDS = 300 # Wait 5 minutes before sending another alert

# Get credentials from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_alert_email(error_count):
    """Sends an email notification about the high error rate."""
    
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("ERROR: Missing email credentials in .env file. Cannot send email.")
        return

    subject = "ALERT: High Error Rate Detected in MLOps Pipeline"
    body = f"""
    Warning,

    The monitoring script has detected a high number of errors in the prediction logs.

    Error Count: {error_count}
    Threshold: {ERROR_THRESHOLD}

    Please check the application logs for more details.
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        print("Alert condition met. Sending email...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


def monitor_logs():
    """Monitors the log file and triggers an email alert if the error threshold is exceeded."""
    print("Monitoring logs... Press Ctrl+C to stop.")
    last_alert_time = 0
    
    while True:
        try:
            current_time = time.time()
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    lines = f.readlines()
                    error_count = sum(1 for line in lines if "ERROR" in line)
                    
                    if error_count > ERROR_THRESHOLD:
                        if (current_time - last_alert_time) > ALERT_COOLDOWN_SECONDS:
                            send_alert_email(error_count)
                            last_alert_time = current_time
                            open(LOG_FILE, 'w').close()
                        else:
                            print(f"Alert condition met ({error_count} errors), but in cooldown period. No email sent.")
            
            time.sleep(10)  # Check every 10 seconds

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred during monitoring: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_logs()