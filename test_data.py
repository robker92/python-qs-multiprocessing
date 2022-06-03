import json
import random

# PARAMS
LENGTH_OF_NUMBER_LIST = 15000000
NUMBER_RANGE_START = -10000
NUMBER_RANGE_END = 10000

NUMBER_LIST_FILE_NAME = 'number_data.json'

def create_number_test_data():
    """Create a list of random generated numbers according to the given parameters."""

    randomlist = []
    for i in range(0,LENGTH_OF_NUMBER_LIST):
        n = random.randint(NUMBER_RANGE_START,NUMBER_RANGE_END)
        randomlist.append(n)

    with open(NUMBER_LIST_FILE_NAME, 'w') as f:
        json.dump(randomlist, f)


def read_number_test_data():
    """Read the number test data from the json file."""

    with open(NUMBER_LIST_FILE_NAME) as f:
        data = json.load(f)
        return data

if __name__ == '__main__':
    create_number_test_data()
    