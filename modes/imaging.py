import sys
sys.path.append('../communications/')

from image_processing import Image_Processor

sys.path.append('../core/')
from logger import Logger

class Imaging_Mode:
    def __init__(self, processor, logger):
        self.processor = processor
        self.image_name = ""
        self.logger = logger
    
    def stabilize(self):
        # stabilizing algorithm with MRW and magnetorquers
        # TODO: Need to develop this algorithm
        return True
    
    def point(self):
        # pointing algorithm with MRW and magnetorquers
        # TODO: Need to develop this algorithm
        return True
    
    def click_image(self):
        # code to interface with the raspberry pi and take the image
        # TODO: Need to get this code from electrical
        self.image_name = "test"
        return self.image_name
    
    def queue_image(self):
        # Code will automatically add image to the queue
        self.processor.add_image(self.image_name)

    def downlink(self):
        # Need to have master downlink capability
        # TODO: Need to develop this class
        return True


if __name__ == "__main__":
    logger = Logger()
    processor_ = Image_Processor(logger)
    mode = Imaging_Mode(processor_, logger)    

