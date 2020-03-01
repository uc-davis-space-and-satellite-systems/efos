import sys
sys.path.append('../communications/')

from image_processing import Image_Processor

sys.path.append('../core/')
from logger import Logger

class Priming_Mode:
    def __init__(self, logger, esc):
        self.logger = logger
        self.esc = esc

    def exec(self):
        # TODO: Need to develop steps and algorithm for executon
        return True