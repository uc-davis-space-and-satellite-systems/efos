import sys
import os

sys.path.append('../core/')
from logger import Logger

class Shell:
    def __init__(self, logger):
        self.logger = logger

    # Executes a given command
    def exec_shell_cmd(self, line):
        self.logger.info("Executing shell command -> " + line)
        os.system(line)
