import pigpio
import json
import base64

RX_PIN = 1
TX_PIN = 0

class Downlinker:
	def __init__(self, pi):
		self.pi = pigpio.pi()
		self.data = {}
	
	# Adding a msg to the downlink data
	def add_msg(self, msg):
		if 'msgs' in self.data:
			self.data['msgs'].append(msg)
		else:
			self.data['msgs'] = [msg]
		
		return True

	# Adding an image to the downlink data
	def add_image(self, img_name):
		img_b64 = base64.encodestring(open(img_name,"rb").read())
		if 'imgs' in self.data:
				self.data['imgs'].append(img_b64)
		else:
				self.data['imgs'] = [img_b64]
		
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




