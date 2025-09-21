"""
Security IoT System - Motion Detection with Ultrasonic Sensor
============================================================

This system detects motion using an ultrasonic sensor and triggers:
- LED alarm blinking when motion is detected
- Blynk platform notifications for distance and alarm status
- Camera capture signal to server when motion is detected

Hardware:
- Raspberry Pi
- Ultrasonic sensor (HC-SR04) connected to GPIO pins 14 (echo) and 15 (trigger)
- LED connected to GPIO pin 13
"""

import BlynkLib
from gpiozero import LED, DistanceSensor
import time
import socket
import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

# Hardware pins
ULTRASONIC_ECHO_PIN = 14
ULTRASONIC_TRIGGER_PIN = 15
LED_PIN = 13

# Motion detection threshold (in centimeters)
MOTION_THRESHOLD = 20.0

# Blynk configuration
BLYNK_AUTH_TOKEN = "p9p35YSnwBZFiHwVaTbKpruU3UgGdkGi"
BLYNK_SERVER = "blynk.cloud"
BLYNK_PORT = 443

# Server connection settings
SERVER_IP = "192.168.137.77"
SERVER_PORT = 5000

# Data logging
LOG_FILE = "../data/distance_log.csv"
LOG_INTERVAL = 1.0  # seconds

# =============================================================================
# SETUP
# =============================================================================

# Initialize hardware
sensor = DistanceSensor(echo=ULTRASONIC_ECHO_PIN, trigger=ULTRASONIC_TRIGGER_PIN)
led = LED(LED_PIN)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN, server=BLYNK_SERVER, port=BLYNK_PORT)

# Initialize log file with headers
def initialize_log_file():
    """Initialize the CSV log file with headers if it doesn't exist."""
    try:
        with open(LOG_FILE, "a") as f:
            if f.tell() == 0:
                f.write("Time,Distance(cm),Status\n")
                print("Log file initialized with headers")
    except Exception as e:
        print(f"Failed to initialize log file: {e}")

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def send_data_to_blynk(distance: float):
    """
    Send distance data and alarm status to Blynk platform.
    
    Args:
        distance (float): Distance measurement in centimeters
    """
    try:
        # Send distance to virtual pin 0
        blynk.virtual_write(0, distance)
        print("Distance:", distance)
        
        # Send alarm status to virtual pin 1
        alarm_status = 1 if distance < MOTION_THRESHOLD else 0
        blynk.virtual_write(1, alarm_status)
        
    except Exception as e:
        print("Error:", e)

def log_distance_data(distance: float) -> None:
    """
    Log distance measurement and safety status to CSV file.
    
    Args:
        distance (float): Distance measurement in centimeters
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "NOT SAFE" if distance < MOTION_THRESHOLD else "SAFE"
        
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp},{distance:.2f},{status}\n")
        
        print(f"Logged: {timestamp} | {distance:.2f} cm | {status}")
        
    except Exception as e:
        print(f"Failed to log distance data: {e}")

def send_camera_capture_signal():
    """
    Send signal to server to trigger camera capture.
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # 5 second timeout
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(b"capture")
        print("Signal sent to laptop to capture image.")
        return True
    except Exception as e:
        print("Failed to send signal to laptop:", e)
        return False
    finally:
        if s:
            s.close()

def control_led_alarm(distance: float):
    """
    Control LED alarm based on distance measurement.
    
    Args:
        distance (float): Distance measurement in centimeters
    """
    if distance < MOTION_THRESHOLD:
        # Blink LED when motion detected
        now = time.time()
        if int(now * 2) % 2 == 0:
            led.on()
        else:
            led.off()
    else:
        led.off()

def read_distance() -> float:
    """
    Read distance from ultrasonic sensor.
    
    Returns:
        float: Distance in centimeters
    """
    try:
        distance = sensor.distance * 100  # Convert from meters to centimeters
        return max(0, distance)  # Ensure non-negative distance
    except Exception as e:
        print(f"Failed to read distance: {e}")
        return 0.0

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution loop for the security system."""
    print("Security IoT System started")
    print(f"Motion threshold: {MOTION_THRESHOLD} cm")
    print(f"Server: {SERVER_IP}:{SERVER_PORT}")
    
    # Initialize log file
    initialize_log_file()
    
    # Timing variables
    last_log_time = time.time()
    last_camera_signal_time = 0
    camera_signal_cooldown = 5.0  # Minimum seconds between camera signals
    
    try:
        while True:
            # Run Blynk communication
            blynk.run()
            
            # Read distance from sensor
            distance = read_distance()
            
            # Control LED alarm
            control_led_alarm(distance)
            
            # Send camera capture signal if motion detected
            if distance < MOTION_THRESHOLD:
                current_time = time.time()
                if current_time - last_camera_signal_time > camera_signal_cooldown:
                    if send_camera_capture_signal():
                        last_camera_signal_time = current_time
            
            # Log and send data at regular intervals
            current_time = time.time()
            if current_time - last_log_time >= LOG_INTERVAL:
                send_data_to_blynk(distance)
                log_distance_data(distance)
                last_log_time = current_time
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Security system stopped by user")
    except Exception as e:
        print(f"Unexpected error in main loop: {e}")


if __name__ == "__main__":
    main()
