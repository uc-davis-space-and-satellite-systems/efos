import image_slicer
import numpy
import cv2

"""
Class meant for processing images
- Queues images by how percentage of darkness
- Splits images into 16 'tiles' and sends each tile one by one,
  taking care that all tiles sent are of one image at a time.
"""

class Image_Processor:
    def __init__(self, logger):
        self.image_queue = []
        self.tile_queue = []
        self.logger = logger
        
        self.logger.debug("Initializing the Image Processor")

    # This is a helper function to sort a list of tuples
    # by its second value
    def sort_tuple_list_(self, tup):
        tup.sort(key = lambda x: x[1])  
        return tup  

    # This functions takes in the filename of the image and
    # Returns the percent of dark pixels in it
    def image_black_percentage(self, img_name):
        image = cv2.imread(img_name, 0)
        self.logger.debug("Reading Image: " + img_name)
        count = sum(image[image < 20])
        size = sum(image[image <= 255])
        percent = count/size * 100

        self.logger.debug("Image " + img_name + " black percentage is " + str(percent))

        return percent

    # This function uses the image_slicer library to split the 
    # image into the number of parts we need
    def image_splitting(self, img_name):
        self.logger.debug("Splitting the image into 16")
        image_slicer.slice(img_name, 16)
        
        self.logger.debug("Splitting done")

    # Adds an image to the queue
    def add_image(self, img_name):
        # Get the percentage of darkness of image
        percent = self.image_black_percentage(img_name)

        # Add this image to the priority queue
        self.logger.info("Adding image and sorting the queue")
        
        self.image_queue.append((img_name, percent))
        self.sort_tuple_list_(self.image_queue)


    # Sends the next tile from the queue
    def send_next_tile(self):
        if not self.tile_queue:
            try:
                if not self.image_queue:
                    raise ValueError
                img_name = self.image_queue[0][0]
                self.image_splitting(img_name)
                for i in range(1,5):
                    for j in range(1,5):
                        self.tile_queue.append(img_name[:-2] + "_0" + str(i) + "_0" + 
                        str(j) + img_name[-3:])
                
            except ValueError:
                self.logger.warning("Image Queue is empty")
    
        ret_tile = self.tile_queue[0]
        self.tile_queue = self.tile_queue[1:-1]
        return ret_tile
