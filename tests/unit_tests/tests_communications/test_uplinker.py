import sys
import pigpio


sys.path.append('../../../core/')
from logger import Logger
from shell import Shell

sys.path.append('../../../communications/')
from uplink import Uplinker


# Testing code
if __name__ == "__main__":
    logger = Logger(1)
    shell = Shell(logger)
    pi = pigpio.pi()
    uplinker = Uplinker(logger, shell, pi)

    # Can't test get_packets
    uplinker.packets.append({'num':0, 'cmd':'echo All cool'})
    uplinker.parse_packets()
    uplinker.exec_cmd()
