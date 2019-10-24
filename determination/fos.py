import logging, logging.config

# setup global logger service
logging.config.fileConfig('./config/logging_config.ini')
logger = logging.getLogger(__name__)

import time, signal, json, pysnooper
import numpy as np
import utils, triad
import mission_control as mc
from mpu9250 import MPU9250
from esc import ESC
import triad_2_PID

# configure terminate signal, when we do ctrl C we want
# to kill the entire program forcibly, not wait for the
# program to stop on its own
signal.signal(signal.SIGINT, signal.SIG_DFL)

# fetch configuration data from the config file
# contains various settings
config = None
with open("./config/fos_config.json", 'r') as f:
    config = json.load(f)

# @pysnooper.snoop(depth=1)
def main():
    logger.debug("initializing imu...")
    imu = MPU9250() # initialize mpu9250, the imu

    logger.debug("initializing esc...")
    esc_hdd = ESC(config['speed_pin_esc'], config['dir_pin1_esc'], config['dir_pin2_esc'])
    esc_hdd.init_sequence() # perform the esc initialization sequence

    # do we want to stream sensor data to the web interface
    if config['enable_mission_control']:
        logger.info("connecting to mission control server...")
        mc.connect() # connect to mission control server

    logger.info("starting main loop...")
    #acc_array = np.zeros(3,1)
    #mag_array = np.zeros(3,1)
    while True: ## TODO This should be depedant on when we are actively tryin to fix ourselves: based on magnetic coils
        # fetch values from the IMU
        imu.update_acc_reading() # update acc values
        imu.update_mag_reading() # update mag values

        acc_meas_raw = [imu.acc_y * -1, imu.acc_x, imu.acc_z * -1] # fix imu right hand rule
        mag_meas_raw = [imu.mag_x, imu.mag_y * -1, imu.mag_z] # fix imu right hand rule

        # generate the necessary vectors for TRIAD
        #DONE# don't recreate numpy array every time, heavy memory computation
        acc_meas = utils.to_unit_vector(acc_meas_raw) # acc unit vector
        mag_meas = utils.to_unit_vector(mag_meas_raw) # mag unit vector

        # TODO if code below replaces code above and is more compoutationaly effecient
        #acc_array[:,0] = acc_meas_raw
        #mag_array[:,0] = mag_meas_raw
        #acc_meas = numpy.linalg.oth(acc_array)
        #mag_meas = numpu.linalg.oth(mag_array)

        acc_ref = np.array([0.0, 0.0, -1.0]) # acc ref vector
        mag_ref = np.array([1.0, 0.0, 0.0]) # mag ref vector

        # make sure none of the vectors are zero vectors
        if not (np.any(acc_meas) and np.any(mag_meas)):
            logger.warn("measurement zero vector computed")
            continue

        # compute the rotation matrix with the aforemened vectors
        rotation = triad.triad(acc_meas, mag_meas, acc_ref, mag_ref)
        # TODO Make sure triad2PID works....
        #correction=triad_2_PID(rotation) ##Utilize PID in seperate file and give back 'correct' rotation... for our understanding
        logger.debug("acc: {} mag: {} rotation: {} correction: {}".format(acc_meas, mag_meas, rotation,correction))

        # broadcast all data to mission control server
        # this is the real-time gui thing
        if config['enable_mission_control']:
            mc.broadcast(acc_meas_raw, mag_meas_raw, rotation)

        # wait a sec before proceeding, this is our
        # update frequency.
        time.sleep(0.05)

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    main() # begin main loop
