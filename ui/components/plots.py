import dearpygui.dearpygui as dpg


def update_plot(x, y, x_axis, y_axis, data_tag):
    # Update plot with data
    dpg.set_value(data_tag, [x, y])

    # Auto adjust to show newly plotted data
    dpg.fit_axis_data(x_axis)
    dpg.fit_axis_data(y_axis)


def plot(x, y, x_axis, y_axis, data_tag, height=-1, width=-1):
    with dpg.plot(height=height, width=width):
        dpg.add_plot_axis(dpg.mvXAxis, tag=x_axis)
        dpg.add_plot_axis(dpg.mvYAxis, tag=y_axis)
        dpg.add_line_series(x, y, parent=y_axis, tag=data_tag)
