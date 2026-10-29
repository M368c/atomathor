import time
from sampler import Sampler

SENSOR_TYPE = None

pressure_sampler = Sampler()
pump_speed_sampler = Sampler()

# Timestamp
start_timestamp = time.time_ns() // 1000  # microseconds


def calculate_timestamp():
    current_timestamp = time.time_ns() // 1000
    timestamp = current_timestamp - start_timestamp
    return timestamp
