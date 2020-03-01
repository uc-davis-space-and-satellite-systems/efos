import logging
import logging.config
import json

class Logger:
    def __init__(self, log_level):
        logging.config.fileConfig('../config/logging_config.ini')
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level
        self.log_data = []

    def debug(self, msg):
        # Wrapper function for debug logging
        self.logger.debug(msg)
    
    def warning(self, msg):
        # Wrapper function for warning logging
        self.logger.warning(msg)

    def info(self, msg):
        # Wrapper function for info logging
        self.logger.info(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def flush(self):
        return True

"""
Test Code
if __name__ == "__main__":
    logger = Logger(10)
    logger.debug("HI")    
"""