import time
from sampler import Sampler


class AppState:
    def __init__(self):
        self.SENSOR_TYPE = None
        self.DEBUG = None


state = AppState()
pressure_sampler = Sampler()
pump_speed_sampler = Sampler()

# Timestamp
start_timestamp = time.time_ns() // 1000  # microseconds


def calculate_timestamp():
    current_timestamp = time.time_ns() // 1000
    timestamp = current_timestamp - start_timestamp
    return timestamp
