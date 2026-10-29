import queue
import dearpygui.dearpygui as dpg

from ui.components.plots import plot, update_plot
from shared_state import pressure_sampler
from pcb_comm import commands

timestamp = []
pressure = []
samples_counter = 0


def update_pressure_plot():
    global samples_counter
    try:
        commands.put(("V1", "pr", "sns"), block=False)  # Write command to serial
    except queue.Full:
        pass

    new_samples = pressure_sampler.samples[samples_counter:]
    if new_samples:
        for sample in new_samples:
            timestamp.append(sample[0] // 1000000)  # seconds
            pressure.append(sample[1])
        samples_counter += len(new_samples)
        dpg.set_value("current_pressure", pressure[-1])
        update_plot(
            timestamp, pressure, "p.time", "pressure", "pressure_data"
        )  # Update plot


def on_combo_change(sender, data):
    print(data)


def build():
    dpg.add_text("Pressure")
    with dpg.group(horizontal=True):
        dpg.add_text("--", tag="current_pressure")
        dpg.add_combo(
            items=["mbar"],
            width=100,
            callback=on_combo_change,
            default_value="mbar",
        )
    plot(timestamp, pressure, "p.time", "pressure", "pressure_data", 300)
