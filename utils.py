import numpy as np

def to_unit_vector(vec):
    np_vec = np.array(vec)

    # TODO make sure these singularity checks actually work
    if np_vec.any():
        np_vec /= np.sqrt((np_vec ** 2).sum())

    return np_vec

if __name__ == "__main__":
    vec = [0, 1, 0]
    print("Vector: " + str(vec))
    print("Unit: " + str(to_unit_vector(vec)))
