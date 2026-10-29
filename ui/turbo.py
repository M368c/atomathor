import queue
import dearpygui.dearpygui as dpg

from ui.components.plots import plot, update_plot
from shared_state import pump_speed_sampler
from turbo_pump.turbo_comm import commands, user_commands
from turbo_pump.x3.parameters import Parameters
from turbo_pump.x3.data_type import DataType, encode_data

timestamp = []
pump_speed = []
samples_counter = 0


def update_speed():
    global samples_counter
    try:
        commands.put((Parameters.ActualSpd, "=?", "read", None), block=False)
    except queue.Full:
        pass

    new_samples = pump_speed_sampler.samples[samples_counter:]
    if new_samples:
        for sample in new_samples:
            timestamp.append(sample[0] // 1000000)  # seconds
            pump_speed.append(sample[1])
        samples_counter += len(new_samples)
        dpg.set_value("current_speed", pump_speed[-1])
        update_plot(
            timestamp, pump_speed, "t.time", "speed", "speed_data"
        )  # Update plot


def start_turbo():
    try:
        user_commands.put(
            (Parameters.PumpgStatn, True, "write", "turbo_response"), block=False
        )
    except queue.Full:
        print("Commands queue is full!")


def stop_turbo():
    try:
        user_commands.put(
            (Parameters.PumpgStatn, False, "write", "turbo_response"), block=False
        )
    except queue.Full:
        print("Commands queue is full!")


def build():
    dpg.add_text("Turbo speed")
    with dpg.group(horizontal=True):
        dpg.add_text("--", tag="current_speed")
    plot(timestamp, pump_speed, "t.time", "speed", "speed_data", 300)
    dpg.add_button(label="Start turbo", callback=start_turbo)
    dpg.add_button(label="Stop turbo", callback=stop_turbo)
    dpg.add_button(label="Turbo parameters", callback=parameters_window)
    dpg.add_text(tag="turbo_response")


def type_description(type: DataType):
    match type:
        case DataType.BooleanOld:
            return "enter boolean value (true/false)"
        case DataType.UInteger:
            return "enter positive integer"
        case DataType.UReal:
            return "enter float value"
        case DataType.String:
            return "enter text with 6 characters"
        case DataType.BooleanNew:
            return "enter boolean value (true/false)"
        case DataType.UShortInt:
            return "enter positive integer"
        case DataType.Exponential:
            return "enter positive number"
        case DataType.String16:
            return "enter text with 16 characters"
        case DataType.String8:
            return "enter text with 8 characters"


def is_valid(type, data):
    response = encode_data(type, data)
    if response:
        return True
    else:
        return False


def on_change(sender, app_data, user_data):
    param = Parameters[sender]
    param_name = param.name
    param_data_type = param.data_type
    valid = is_valid(param_data_type, app_data)

    # Change color
    valid_input_theme = user_data[0]
    invalid_input_theme = user_data[1]
    if valid:
        dpg.bind_item_theme(param_name, valid_input_theme)
    else:
        dpg.bind_item_theme(param_name, invalid_input_theme)


def parameter_write(sender, app_data, user_data):
    param = user_data
    param_type = param.data_type
    input_text = dpg.get_value(param.name)

    if is_valid(param_type, input_text):
        try:
            user_commands.put((param, input_text, "write", param.name), block=False)
        except queue.Full:
            print("Commands queue is full!")


def parameter_read(sender, app_data, user_data):
    param = user_data
    try:
        user_commands.put((param, "=?", "read", f"{param.name}_read_data"), block=False)
    except queue.Full:
        print("Commands queue is full!")


def parameters_window():
    if dpg.does_item_exist("turbo_parameters"):
        dpg.delete_item("turbo_parameters")

    with dpg.theme() as valid_input:
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 255, 0])

    with dpg.theme() as invalid_input:
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0])

    with dpg.window(
        label="Trubo parameters",
        tag="turbo_parameters",
        pos=[100, 100],
        max_size=[1000, 600],
        autosize=True,
        modal=False,
    ):
        for param in Parameters:
            with dpg.group(horizontal=True):
                dpg.add_button(label="Read", callback=parameter_read, user_data=param)
                dpg.add_text(param.name)
                dpg.add_input_text(
                    tag=param.name,
                    width=350,
                    indent=200,
                    hint=type_description(param.data_type),
                    enabled=param.is_writeable,
                    callback=on_change,
                    user_data=(valid_input, invalid_input),
                )
                dpg.bind_item_theme(param.name, valid_input)
                dpg.add_button(label="Write", callback=parameter_write, user_data=param)
                dpg.add_text(tag=f"{param.name}_read_data")
