import sys
import numpy as np

sys.path.append("../control_systems/")
import triad

def test_triad(q0, q1, q2, q3):
    acc_meas = np.array([0.0, 0.0, -1.0])
    mag_meas = np.array([1.0, 0.0, 0.0])
    acc_ref = np.array([0.0, 0.0, -1.0]) # constant reference vector
    mag_ref = np.array([1.0, 0.0, 0.0]) # constant reference vector

    print("Input Reference Vectors:")
    print("Acc:", acc_meas)
    print("Mag:", mag_meas)
    print()

    print("Input Quaternion:")
    print("q0:", q0)
    print("q1:", q1)
    print("q2:", q2)
    print("q3:", q3)
    print()

    rot = np.array([
        [1-2*(q2*q2+q3*q3), 2*(q1*q2-q3*q0), 2*(q1*q3+q2*q0)],
        [2*(q1*q2+q3*q0), 1-2*(q1*q1+q3*q3), 2*(q2*q3-q1*q0)],
        [2*(q1*q3-q2*q0), 2*(q2*q3+q1*q0), 1-2*(q1*q1+q2*q2)]
    ])

    print("Direction Cosine Matrix:")
    print(rot)
    print()

    print("Determinant of DCM:")    # proper matrix is det(rot)=1, improper if det(rot)=-1
    print(np.linalg.det(rot))
    print()

    acc_meas_rot = np.dot(rot, acc_meas)
    mag_meas_rot = np.dot(rot, mag_meas)

    print("Output Rotated Measurement Vectors:")
    print("Acc:", acc_meas_rot)
    print("Mag:", mag_meas_rot)
    print()

    rot_triad = triad_quaternion_v4.triad(acc_meas_rot, mag_meas_rot, acc_ref, mag_ref)
    rot_input = np.array([q0, q1, q2, q3])
    valid = np.allclose(rot_triad, rot_input)
    if (valid == False):
        rot_triad = np.dot(-1, rot_triad)
        valid = np.allclose(rot_triad, rot_input)

    print("Output Rotations:")
    print("Input:", rot_input)
    print("Output:", rot_triad)
    print("Valid:", valid)

    return valid

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22222818/how-to-printing-numpy-array-with-3-decimal-places
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    test_triad(0.64085638, -0.69636424, -0.1227878, 0.29883624)
​
    '''
    valid_cnt = 0
    total_cnt = 360**3
​
    for r in range(-180, 180):
        for p in range(-180, 180):
            for y in range(-180, 180):
                valid = test_triad(r, p, y)
                if valid: valid_cnt += 1
                print("[", r, p, y, "]:", valid, valid_cnt, "/", total_cnt)
    '''