import logging
import logging.config

class Logger:
    def __init__(self):
        logging.config.fileConfig('../config/logging_config.ini')
        self.logger = logging.getLogger(__name__)

    def debug(self, msg):
        # Wrapper function for debug logging
        self.logger.debug(msg)
    
    def warning(self, msg):
        # Wrapper function for warning logging
        self.logger.warning(msg)

    def info(self, msg):
        # Wrapper function for info logging
        self.logger.info(msg)