import time, pysnooper
import utils
from mpu9250 import MPU9250

def main():
    imu = MPU9250() # initialize mpu9250
    imu.update_mag_axis_sensitivity() # fix mag sensitivity

    while True:
        imu.update_acc_reading() # update acc values
        imu.update_mag_reading() # update mag values

        acc_meas_raw = [imu.acc_x, imu.acc_y, imu.acc_z]
        mag_meas_raw = [imu.mag_x, imu.mag_y, imu.mag_z]

        # TODO don't recreate numpy array every time, heavy computation
        acc_meas = utils.to_unit_vector(acc_meas_raw) # acc unit vector
        mag_meas = utils.to_unit_vector(mag_meas_raw) # mag unit vector

        time.sleep(0.05)

if __name__ == "__main__":
    main() # begin main loop
