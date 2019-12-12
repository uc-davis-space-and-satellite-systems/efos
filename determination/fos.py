import logging
import logging.config
import time
import signal
import json
import pysnooper  # Is this needed?
import numpy as np
import utils
import triad
import mission_control as mc
from mpu9250 import MPU9250
from esc import ESC

# Fetch configuration data from the config file. The file contains multiple
# settings.
config = None
with open("./config/fos_config.json", 'r') as f:
    config = json.load(f)

# Set up the global logger service.
logging.config.fileConfig('./config/logging_config.ini')
logger = logging.getLogger(__name__)
if config['disable_logging']:
    logging.disable(logging.CRITICAL)

# Reconfigure the keyboard interrupt signal so that Ctrl-C kills the entire
# program forcibly instead of letting the program stop on its own.
signal.signal(signal.SIGINT, signal.SIG_DFL)

# @pysnooper.snoop(depth=1)


def get_updated_sensor_data(imu: MPU9250) -> tuple:
    """Gets updated raw measures of the acceloremter and magnetometer.
    Parameters
    ----------
    x : MPU9250
        An instance of the MPU9250 sensor class.

    Returns
    -------
    tuple
        A tuple of two vectors, represented by lists. Each list represents a
        vector [x, y, z]. The format is (accelerometer, magnetometer).
    """

    # Get new readings from the accelerometer and magnetometer.
    imu.update_acc_reading()
    imu.update_mag_reading()

    # Calculate the raw measures by fixing the imu right hand rule.
    raw_acc_measure = [imu.acc_y * -1, imu.acc_x, imu.acc_z * -1]
    raw_mag_measure = [imu.mag_x, imu.mag_y * -1, imu.mag_z]

    # Return a tuple of the calculated values.
    return (raw_acc_measure, raw_mag_measure)


def main():
    logger.debug("Initializing the imu...")

    # Initialize the imu.
    imu = MPU9250()

    # Initialize the speed controller.
    logger.debug("initializing esc...")
    esc_hdd = ESC(config['speed_pin_esc'],
                  config['dir_pin1_esc'], config['dir_pin2_esc'])
    esc_hdd.init_sequence()

    # If enabled, connect to the web interface server.
    if config['enable_mission_control']:
        logger.info("connecting to mission control server...")
        mc.connect()  # connect to mission control server

    logger.info("starting main loop...")
    # acc_array = np.zeros(3,1)
    # mag_array = np.zeros(3,1)
    while True:
        # Fetch and calculate raw measure values from the IMU.
        raw_acc_measure, raw_mag_measure = get_updated_sensor_data(imu)

        # TODO don't recreate numpy array every time, heavy memory computation
        # Generate the necessary vectors for TRIAD.
        acc_measure_uvec = utils.to_unit_vector(raw_acc_measure)
        mag_measure_uvec = utils.to_unit_vector(raw_mag_measure)

        # acc_array[:,0] = acc_meas_raw
        # mag_array[:,0] = mag_meas_raw
        # acc_meas = numpy.linalg.oth(acc_array)
        # mag_meas = numpu.linalg.oth(mag_array)

        # Create reference vectors for the accelerometer and magnetometer.
        acc_refvec = np.array([0.0, 0.0, -1.0])
        mag_refvec = np.array([1.0, 0.0, 0.0])

        # Make sure none of the vectors are zero vectors.
        if not (np.any(acc_measure_uvec) and np.any(mag_measure_uvec)):
            logger.warn("measurement zero vector computed")
            continue

        # Compute the rotation matrix with the aforementioned vectors.
        rotation = triad.triad(
            acc_measure_uvec, mag_measure_uvec, acc_refvec, mag_refvec)

        logger.debug("acc: {} mag: {} rotation: {}".format(
            acc_measure_uvec, mag_measure_uvec, rotation))

        # Broadcast the raw measures to the mission control server.
        if config['enable_mission_control']:
            mc.broadcast(raw_acc_measure, raw_mag_measure, rotation)

        # Simulate update frequency through sleeping.
        time.sleep(0.05)


if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    main()  # begin main loop
