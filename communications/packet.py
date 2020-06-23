"""
Class meant for the definition of a packet
"""

class Packet:
    def __init__(self, img_data, tel_data, log_data, num):
        self.img_data = img_data
        self.tel_data = tel_data
        self.log_data = log_data
        self.num = num

    def __repr__(self):
        num_str = ""
        img_str = ""
        tel_str = ""
        log_str = ""

        if self.num:
            num_str = "num:" + str(self.num) 
        if self.img_data:
            img_str = ",img:" + (self.img_data).decode('utf-8')
        if self.tel_data:
            tel_str = ",tel:" + str(self.tel_data)
        if self.log_data:
            log_str = ",log:" + (self.log_data).decode('utf-8')

        return  num_str + img_str + tel_str + log_str 