import socket
import cv2
import datetime
import os

HOST = "0.0.0.0"
PORT = 5000

# Create captures directory
if not os.path.exists("captures"):
    os.makedirs("captures")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("Waiting for Pi signal...")

try:
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024).decode()
        if data == "capture":
            print("Signal received! Taking picture...")
            cam = cv2.VideoCapture(0)  # default laptop webcam
            ret, frame = cam.read()
            if ret:
                filename = f"captures/capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                print("Saved:", filename)
            cam.release()
        conn.close()
except KeyboardInterrupt:
    print("Server stopped by user")
    s.close()