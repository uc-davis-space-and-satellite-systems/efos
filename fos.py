import time, pysnooper
import utils, triad
from mpu9250 import MPU9250

def main():
    imu = MPU9250() # initialize mpu9250

    while True:
        imu.update_acc_reading() # update acc values
        imu.update_mag_reading() # update mag values

        acc_meas_raw = [imu.acc_x, imu.acc_y, imu.acc_z]
        mag_meas_raw = [imu.mag_x, imu.mag_y, imu.mag_z]

        # TODO don't recreate numpy array every time, heavy computation
        acc_meas = utils.to_unit_vector(acc_meas_raw) # acc unit vector
        mag_meas = utils.to_unit_vector(mag_meas_raw) # mag unit vector

        acc_ref = np.array([0.0, 0.0, -1.0]) # acc ref vector
        mag_ref = np.array([1.0, 0.0, 0.0]) # mag ref vector

        rotation = triad.triad(acc_meas, mag_meas, acc_ref, mag_ref)

        print("Acc:", acc_meas, "Mag:", mag_meas, "Rot:", rotation)

        time.sleep(0.1)

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    main() # begin main loop
