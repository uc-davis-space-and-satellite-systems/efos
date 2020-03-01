import pigpio
import sys

sys.path.append('../core/')
from logger import Logger
from shell import Shell

sys.path.append('../control_systems/')
from bdot import BDot
from esc import ESC

sys.path.append('../determination/')
from mpu9250 import MPU9250

sys.path.append('../communications/')
from downlink import Downlinker
from uplink import Uplinker
from image_processing import Image_Processor

sys.path.append('../modes/')
from imaging import Imaging_Mode
from priming import Priming_Mode


class FOS:
    def __init__(self, pi, logger, shell, uplinker, downlinker, image_processor, esc, mpu9250):
        # Core
        self.pi = pi
        self.logger = logger
        self.shell = shell

        # Communications
        self.uplinker = uplinker
        self.downlinker = downlinker
        self.image_processor = image_processor

        # Control Systems
        self.esc = esc

        # Determination
        self.mpu9250 = mpu9250

        # Modes
        self.priming_mode = Priming_Mode(self.esc)
        self.imaging_mode = Imaging_Mode(self.image_processor)

        self.modes = [self.priming_mode, self.imaging_mode]

        # Initialize it to be set to the priming mode
        self.current_mode = 0 

    def shift_mode(self, mode):
        self.current_mode = self.modes[mode]
    


if __name__ == "__main__":
    # Core Stuff
    pi = pigpio.pi()
    logger = Logger()
    shell = Shell()

    uplinker = Uplinker(logger, shell, pi)
    downlinker = Downlinker(logger, pi)
    image_processor = Image_Processor(logger)

    esc = ESC()
    mpu9250 = MPU9250(pi)

    fos = FOS(pi, logger, shell, uplinker, downlinker, image_processor, esc, mpu9250)