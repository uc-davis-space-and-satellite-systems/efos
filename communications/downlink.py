import pigpio
import json
import base64
import struct

from packing import Packing

"""
Class meant for handling downlink
- Parses dowlink data into binary packets
- Sends this data through the antenna to Earth
"""

class Downlinker:
	def __init__(self, logger, pi):
		self.pi = pi
		self.logger = logger
		self.data = {}
		self.packets = []

	# Adding an image to the downlink data
	def add_image(self, img_name):
        # Convert image to a base64 string and add it to the downlink data
		img_b64 = base64.encodestring(open(img_name,"rb").read())

		if 'img' in self.data:
            # If there is an image already in the data, add another one in a list
			self.data['img'].append(img_b64)
		else:
            # If no image, add the image as the first in the list
			self.data['img'] = [img_b64]
    
    # Adding the current logs to the downlink data
	def add_logs(self, log_file_name):
        # Opening the specified log file
        log_file = open(log_file_name)

        if 'log' in self.data:
            # If there is an log already in the data, add another one in a list
            self.data['log'] += "\n" + log_file.read()
        else:
            # If no log, add the log as the first in the list
            self.data['log'] = log_file.read()

        # Closing the specified log file
        log_file.close()

	# Automatically adds telemetry before it flushes the data
	def add_telemetry(self, telemetry):
        for tel in telemetry:
            if 'tel' in self.data:
                self.data['tel'].append(tel)
            else:
                self.data['tel'] = [tel]

    # Package the current data into 90-byte packets
	def package(self):
		package = Packing(self.data)
		self.packets = package.pack()

    # Flush this data from the pi to the serial ports
	def flush(self):
		# Writes the downlink to the serial port and sends it over

		h2 = self.pi.serial_open("/dev/ttyUSB1", 19200, 0)
		for packet in self.packets:
			self.pi.serial_write(h2, repr(packet))
		
		self.pi.serial_close(h2)




