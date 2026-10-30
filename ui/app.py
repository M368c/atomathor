import dearpygui.dearpygui as dpg

from ui import pressure, turbo
from turbo_pump.turbo_comm import data as turbo_data
from pcb_comm import data as pcb_data
from pcb_comm import user_commands


def create_qui():
    dpg.create_context()

    # Fonts
    with dpg.font_registry():
        default_font = dpg.add_font(
            "./ui/fonts/proggyvectordotted/ProggyVector-Regular.otf", 20
        )
        second_font = dpg.add_font(
            "./ui/fonts/proggyvectordotted/ProggyVector-Dotted.otf", 20
        )

    dpg.bind_font(default_font)

    # Menu bar
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Setting 1", check=True)
            dpg.add_menu_item(label="Setting 2", check=True)

    create_main_window()

    dpg.create_viewport(title="Atomathor", width=800, height=600)
    dpg.set_primary_window("main", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()

    while dpg.is_dearpygui_running():
        pressure.update_pressure_plot()  # Updating plot
        turbo.update_speed()
        handle_serial_response()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


def send_command():
    address = dpg.get_value("address_cmd")
    msg = dpg.get_value("msg_cmd")

    if address and msg:
        user_commands.put((address, "cm", msg), block=False)
    else:
        dpg.set_value("pcb_response", "Invalid command")


def open_cmd():
    if dpg.does_item_exist("address_cmd"):
        dpg.delete_item("address_cmd")
    if dpg.does_item_exist("msg_cmd"):
        dpg.delete_item("msg_cmd")
    if dpg.does_item_exist("pcb_response"):
        dpg.delete_item("pcb_response")

    with dpg.window(
        label="Command prompt",
        pos=[240, 40],
        autosize=True,
        modal=False,
    ):
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="address_cmd",
                hint="Enter address",
                width=180,
            )
            dpg.add_input_text(
                tag="msg_cmd",
                hint="Enter msg",
                width=180,
            )

            dpg.add_button(label="Write", callback=send_command)
        dpg.add_text(tag="pcb_response")


def create_main_window():
    with dpg.window(tag="main", label="main"):
        dpg.add_text("")
        dpg.add_button(label="Open commands prompt", callback=open_cmd)
        pressure.build()
        turbo.build()


def handle_serial_response():
    try:
        pcb_response = pcb_data.get_nowait()  # (msg_id, msg)
        dpg.set_value("pcb_response", pcb_response[1])
    except:
        pass

    try:
        turbo_response = turbo_data.get_nowait()  # (parameter, data, caller)
        caller = turbo_response[2]
        response_data = turbo_response[1]
        dpg.set_value(caller, response_data)
    except:
        pass
