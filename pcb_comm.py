import sys
import serial
import threading
from crc import Calculator, Configuration

from pressure.pressure import get_pressure
from shared_state import INPUT

# Request: \n@{addr, 2B} {msgID, 2B} {msg}|{crc}\n
# Response: \n!{msgID, 2B} {msg}|{crc}\n

try:
    ser = serial.Serial(INPUT, 9600, timeout=1, bytesize=8, parity="N", stopbits=1)
    ser.reset_input_buffer()
except serial.SerialException as e:
    print(f"Serial error: {e}")
    sys.exit(1)
except FileNotFoundError:
    print("Port not found. Check device connection.")
    sys.exit(1)
except PermissionError:
    print("Permission denied!")
    sys.exit(1)


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


def serial_write(addr, msgID, msg):
    data = f"@{addr} {msgID} {msg}"
    crc = calculator.checksum(data.encode("ascii"))
    ser.write(f"\n{data}|{crc}\n".encode("ascii"))


def serial_read(pressure_addr="pr"):
    while True:
        line = ser.readline()
        if not line:
            continue

        payload, _, crc_text = line.rpartition(b"|")
        if not calculator.verify(payload, crc_text):
            print("Message is not valid!")
            continue

        try:
            line = line.decode("ascii").strip()
        except:
            print(f"Could not decode line: {line}")
            continue

        print(line)

        if len(line) == 0:
            continue

        if line[0] != "!":
            print("Message is not from pcb!")
            continue

        addr = line[1:3]
        msg_id = line[4:6]
        msg = line[7:]
        msg = msg.split("|", 1)[0]
        print(addr, msg_id, msg)

        if addr == pressure_addr:
            get_pressure(msg)
        else:
            print("Address is not valid")
            continue


def start_pcb_serial_thread():
    # Start reading thread
    thread = threading.Thread(target=serial_read)
    thread.start()
    print(f"Thread started, reading from serial port: {INPUT}")
