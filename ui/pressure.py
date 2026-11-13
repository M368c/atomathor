import queue
import dearpygui.dearpygui as dpg

from ui.components.plots import plot, update_plot
from shared_state import pressure_sampler_1, pressure_sampler_2

timestamp1 = []
pressure1 = []

timestamp2 = []
pressure2 = []


def update_pressure_plot():
    if pressure_sampler_1.samples:
        new_samples = pressure_sampler_1.samples[-1]
        timestamp1.append(new_samples[0] / 1000000)  # seconds
        pressure1.append(new_samples[1])
        dpg.set_value("current_pressure1", "{:.4e}".format(new_samples[1]))

        update_plot(
            timestamp1, pressure1, "p.time1", "pressure1", "pressure_data1"
        )  # Update plot

    if pressure_sampler_2.samples:
        new_samples = pressure_sampler_2.samples[-1]
        timestamp2.append(new_samples[0] / 1000000)  # seconds
        pressure2.append(new_samples[1])
        dpg.set_value("current_pressure2", "{:.4e}".format(new_samples[1]))

        update_plot(
            timestamp2, pressure2, "p.time2", "pressure2", "pressure_data2"
        )  # Update plot


def on_combo_change(sender, data):
    print(data)


def build():
    dpg.add_text("Pressure")
    with dpg.group(horizontal=True):
        dpg.add_text(0.0, tag="current_pressure1")
        dpg.add_combo(
            items=["mbar"],
            width=100,
            callback=on_combo_change,
            default_value="mbar",
        )
    plot(timestamp1, pressure1, "p.time1", "pressure1", "pressure_data1", 300)

    dpg.add_text(0.0, tag="current_pressure2")
    plot(timestamp2, pressure2, "p.time2", "pressure2", "pressure_data2", 300)
