from pressure.sampler import Sampler
from shared_state import calculate_timestamp, SENSOR_TYPE

sampler = Sampler()


def get_pressure(line):
    data = parse_input_line(line.strip())
    if data == None:
        return

    [_, voltage_1, _, voltage_2] = data
    if voltage_1 == None or voltage_2 == None:
        print(f"Invalid voltage: {line}")
        return

    # Add calculating voltage for both sensors

    pressure = calculate_pressure(voltage_1, SENSOR_TYPE)

    timestamp = calculate_timestamp()
    print(timestamp, pressure)
    sampler.push(timestamp, pressure)


def parse_input_line(line):
    voltage_1 = None
    id_1 = None
    voltage_2 = None
    id_2 = None

    for part in line.split(";"):
        try:
            key = part.split("=", 1)[0]
            value = part.split("=", 1)[1]
        except:
            print("Invalid input")
            return None

        if key == "V1":
            voltage_1 = value
        elif key == "id1":
            id_1 = value
        elif key == "V2":
            voltage_2 = value
        elif key == "id2":
            id_2 = value
        else:
            print("Invalid key")

    if (
        voltage_1 is not None
        and id_1 is not None
        and voltage_2 is not None
        and id_2 is not None
    ):
        pass
    else:
        print("Missing keys")
        return None

    try:
        voltage_1 = float(voltage_1)
        id_1 = float(id_1)
        voltage_2 = float(voltage_2)
        id_2 = float(id_2)
    except:
        print("Invadid pressure data")
        return None

    return [id_1, voltage_1, id_2, voltage_2]


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
    D = 11.33  # mbar
    return 10 ** ((voltage * 2.0 / 1000.0) * MUL - D)
