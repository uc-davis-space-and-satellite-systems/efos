import numpy as np

def to_unit_vector(vec):
    np_vec = np.array(vec)
    return np_vec / np.sqrt((np_vec ** 2).sum())

if __name__ == "__main__":
    vec = [0, 1, 0]
    print("Vector: " + str(vec))
    print("Unit: " + str(to_unit_vector(vec)))
