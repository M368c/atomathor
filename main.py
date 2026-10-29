import queue
import argparse
import threading
import shared_state
import ui.app

from mock_serial import MockSerial
from pcb_comm import start_pcb_serial_thread
from turbo_pump.turbo_comm import start_turbo_serial_thread
from turbo_pump.turbo_comm import commands as turbo_commands
from pcb_comm import commands as pcb_commands
from turbo_pump.x3.parameters import Parameters

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", default="/dev/ttyACM0", type=str, help="Serial input"
    )
    parser.add_argument(
        "-t",
        "--sensor_type",
        choices=["pkr361", "tpr250"],
        default="tpr250",
        type=str,
        help="Vacuum sensor type",
    )
    parser.add_argument(
        "-a",
        "--turbo_address",
        default="001",
        type=int,
        help="X3 address of turbo pump",
    )
    parser.add_argument(
        "-p", "--turbo_port", default="/dev/ttyACM0", type=str, help="X3 serial port"
    )
    parser.add_argument("--no_device", default=False, type=bool)
    parser.add_argument("--disable_turbo", default=False, type=bool)
    args = parser.parse_args()

shared_state.SENSOR_TYPE = args.sensor_type

if args.no_device:
    device = MockSerial()
    device.open()
    start_pcb_serial_thread(device.port)
else:
    start_pcb_serial_thread(args.input)

if not args.disable_turbo:
    start_turbo_serial_thread(args.turbo_port, args.turbo_address)
else:
    turbo_device = MockSerial()
    turbo_device.open()
    start_turbo_serial_thread(turbo_device.port, args.turbo_address)


def worker():
    while True:
        try:
            pcb_commands.put(("V1", "pr", "sns"), block=False)
            turbo_commands.put((Parameters.ActualSpd, "=?", "read", None), block=False)
        except queue.Full:
            pass


thread = threading.Thread(target=worker, daemon=True)
thread.start()

# Create gui
ui.app.create_qui()

print("Exiting")
