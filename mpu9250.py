import smbus, time

# USEFUL LINKS
# https://www.invensense.com/wp-content/uploads/2015/02/RM-MPU-9250A-00-v1.6.pdf
# https://www.akm.com/akm/en/file/datasheet/AK8963C.pdf

MPU_ADDRESS          = 0x68              # i2c address (AD0 LOW)
ACCEL_XOUT_H         = 0x3B              # high byte of accelerometer x-axis data
ACCEL_YOUT_H         = 0x3D              # high byte of accelerometer y-axis data
ACCEL_ZOUT_H         = 0x3F              # high byte of accelerometer z-axis data
AK8963_ADDRESS       = 0x0C              # ak8963 slave address
AK8963_HXL           = 0x03              # low byte of magnetometer x-axis data
AK8963_CNTL1         = 0x0A              # control register for changing modes
AK8963_ASAX          = 0x10              # x-axis sensitivity adjustment value
AK8963_PWR_DOWN      = 0x00              # mode for powering down all ak8963 internal circuits
AK8963_FUSE_ROM      = 0x0F              # mode for reading Fuse ROM data; must transition to PWR DOWN mode after
AK8963_CM8HZ         = 0x02              # mode for continuous measuring periodically at 8Hz; no transition to PWR DOWN needed
AK8963_OUTPUT_LENGTH = 0x01              # setting for 16 bit output
AK8963_SCALE_RES     = 4912.0 / 32760.0  # scale resolution for 16 bit (32760) output; 4912 = max magnetic flux density

bus = smbus.SMBus(1) # TODO should this be a class variable?

class MPU9250:
    def __init__(self):
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
        self.mag_x = 0
        self.mag_y = 0
        self.mag_z = 0
        self.mag_x_sensitivity = 0
        self.mag_y_sensitivity = 0
        self.mag_z_sensitivity = 0

        self.enable_passthrough()
        self.init_mag()
        self.update_mag_axis_sensitivity()

    def twos_complement(self, val, num_bits):
        mask_one = 1 << (num_bits - 1)
        mask_two = 1 << num_bits
        if val & mask_one != 0:
            val = val - mask_two
        return val

    def unit_vector(self, x, y, z):
        magnitude = (x**2 + y**2 + z**2)**0.5
        return (x / magnitude, y / magnitude, z / magnitude)

    def read_word(self, subaddress, data):
        high = bus.read_byte_data(subaddress, data)
        low = bus.read_byte_data(subaddress, data + 1)
        word = (high << 8) + low
        return self.twos_complement(word, 16)

    def word(self, low, high):
        return (high << 8) | low

    def enable_passthrough(self):
        bus.write_byte_data(MPU_ADDRESS, 0x6A, 0x00) # disable i2c master controller
        bus.write_byte_data(MPU_ADDRESS, 0x37, 0x02) # enable i2c passthrough

    def init_mag(self):
        self.change_mag_mode(AK8963_PWR_DOWN)
        self.change_mag_mode(AK8963_FUSE_ROM)

    def update_mag_axis_sensitivity(self):
        data = bus.read_i2c_block_data(AK8963_ADDRESS, AK8963_ASAX, 3)
        self.mag_x_sensitivity = 0.5 * (data[0] - 128) / 128.0 + 1.0
        self.mag_y_sensitivity = 0.5 * (data[1] - 128) / 128.0 + 1.0
        self.mag_z_sensitivity = 0.5 * (data[2] - 128) / 128.0 + 1.0
        self.change_mag_mode(AK8963_PWR_DOWN)
        self.change_mag_mode((AK8963_OUTPUT_LENGTH << 4 | AK8963_CM8HZ))

    def change_mag_mode(self, mode):
        data = (AK8963_OUTPUT_LENGTH << 4) | mode
        bus.write_byte_data(AK8963_ADDRESS, AK8963_CNTL1, data)

    def update_mag_reading(self):
        data = bus.read_i2c_block_data(AK8963_ADDRESS, AK8963_HXL, 7)
        x_data = self.twos_complement(self.word(data[0], data[1]), 16)
        y_data = self.twos_complement(self.word(data[2], data[3]), 16)
        z_data = self.twos_complement(self.word(data[4], data[5]), 16)
        self.mag_x = x_data * self.mag_x_sensitivity * AK8963_SCALE_RES
        self.mag_y = y_data * self.mag_y_sensitivity * AK8963_SCALE_RES
        self.mag_z = z_data * self.mag_z_sensitivity * AK8963_SCALE_RES

    def update_acc_reading(self):
        self.acc_x = self.read_word(MPU_ADDRESS, ACCEL_XOUT_H)
        self.acc_y = self.read_word(MPU_ADDRESS, ACCEL_YOUT_H)
        self.acc_z = self.read_word(MPU_ADDRESS, ACCEL_ZOUT_H)

if __name__ == "__main__":
    mpu9250 = MPU9250()

    while True:
        mpu9250.update_acc_reading()
        mpu9250.update_mag_reading()
        print(mpu9250.acc_x, mpu9250.acc_y, mpu9250.acc_z)
        print(mpu9250.mag_x, mpu9250.mag_y, mpu9250.mag_z)
        time.sleep(0.1)
