import dearpygui.dearpygui as dpg
from components.plots import plot, update_plot

current_pressure = "--"
x = []  # time
y = []  # samples


def on_combo_change(sender, app_data):
    print(app_data)


def build():
    dpg.add_text("Pressure")
    with dpg.group(horizontal=True):
        dpg.add_text(current_pressure)
        dpg.add_combo(
            items=["mbar"],
            width=100,
            callback=on_combo_change,
            default_value="mbar",
        )
    plot(x, y, 300)
