import socket, json, signal

mission_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    with open("./config/mission_control_config.json", 'r') as f:
        config = json.load(f)
        mission_control_socket.connect((config['host'], config['port']))

def broadcast(acc_meas, mag_meas, rotation):
    data = {
        "acc_x": acc_meas[0],
        "acc_y": acc_meas[1],
        "acc_z": acc_meas[2],
        "mag_x": mag_meas[0],
        "mag_y": mag_meas[1],
        "mag_z": mag_meas[2],
        "triad_x": rotation[0],
        "triad_y": rotation[1],
        "triad_z": rotation[2],
    }

    data = json.dumps(data)
    mission_control_socket.sendall(bytes(data + "\n", "utf-8"))

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    connect()
    broadcast([1, 1, 1], [1, 1, 1], [1, 1, 1])
