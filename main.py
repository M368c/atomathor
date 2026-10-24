import argparse
import shared_state
from pcb_comm import start_pcb_serial_thread

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
    parser.add_argument("--disable_turbo", default=False, type=bool)
    args = parser.parse_args()

shared_state.INPUT = args.input
shared_state.SENSOR_TYPE = args.sensor_type
shared_state.TURBO_ADDRESS = args.turbo_address
shared_state.TURBO_PORT = args.turbo_port
shared_state.DISABLE_TURBO = args.disable_turbo

start_pcb_serial_thread(args.input)
