import dearpygui.dearpygui as dpg

full_view = True


def update_plot(x, y, x_axis, y_axis, data_tag):
    # Update plot with data
    if not full_view:
        x, y = x[-1000:], y[-1000:]

    dpg.set_value(data_tag, [x, y])


def plot(x, y, x_axis, y_axis, data_tag, height=-1, width=-1):
    with dpg.plot(
        height=height,
        width=width,
        crosshairs=True,
    ):
        dpg.add_plot_axis(dpg.mvXAxis, tag=x_axis, auto_fit=True)

        if x_axis == "t.time":
            dpg.add_plot_axis(dpg.mvYAxis, tag=y_axis, auto_fit=True, log_scale=False)
        else:
            dpg.add_plot_axis(dpg.mvYAxis, tag=y_axis, auto_fit=True, log_scale=True)
        dpg.add_line_series(x, y, parent=y_axis, tag=data_tag)
