import numpy as np
import pysnooper

# @pysnooper.snoop(depth=1)
def triad(acc_meas, mag_meas, acc_ref, mag_ref):
    v_1b = np.asmatrix(acc_meas)    # Accelerometer vector in body frame (measurement)
    v_2b = np.asmatrix(mag_meas)    # Magnetic Field vector in body frame (measurement)
    v_1i = np.asmatrix(acc_ref)   # Accelerometer vector in reference frame
    v_2i = np.asmatrix(mag_ref)    # Magnetic Field vector in reference frame

    t_1b = v_1b                     # First basis vector in body frame
    t_2b = np.cross(v_1b, v_2b)     # Second basis vector in body frame

    if t_2b.all() != 0:
        t_2b = np.divide(t_2b, np.linalg.norm(t_2b))    # Normalize second basis vector

    t_3b = np.cross(t_1b, t_2b)     # Third basis vector in body frame

    t_1i = v_1i                     # First basis vector in reference frame
    t_2i = np.cross(v_1i, v_2i)     # Second basis vector in reference frame

    if t_2i.all() != 0:
        t_2i = np.divide(t_2i, np.linalg.norm(t_2i))    # Normalize second basis vector

    t_3i = np.cross(t_1i, t_2i)     # Third basis vector in reference frame

    R_bt = np.concatenate((t_1b, t_2b, t_3b)).T    # Construct DCM for body frame
    R_it = np.concatenate((t_1i, t_2i, t_3i)).T    # Construct DCM for reference frame
    R_bi = np.matmul(R_bt, R_it.T)      # Construct DCM from reference frame to body frame

    theta_roll = np.arctan2(-1*R_bi.item((1,2)), R_bi.item((2,2)))      # Euler angle from x-axis
    theta_pitch = np.arctan2(R_bi.item((0,2)), np.sqrt(np.power(R_bi.item((0,0)), 2) + np.power(R_bi.item((0,0)), 2)))  #Euler angle from y-axis
    theta_yaw = np.arctan2(-1*R_bi.item((0,1)), R_bi.item((1,1)))   # Euler angle from z-axis

    theta_roll = np.degrees(theta_roll)       # Convert Euler Angles from radians
    theta_pitch = np.degrees(theta_pitch)     # to degrees
    theta_yaw = np.degrees(theta_yaw)

    return [theta_roll, theta_pitch, theta_yaw]

if __name__ == "__main__":
    acc_meas = np.matrix([0, 0, -1])    # accelerometer vector in body frame
    mag_meas = np.matrix([1, 0, 0])    # Magnetic Field vector in body frame
    acc_ref = np.matrix([0, 0, -1])    # accelerometer vector in reference frame
    mag_ref = np.matrix([1, 0, 0])     # Magnetic Field vector in reference frame

    print(triad(acc_meas, mag_meas, acc_ref, mag_ref))
