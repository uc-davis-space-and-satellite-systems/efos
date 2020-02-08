import sys
import socket
import random
import json
import time

HOST, PORT = "localhost", 9998


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    for x in range(0, 1000):
        data = {
            "acc_x": round(random.random()*100, 2),
            "acc_y": round(random.random()*100, 2),
            "acc_z": round(random.random()*100, 2),
            "mag_x": round(random.random()*100, 2),
            "mag_y": round(random.random()*100, 2),
            "mag_z": round(random.random()*100, 2),
            "triad_x": round(random.random()*100, 2),
            "triad_y": round(random.random()*100, 2),
            "triad_z": round(random.random()*100, 2),
        }
        data = json.dumps(data)
        sock.sendall(bytes(data + "\n", "utf-8"))
        print("Sent:     {}".format(data))
        time.sleep(0.3)
        
