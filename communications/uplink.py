import pigpio
import sys
import serial
import struct
import json

sys.path.append('../core/')
from logger import Logger
from shell import Shell


"""
Class meant for handling uplinking
- Parses uplinked packets into commands
- Sends these commands to the shell to execute
"""

class Uplinker:
    def __init__(self, logger, shell, pi):
        self.logger = logger
        self.shell = shell
        self.packets = []
        self.pi = pi

    def get_packets(self):
        handler = self.pi.serial_open("/dev/ttyUSB1", 19200, 0)

        while True:
            # Assuming each packet is 90 bytes long
            total_bytes, data = self.pi.serial_read(handler, 90)
            
            if total_bytes > 0:
                # If total bytes read in are greater than zero
                # WARN might have issue with json.loads
                self.packets.append(json.loads(data))
            else:
                break
		
        self.pi.serial_close(handler)
        

    def parse_packets(self):
        # TODO Add better exceptions
        line = []
        i = 0
        try:
            for packet in self.packets:
                if packet['num'] == 0 or packet['num'] == i:
                    pass
                else:
                    raise ValueError
                line.append(packet['cmd'])
                i += 1
        
        except(ValueError):
            return "echo Error"
        
        return "".join(line)

    def exec_cmd(self):
        self.shell.exec_shell_cmd(self.parse_packets())