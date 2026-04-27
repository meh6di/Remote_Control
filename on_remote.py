import cv2
import socket
import pickle
import struct

# Connect to your PC's Tailscale IP
PC_TAILSCALE_IP = '100.x.y.z'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PC_TAILSCALE_IP, 8089))

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)
    # Send message length first, then frame
    message = struct.pack("Q", len(data)) + data
    client_socket.sendall(message)
