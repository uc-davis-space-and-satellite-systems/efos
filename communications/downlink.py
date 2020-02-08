import pigpio
import json

RX_PIN = 1
TX_PIN = 0

class Downlinker:
	def __init__(self, pi):
		self.pi = pigpio.pi()
		self.data = []
	
	def add_msg(self, msg):
		# Adding a msg to the downlink data
		# TODO: Write code to add the msg to data
		return True
	
	def add_image(self, img_name):
		# Adding an image to the downlink data
		# TODO: Write code to translate the image to a byte stream and add to data
		return True
	
	def add_logs(self, log_file_name):
		# Automatically adds logs before flushing the data
		# TODO: Write logs to the data
		return True
	
	def add_telemetry(self):
		# Automatically adds telemetry before it flushes the data
		# TODO: Need to define (or learn what telemetry is)
		return True
	
	def flush(self):
		# Writes the downlink to the TX pin and sends it over
		# TODO: Algorithm needs to be developed
		return True
	



