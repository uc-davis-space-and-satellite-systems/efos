import pigpio
import sys
import serial
import struct

sys.path.append('../core/')
from logger import Logger
from shell import Shell

class Uplinker:
    def __init__(self, logger, shell, pi):
        self.logger = logger
        self.shell = shell
        self.packets = []
        self.pi = pi

    def get_packets(self):
        # TODO Need to add raspi code for getting packets
        return True

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


"""
Testing code
if __name__ == "__main__":
    logger = Logger()
    shell = Shell(logger)
    uplinker = Uplink_Handler(logger, shell)

    uplinker.get_packets()
    uplinker.parse_packets()
    uplinker.exec_cmd()
"""
