import sys
sys.path.append("..")

import numpy as np
import triad

def test_triad(r, p, y):
    acc_meas = np.array([0.0, 0.0, -1.0])
    mag_meas = np.array([1.0, 0.0, 0.0])
    acc_ref = np.array([0.0, 0.0, -1.0]) # constant reference vector
    mag_ref = np.array([1.0, 0.0, 0.0]) # constant reference vector

    print("Input Reference Vectors:")
    print("Acc:", acc_meas)
    print("Mag:", mag_meas)
    print()

    theta_roll = r
    theta_pitch = p
    theta_yaw = y

    print("Input Rotation:")
    print("Roll:", theta_roll)
    print("Pitch:", theta_pitch)
    print("Yaw:", theta_yaw)
    print()

    theta_roll = np.radians(-1 * theta_roll)
    theta_pitch = np.radians(-1 * theta_pitch)
    theta_yaw = np.radians(-1 * theta_yaw)

    rot_y = np.array([
        [np.cos(theta_yaw), -1 * np.sin(theta_yaw), 0],
        [np.sin(theta_yaw), np.cos(theta_yaw), 0],
        [0, 0, 1]
    ])

    rot_p = np.array([
        [np.cos(theta_pitch), 0, np.sin(theta_pitch)],
        [0, 1, 0],
        [-1 * np.sin(theta_pitch), 0, np.cos(theta_pitch)]
    ])

    rot_r = np.array([
        [1, 0, 0],
        [0, np.cos(theta_roll), -1 * np.sin(theta_roll)],
        [0, np.sin(theta_roll), np.cos(theta_roll)]
    ])

    print("Rotation Matrix:")
    print("R:")
    print(rot_r)
    print("P:")
    print(rot_p)
    print("Y:")
    print(rot_y)

    # being verbose for some reason helps wtf??
    rot_tmp = np.dot(rot_r, rot_p)
    rot = np.dot(rot_tmp, rot_y)
    rot = rot.T

    print("RPY:")
    print(rot)
    print()

    acc_meas_rot = np.dot(rot, acc_meas)
    mag_meas_rot = np.dot(rot, mag_meas)

    print("Output Rotated Measurement Vectors:")
    print("Acc:", acc_meas_rot)
    print("Mag:", mag_meas_rot)
    print()

    rot_triad = triad.triad(acc_meas_rot, mag_meas_rot, acc_ref, mag_ref)
    rot_input = np.degrees([-theta_roll, -theta_pitch, -theta_yaw])
    valid = np.allclose(rot_triad, rot_input)

    print("Output Rotations:")
    print("Input:", rot_input)
    print("Output:", rot_triad)
    print("Valid:", valid)

    return valid

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    test_triad(-180, 95, 3)

    '''
    valid_cnt = 0
    total_cnt = 360**3

    for r in range(-180, 180):
        for p in range(-180, 180):
            for y in range(-180, 180):
                valid = test_triad(r, p, y)
                if valid: valid_cnt += 1
                print("[", r, p, y, "]:", valid, valid_cnt, "/", total_cnt)
    '''
