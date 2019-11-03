import random
import utils

NUM_TESTS = 100


def test_utils_vector_to_unit_vector():
    """Tests utils.py's to_unit_vector function

    Enter "pytest test_utils.py in the terminal to run the test script.
    """

    # Test 100 times.
    for _ in range(100):
        # Create a vector of random values.
        x = random.randint(-999999999, 999999999)
        y = random.randint(-999999999, 999999999)
        z = random.randint(-999999999, 999999999)
        vector = [x, y, z]

        # Calculate the correct unit vector manually.
        magnitude = (x**2 + y**2 + z**2)**0.5
        unit_vector = [_ / magnitude for _ in vector]

        # Get the unit vector from utils.py's function.
        unit_vector_from_utils = utils.to_unit_vector(vector).tolist()

        # Compare the x, y, and z values of the two unit vectors.
        assert(unit_vector[0] == unit_vector_from_utils[0])
        assert(unit_vector[1] == unit_vector_from_utils[1])
        assert(unit_vector[2] == unit_vector_from_utils[2])
