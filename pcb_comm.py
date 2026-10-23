import sys
import serial
import threading
from crc import Calculator, Configuration

from pressure.pressure import get_pressure

# Request: @{addr, 2B} {msgID, 2B} {msg}|{crc}\n
# Response: !{msgID, 2B} {msg}|{crc}\n


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

    # Start reading thread
    thread = threading.Thread(target=serial_read)
    thread.start()
    print(f"Thread started, reading from serial port: {port}")


def serial_write(addr, msgID, msg):
    data = f"@{addr} {msgID} {msg}"
    crc = calculator.checksum(data.encode("ascii"))
    print(f"Request: {data}|{crc:x}")
    ser.write(f"{data}|{crc:x}\n".encode("ascii"))


def serial_read(pressure_addr="pr"):
    while True:
        line = ser.readline()
        if not line:
            continue

        print(line)
        payload, _, crc_text = line.rpartition(b"|")

        try:
            crc = int(crc_text.strip(), 16)

            if not calculator.verify(payload, crc):
                print("Crc is not valid!")
                continue
        except ValueError:
            print("Could not parse crc!")
            continue

        try:
            line = line.decode("ascii").strip()
        except:
            print(f"Could not decode line: {line}")
            continue

        print(f"Data: {line}")

        if len(line) == 0:
            continue

        if line[0] != "!":
            print("Message is not from pcb!")
            continue

        msg_id = line[1:3]
        msg = line[4:]
        msg = msg.split("|", 1)[0]

        if msg_id == pressure_addr:
            get_pressure(msg)
        else:
            print("Message doesn't have a valid id!")
            continue
