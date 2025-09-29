import time
import os

LOG_FILE = "predictions.log"
ERROR_THRESHOLD = 2  # Trigger alert if more than 2 errors are found

def monitor_logs():
    print("Monitoring logs...")
    while True:
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    lines = f.readlines()
                    error_count = sum(1 for line in lines if "ERROR" in line)

                    if error_count > ERROR_THRESHOLD:
                        print(f"\nALERT! High error rate detected: {error_count} errors found in logs.")
                        print("This would trigger a notification to Slack/Email.\n")

                        # Optional: Clear the log to reset the alert
                        # open(LOG_FILE, 'w').close()
            else:
                print(f"Log file '{LOG_FILE}' not found. Waiting...")

        except Exception as e:
            print(f"An error occurred during monitoring: {e}")

        time.sleep(10) # Check every 10 seconds

if __name__ == "__main__":
    monitor_logs()