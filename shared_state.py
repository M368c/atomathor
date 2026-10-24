import time
from pressure.sampler import Sampler

# Args in variables
INPUT = None
SENSOR_TYPE = None
TURBO_ADDRESS = None
TURBO_PORT = None
DISABLE_TURBO = None

sampler = Sampler()

# Timestamp
start_timestamp = time.time_ns() // 1000  # microseconds


def calculate_timestamp():
    current_timestamp = time.time_ns() // 1000
    timestamp = current_timestamp - start_timestamp
    return timestamp
