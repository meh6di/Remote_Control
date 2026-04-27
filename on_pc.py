import cv2
import socket
import numpy as np
from pyexpat import model

# --- CONFIGURATION ---
REMOTE_IP = "100.x.y.z"  # Listen on all interfaces (including Tailscale)
CMD_PORT = 5006
cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 1. Setup UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((REMOTE_IP, CMD_PORT))


print(f"PC Receiver started. Listening on {REMOTE_IP}:{CMD_PORT}...")

while True:
    # 2. Receive packet
    data, addr = sock.recvfrom(65507)

    # 3. Decode packet back into a frame
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # 'frame' is now defined for AI!

    if frame is not None:
        # Code D'IA
        results = model(frame)

        # Example: If AI detects an object, send a command back
        if results.detected:
            # Use a separate socket or API call to the remote device's IP
            for r in results:
                for box in r.boxes:
                    # 1. Get box coordinates (x1, y1, x2, y2)
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    # 2. Calculate Center Coordinates
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)

                    # 3. Send to Remote Device
                    # Format: "X,Y"
                    message = f"{center_x},{center_y}"
                    cmd_sock.sendto(message.encode(), (REMOTE_IP, CMD_PORT))

        cv2.imshow("AI Processing Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cv2.destroyAllWindows()