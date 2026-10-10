import dearpygui.dearpygui as dpg


def update_plot(x, y):
    dpg.set_value("data", [x, y])


def plot(x, y, height=-1, width=-1):
    with dpg.plot(height=height, width=width):
        dpg.add_plot_axis(dpg.mvXAxis)
        dpg.add_plot_axis(dpg.mvYAxis, tag="y_axis")
        dpg.add_line_series(x, y, parent="y_axis", tag="data")
