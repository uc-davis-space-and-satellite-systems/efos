import pigpio, time
import sys

sys.path.append('../core/')
from logger import Logger
from shell import Shell

sys.path.append("../determination/")
from mpu9250 import MPU9250

class BDot:
    def __init__(self, pi, mpu9250, k, num_of_windings, surface_area):
        self.k = k
        self.num_of_windings = num_of_windings
        self.surface_area = surface_area
        self.pi = pi
        self.mpu9250 = mpu9250

        self.rate_x = 0
        self.rate_y = 0
        self.rate_z = 0

        self.last_x = 0
        self.last_y = 0
        self.last_z = 0

        self.current_x = 0
        self.current_y = 0
        self.current_z = 0

        while True:
            self.update_rate()
            self.update_current()
            self.apply_current()

    def update_rate(self):
        self.mpu9250.update_mag_reading()

        self.rate_x = self.mpu9250.mag_x - self.last_x
        self.rate_y = self.mpu9250.mag_y - self.last_y
        self.rate_z = self.mpu9250.mag_z - self.last_z

        self.last_x = self.mpu9250.mag_x
        self.last_y = self.mpu9250.mag_y
        self.last_z = self.mpu9250.mag_z

        time.sleep(0.01)

    def update_current(self):
        self.current_x = (self.k * self.rate_x)/(self.num_of_windings * self.surface_area)
        self.current_y = (self.k * self.rate_y)/(self.num_of_windings * self.surface_area)
        self.current_z = (self.k * self.rate_z)/(self.num_of_windings * self.surface_area)

    def apply_current(self):
        # TODO Add raspi code to add current to the magnetorquers
        return True


if __name__ == "__main__":
    # K value of BDot algorithm
    k = 0
    # Number of coil windings
    num_of_windings = 1
    # Surface area of torquerod/coil
    surface_area = 1.0

    pi = pigpio.pi()
    mpu = MPU9250(pi)

    bdot = BDot(pi, mpu, k, num_of_windings, surface_area)
