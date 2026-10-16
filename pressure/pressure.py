from pressure.sampler import Sampler
from shared_state import calculate_timestamp, SENSOR_TYPE

sampler = Sampler()


def get_pressure(line):
    data = parse_input_line(line.strip())
    if data == None:
        return

    [voltage, _, _] = data
    if voltage == None:
        print(f"Invalid voltage: {line}")
        return

    pressure = calculate_pressure(voltage, SENSOR_TYPE)

    timestamp = calculate_timestamp()
    print(timestamp, pressure)
    sampler.push(timestamp, pressure)


def parse_input_line(line):
    pressure_voltage = None
    voltage = None
    current = None

    for part in line.split(";"):
        try:
            key = part.split("=", 1)[0]
            value = part.split("=", 1)[1]
        except:
            print("Invalid input")
            return None

        if key == "pv":
            pressure_voltage = value
        elif key == "v":
            voltage = value
        elif key == "c":
            current = value
        else:
            print("Invalid key")

    if pressure_voltage is not None and voltage is not None and current is not None:
        pass
    else:
        print("Missing keys")
        return None

    try:
        pressure_voltage = float(pressure_voltage)
        voltage = float(voltage)
        current = float(current)
    except:
        print("Invadid pressure data")
        return None

    return [pressure_voltage, voltage, current]


def calculate_pressure(voltage: float, sensor_type: str):
    if sensor_type == "pkr361":
        return calculate_pressure_pkr361(voltage)
    else:
        return calculate_pressure_tpr250(voltage)


def calculate_pressure_tpr250(voltage: float):
    C = 2.5
    return 10 ** ((voltage * 2.0 / 1000.0) - C)


def calculate_pressure_pkr361(voltage: float):
    MUL = 1.667
    D = 8.458
    return 10 ** ((voltage * 2.0 / 1000.0) * MUL - D)
