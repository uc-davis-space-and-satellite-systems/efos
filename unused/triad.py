# triad test function
def skew(vec):
    return np.matrix([
        [0, -vec[2], vec[1]],
        [vec[2], 0, -vec[0]],
        [-vec[1], vec[0], 0]
    ])

# triad test function
# @pysnooper.snoop(depth=1)
def triadv2(acc_meas, mag_meas, acc_ref, mag_ref):
    acc_meas = np.asmatrix(acc_meas).T    # Accelerometer vector in body frame (measurement)
    mag_meas = np.asmatrix(mag_meas).T    # Magnetic Field vector in body frame (measurement)
    acc_ref = np.asmatrix(acc_ref).T   # Accelerometer vector in reference frame
    mag_ref = np.asmatrix(mag_ref).T    # Magnetic Field vector in reference frame

    v1_body = acc_meas
    v1_ref = acc_ref

    v2_body = np.dot(skew(acc_meas), mag_meas)
    if v2_body.all() != 0:
        v2_body = np.divide(v2_body, np.linalg.norm(v2_body))

    v2_ref = np.dot(skew(acc_ref), mag_ref)
    if v2_ref.all() != 0:
        v2_ref = np.divide(v2_ref, np.linalg.norm(v2_ref))

    v3_body = np.dot(skew(v1_body), v2_body)
    v3_ref = np.dot(skew(v1_ref), v2_ref)

    rot_body = np.concatenate((v1_body, v2_body, v3_body), axis=1)
    rot_ref = np.concatenate((v1_ref, v2_ref, v3_ref), axis=1)
    rot = np.dot(rot_ref, rot_body.T).T

    print(rot)
    dcm_to_euler(rot)

    theta_roll = np.arctan2(-1*rot.item((1,2)), rot.item((2,2)))      # Euler angle from x-axis
    theta_pitch = np.arctan2(rot.item((0,2)), np.sqrt(np.power(rot.item((0,0)), 2) + np.power(rot.item((0,1)), 2)))  #Euler angle from y-axis
    theta_yaw = np.arctan2(-1*rot.item((0,1)), rot.item((1,1)))   # Euler angle from z-axis

    theta_roll = np.degrees(theta_roll)       # Convert Euler Angles from radians
    theta_pitch = np.degrees(theta_pitch)     # to degrees
    theta_yaw = np.degrees(theta_yaw)

    return [theta_roll, theta_pitch, theta_yaw]
