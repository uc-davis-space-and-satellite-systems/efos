import sys
import base64

sys.path.append("../../../communications/")
from packet import Packet
from packing import Packing

# Creating the Data
data = {}

data['img'] = base64.encodebytes(open('test_data/img.png',"rb").read())
data['tel'] = [[0, 90, 100, 380, 394], [0, 0, 0, 38, 94], [0, 60, 130, 350, 254]]
data['log'] = "This is some test text that I am inputting for this test program"

packets = Packing(data).pack()

# Printing image data
for packet in packets:
    print(packet.img_data.decode('utf-8'), end="")
print()
