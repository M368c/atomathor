import sys
import serial
import threading
import queue

from turbo_pump.x3.frame import encode, decode
from shared_state import pump_speed_sampler, calculate_timestamp
from turbo_pump.x3.parameters import Parameters

commands = queue.Queue()  # writing (tuples)
user_commands = queue.Queue()
data = queue.Queue()  # reading


def start_turbo_serial_thread(port, address):
    global ser
    try:
        ser = serial.Serial(port, 9600, timeout=1, bytesize=8, parity="N", stopbits=1)
        ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"Turbo serial: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Turbo serial: Port not found. Check device connection.")
        sys.exit(1)
    except PermissionError:
        print("Turbo serial: Permission denied!")
        sys.exit(1)

    thread = threading.Thread(target=worker, args=[address], daemon=True)
    thread.start()
    print(f"Turbo thread started, reading from serial port: {port}")


def worker(address):
    while True:
        if not user_commands.empty():
            parameter, command, action, caller = user_commands.get_nowait()
        else:
            parameter, command, action, caller = commands.get()

        serial_write(address, parameter, command, action)

        is_read = serial_read(caller)
        if not is_read and caller != None:
            data.put((False, "Error: no response", caller))


def serial_write(address, parameter: Parameters, data, action):
    frame = encode(address, parameter, data, action)
    if frame != None:
        ser.write(frame)


def serial_read(caller):
    line = ser.read_until(b"\r")
    if not line:
        return

    address, parameter_value, parameter_data = decode(line)

    parameter = Parameters(int(parameter_value))
    data.put((parameter.name, parameter_data, caller))
    # print(f"Turbo pump response: {parameter.name}, {parameter_data}")

    if parameter == Parameters.ActualSpd:
        pump_speed_sampler.push(calculate_timestamp(), float(parameter_data))

    return True
