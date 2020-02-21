import pigpio

sys.path.append('../core/')
from logger import Logger

class Uplink_Handler:
    # TODO: Class still needs definition

    def __init__(self, logger, shell):
        self.logger = logger
        self.shell = shell

    def parse_line(self, line):
        self.shell.exec_shell_cmd(line)