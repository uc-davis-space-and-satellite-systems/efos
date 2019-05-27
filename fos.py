import logging, logging.config

# setup logger
logging.config.fileConfig('./config/logging_config.ini')
logger = logging.getLogger(__name__)

import time, signal, json, pysnooper
import numpy as np
import utils, triad
import mission_control as mc
from mpu9250 import MPU9250
from esc import ESC

# configure terminate signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# fetch configuration data
config = None
with open("./config/fos_config.json", 'r') as f:
    config = json.load(f)

# @pysnooper.snoop(depth=1)
def main():
    logger.debug("initializing imu...")
    imu = MPU9250() # initialize mpu9250

    logger.debug("initializing esc...")
    esc_hdd = ESC(config['speed_pin_esc'], config['dir_pin1_esc'], config['dir_pin2_esc'])
    esc_hdd.init_sequence() # initialize hdd esc

    if config['enable_mission_control']:
        logger.info("connecting to mission control server...")
        mc.connect() # connect to mission control server

    logger.info("starting main loop...")

    while True:
        imu.update_acc_reading() # update acc values
        imu.update_mag_reading() # update mag values

        acc_meas_raw = [imu.acc_y * -1, imu.acc_x, imu.acc_z * -1] # fix imu right hand rule
        mag_meas_raw = [imu.mag_x, imu.mag_y * -1, imu.mag_z] # fix imu right hand rule

        # TODO don't recreate numpy array every time, heavy computation
        acc_meas = utils.to_unit_vector(acc_meas_raw) # acc unit vector
        mag_meas = utils.to_unit_vector(mag_meas_raw) # mag unit vector

        acc_ref = np.array([0.0, 0.0, -1.0]) # acc ref vector
        mag_ref = np.array([1.0, 0.0, 0.0]) # mag ref vector

        if not (np.any(acc_meas) and np.any(mag_meas)):
            logger.warn("measurement zero vector computed")
            continue

        rotation = triad.triad(acc_meas, mag_meas, acc_ref, mag_ref)

        logger.debug("acc: {} mag: {} rotation: {}".format(acc_meas, mag_meas, rotation))

        # broadcast all data to mission control server
        if config['enable_mission_control']:
            mc.broadcast(acc_meas_raw, mag_meas_raw, rotation)

        time.sleep(0.05)

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    main() # begin main loop
