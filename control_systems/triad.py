import numpy as np
import math

sys.path.append('../core/')
from exceptions import InvalidDirectionCosineMatrix
from logger import Logger
​
# direction cosine matrix to euler angles
# https://www.learnopencv.com/rotation-matrix-to-euler-angles/
def dcm_to_euler(dcm):
    # verify that dcm is valid
    err = np.linalg.norm(np.identity(3, dtype=dcm.dtype) - np.dot(dcm.T, dcm))
    if err > 1e-6:
        raise InvalidDirectionCosineMatrix
    
    t = np.trace(dcm)
    r = np.sqrt(1+t)
    q_0 = 0.5*r
    q_1 = math.copysign(0.5*np.sqrt(1+dcm[0,0]-dcm[1,1]-dcm[2,2]),dcm[2,1]-dcm[1,2])
    q_2 = math.copysign(0.5*np.sqrt(1-dcm[0,0]+dcm[1,1]-dcm[2,2]),dcm[0,2]-dcm[2,0])
    q_3 = math.copysign(0.5*np.sqrt(1-dcm[0,0]-dcm[1,1]+dcm[2,2]),dcm[1,0]-dcm[0,1])
​
    # Display quaternion
    q = [q_0, q_1, q_2, q_3]
​
    print("q:")
    print(q)
    print()
​
    # Extract Euler angles from quaternion
    angle_x = np.arctan2(2*(q_0*q_1 + q_2*q_3), 1 - 2*(np.power(q_1, 2) + np.power(q_2, 2)))
    angle_y = np.arcsin(2*(q_0*q_2 - q_3*q_1))
    angle_z = np.arctan2(2*(q_0*q_3 + q_1*q_2), 1 - 2*(np.power(q_2, 2) + np.power(q_3, 2)))
​
    # Convert Euler angles to degrees
    angle_x = np.degrees(angle_x)
    angle_y = np.degrees(angle_y)
    angle_z = np.degrees(angle_z)
​
    # Display Euler angles
    angles = [angle_x, angle_y, angle_z]
​
    print("Euler angles:")
    print(angles)
    print()
​
    return q
​
# @pysnooper.snoop(depth=1)
def triad(acc_meas, mag_meas, acc_ref, mag_ref):
    v_1b = np.asmatrix(acc_meas)    # Accelerometer vector in body frame (measurement)
    v_2b = np.asmatrix(mag_meas)    # Magnetic Field vector in body frame (measurement)
    v_1i = np.asmatrix(acc_ref)   # Accelerometer vector in reference frame
    v_2i = np.asmatrix(mag_ref)    # Magnetic Field vector in reference frame
​
    t_1b = v_1b                     # First basis vector in body frame
    t_2b = np.cross(v_1b, v_2b)     # Second basis vector in body frame
​
    # TODO make sure these singularity checks actually work
    if t_2b.any():
        t_2b = np.divide(t_2b, np.linalg.norm(t_2b))    # Normalize second basis vector
​
    t_3b = np.cross(t_1b, t_2b)     # Third basis vector in body frame
​
    t_1i = v_1i                     # First basis vector in reference frame
    t_2i = np.cross(v_1i, v_2i)     # Second basis vector in reference frame
​
    # TODO make sure these singularity checks actually work
    if t_2i.any():
        t_2i = np.divide(t_2i, np.linalg.norm(t_2i))    # Normalize second basis vector
​
    t_3i = np.cross(t_1i, t_2i)     # Third basis vector in reference frame
​
    R_bt = np.concatenate((t_1b, t_2b, t_3b)).T    # Construct DCM for body frame
    R_it = np.concatenate((t_1i, t_2i, t_3i)).T    # Construct DCM for reference frame
    R_bi = np.matmul(R_bt, R_it.T)      # Construct DCM from reference frame to body frame
    
    print("R_bi:")
    print(R_bi)
    print()
    
    logger.debug("TRIAD DCM: {}".format(R_bi.flatten()))
​
    return dcm_to_euler(R_bi)
​
if __name__ == "__main__":
    acc_meas = np.matrix([0, 0, -1])    # accelerometer vector in body frame
    mag_meas = np.matrix([1, 0, 0])    # Magnetic Field vector in body frame
    acc_ref = np.matrix([0, 0, -1])    # accelerometer vector in reference frame
    mag_ref = np.matrix([1, 0, 0])     # Magnetic Field vector in reference frame
​
    print(triad(acc_meas, mag_meas, acc_ref, mag_ref))