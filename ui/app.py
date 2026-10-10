import dearpygui.dearpygui as dpg
import main

dpg.create_context()

# Fonts
with dpg.font_registry():
    default_font = dpg.add_font("fonts/proggyvectordotted/ProggyVector-Regular.otf", 20)
    second_font = dpg.add_font("fonts/proggyvectordotted/ProggyVector-Dotted.otf", 20)

dpg.bind_font(default_font)

# Menu bar
with dpg.viewport_menu_bar():
    with dpg.menu(label="Settings"):
        dpg.add_menu_item(label="Setting 1", check=True)
        dpg.add_menu_item(label="Setting 2", check=True)

# Window
with dpg.window(tag="main", label="main"):
    dpg.add_text("")
    main.build()


dpg.create_viewport(title="Atomathor", width=800, height=600)
dpg.set_primary_window("main", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()

dpg.destroy_context()
