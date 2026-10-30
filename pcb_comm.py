import sys
import serial
import threading
import queue

from crc import Calculator, Configuration
from pressure.pressure import get_pressure

# Request: @{addr, 2B} {msgID, 2B} {msg}|{crc}\n
# Response: !{msgID, 2B} {msg}|{crc}\n

commands = queue.Queue()  # writing (tuples)
user_commands = queue.Queue()
data = queue.Queue()  # reading

# CRC configuration
config = Configuration(
    width=8,
    polynomial=0x4D,
    init_value=0xFF,
    final_xor_value=0xFF,
    reverse_input=True,
    reverse_output=True,
)

calculator = Calculator(config)


def start_pcb_serial_thread(port):
    global ser
    try:
        ser = serial.Serial(port, 9600, timeout=1, bytesize=8, parity="N", stopbits=1)
        ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"Main serial: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Main serial: Port not found. Check device connection.")
        sys.exit(1)
    except PermissionError:
        print("Main serial: Permission denied!")
        sys.exit(1)

    # Start serial thread
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    print(f"Thread started, reading from serial port: {port}")


def worker():
    while True:
        if not user_commands.empty():
            addr, msg_id, msg = user_commands.get()
        else:
            addr, msg_id, msg = commands.get()

        serial_write(addr, msg_id, msg)

        serial_read()


def serial_write(addr, msgID, msg):
    data = f"@{addr} {msgID} {msg}"
    crc = calculator.checksum(data.encode("ascii"))
    # print(f"Request: {data}|{crc:x}")
    ser.write(f"{data}|{crc:x}\n".encode("ascii"))


def serial_read():
    line = ser.readline()
    if not line:
        return

    print(line)
    payload, _, crc_text = line.rpartition(b"|")

    try:
        crc = int(crc_text.strip(), 16)

        if not calculator.verify(payload, crc):
            print("Crc is not valid!")
            return
    except ValueError:
        print("Could not parse crc!")
        return

    try:
        line = line.decode("ascii").strip()
    except:
        print(f"Could not decode line: {line}")
        return

    # print(f"Data: {line}")

    if len(line) == 0:
        return

    if line[0] != "!":
        print("Message is not from pcb!")

    msg_id = line[1:3]
    msg = line[4:]
    msg = msg.split("|", 1)[0]

    if msg_id == "pr":
        get_pressure(msg)
    elif msg_id == "cm":
        data.put((msg_id, msg))
    else:
        print("Message doesn't have a valid id!")
