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
    for x in range(0, 100):
        data = {
            "accx": round(random.random()*100, 2),
            "accy": round(random.random()*100, 2),
            "accz": round(random.random()*100, 2),
            "magx": round(random.random()*100, 2),
            "magy": round(random.random()*100, 2),
            "magz": round(random.random()*100, 2),
            "gyrx": round(random.random()*100, 2)
        }
        data = json.dumps(data)
    sock.sendall(bytes(data + "\n", "utf-8"))
        
print("Sent:     {}".format(data))