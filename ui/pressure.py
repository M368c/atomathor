import queue
import dearpygui.dearpygui as dpg

from ui.components.plots import plot, update_plot
from shared_state import sampler
from pcb_comm import commands

current_pressure = "--"
timestamp = []
pressure = []


def update_pressure_plot():
    global current_pressure, timestamp, pressure
    try:
        commands.put(("V1", "pr", "sns"), block=False)  # Write command to serial
    except queue.Full:
        pass

    samples = sampler.samples
    if samples:
        for sample in samples:
            timestamp.append(sample[0] // 1000000)  # seconds
            pressure.append(sample[1])

        dpg.set_value("current_pressure", pressure[-1])
        update_plot(timestamp, pressure)  # Update plot


def on_combo_change(sender, data):
    print(data)


def build():
    dpg.add_text("Pressure")
    with dpg.group(horizontal=True):
        dpg.add_text(current_pressure, tag="current_pressure")
        dpg.add_combo(
            items=["mbar"],
            width=100,
            callback=on_combo_change,
            default_value="mbar",
        )
    plot(timestamp, pressure, 300)
