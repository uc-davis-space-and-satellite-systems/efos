import sys
import base64
import image_compression_native

sys.path.append("../../../communications/")
from packet import Packet
from packing import Packing

# Use earth and moon images for better representation of how the size of the image will change in production
# test_data/moon.png
imagePath = 'test_data/'
imageName = 'moon.jpg'

# The compressed image is saved in the same folder as original image but with 'COMPRESSED' before name
compressedImagePath = image_compression_native.compress_image(path=imagePath, image_name=imageName, quality=30)

# Creating the Data
data = {}

data['img'] = base64.encodebytes(open(compressedImagePath, "rb").read())
data['tel'] = [[0, 90, 100, 380, 394], [0, 0, 0, 38, 94], [0, 60, 130, 350, 254]]
data['log'] = "This is some test text that I am inputting for this test program"

packets = Packing(data).pack()

# Printing image data
for packet in packets:
    print(packet.img_data.decode('utf-8'), end="")
print()
