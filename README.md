# Security IoT System

A motion detection security system using Raspberry Pi with ultrasonic sensor, LED alarm, Blynk integration, and camera capture functionality.

## Features

- **Motion Detection**: Uses ultrasonic sensor (HC-SR04) to detect objects within 20cm
- **LED Alarm**: Blinks LED when motion is detected
- **Blynk Integration**: Sends distance data and alarm status to Blynk cloud platform
- **Camera Capture**: Triggers laptop camera to capture images when motion is detected
- **Data Logging**: Logs all distance measurements and safety status to CSV file
- **Robust Error Handling**: Comprehensive error handling and logging throughout

## Hardware Requirements

### Raspberry Pi
- Ultrasonic sensor (HC-SR04) connected to GPIO pins 14 (echo) and 15 (trigger)
- LED connected to GPIO pin 13
- Internet connection for Blynk integration

### Laptop/Server
- Webcam for image capture
- Python with OpenCV installed

## Software Requirements

### Raspberry Pi (motion_detector.py)
```bash
pip install BlynkLib gpiozero
```

### Laptop/Server (camera_server.py)
```bash
pip install opencv-python
```

### Install All Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### Motion Detector (motion_detector.py)
Edit the configuration section at the top of the file:

```python
# Hardware pins
ULTRASONIC_ECHO_PIN = 14
ULTRASONIC_TRIGGER_PIN = 15
LED_PIN = 13

# Motion detection threshold (in centimeters)
MOTION_THRESHOLD = 20.0

# Blynk configuration
BLYNK_AUTH_TOKEN = "your_blynk_token_here"
BLYNK_SERVER = "blynk.cloud"
BLYNK_PORT = 443

# Server connection settings
SERVER_IP = "your_server_IP_address"
SERVER_PORT = 5000
```

### Camera Server (camera_server.py)
Edit the configuration section:

```python
# Server configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000
```

## Usage

### 1. Start the Camera Server (Laptop)
```bash
cd server
python camera_server.py
```

The server will:
- Create a `captures` directory for storing images
- Listen on port 5000 for capture signals
- Print status messages to console

### 2. Start the Motion Detector (Raspberry Pi)
```bash
cd raspberry_pi
python motion_detector.py
```

The system will:
- Continuously monitor distance using ultrasonic sensor
- Blink LED at 2Hz when motion is detected (distance < 20cm)
- Send data to Blynk platform every second
- Log all measurements to `../data/distance_log.csv`
- Send camera capture signals when motion is detected

## File Structure

```
Security_System/
├── raspberry_pi/
│   └── motion_detector.py    # Main motion detection system (Raspberry Pi)
├── server/
│   ├── camera_server.py      # Camera capture server (Laptop)
│   └── captures/             # Captured images directory (created by server)
├── data/
│   └── distance_log.csv      # Distance measurements log
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md               # This file
```

## Key Improvements Made

### Motion Detector (motion_detector.py)
- Clean, modular function structure
- Implemented camera signal cooldown to prevent spam
- Better resource management with proper cleanup
- LED blinking alarm (2Hz when motion detected)
- Enhanced Blynk integration with error handling

### Camera Server (camera_server.py)
- Simple, direct approach
- Automatic capture directory creation
- Clean error handling
- Minimal dependencies

### Features Added
- **Logging**: Comprehensive logging system for debugging and monitoring
- **Configuration**: Easy-to-modify configuration sections
- **Error Recovery**: Graceful error handling and recovery
- **Resource Management**: Proper cleanup and resource management
- **Documentation**: Clear documentation and comments throughout

## Troubleshooting

### Common Issues

1. **Camera not working**: Check if webcam is available and not used by other applications
2. **Blynk connection failed**: Verify internet connection and Blynk token
3. **Server connection failed**: Ensure both devices are on the same network
4. **GPIO errors**: Check hardware connections and GPIO pin assignments

### Logs
- Monitor console output for real-time system status
- Review `data/distance_log.csv` for historical data
- Check `server/captures/` for captured images

## Credits

This project was developed with contributions from:

- [@salehNassar](https://github.com/salehNassar)
- [@AyaAhmed72](https://github.com/AyaAhmed72)
- [@mohamedabdallah82](https://github.com/mohamedabdallah82)