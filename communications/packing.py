"""
Class meant for packaging data into packets
- Parses data into binary packets
"""
from packet import Packet

import time

class Packing:
    def __init__(self, data):
        self.data = data
    
    def pack(self):
        # Package given data into small packets
        tel_offset = 0
        log_offset = 0
        packet_num = 0
        img_offset = 0

        img_flag = False
        tel_flag = False
        log_flag = False

        packets = []

        while True:
            # 20 bytes of image data
            img_data = None
            tel_data = None
            log_data = None

            if img_offset < len(self.data['img']):
                if img_offset + 20 < len(self.data['img']):
                    img_data = self.data['img'][img_offset: img_offset + 20]
                else:
                    img_data = self.data['img'][img_offset: ]
                    img_flag = True

                img_offset += 20

            # Reading one array of telemetry data
            if tel_offset < len(self.data['tel']):
                tel_data = self.data['tel'][tel_offset]
            else:
                tel_flag = True

            tel_offset += 1

            if log_offset < len(self.data['log']):
                # 8 bytes of log data
                if log_offset + 8 < len(self.data['log']):
                    log_data = self.data['log'][log_offset: log_offset+8].encode('utf-8')
                else:
                    log_data = self.data['log'][log_offset:].encode('utf-8')
                    log_flag = True
                log_offset += 8

            packets.append(Packet(img_data, tel_data, log_data, packet_num))
            packet_num += 1
            
            if tel_flag and log_flag and img_flag:
                break


   
        return packets