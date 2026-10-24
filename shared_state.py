import time
from pressure.sampler import Sampler

SENSOR_TYPE = None

sampler = Sampler()

# Timestamp
start_timestamp = time.time_ns() // 1000  # microseconds


def calculate_timestamp():
    current_timestamp = time.time_ns() // 1000
    timestamp = current_timestamp - start_timestamp
    return timestamp
