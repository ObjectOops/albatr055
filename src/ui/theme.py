import dearpygui.dearpygui as dpg

from util import resource

def set_global_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            theme_data = [
                (dpg.mvThemeCol_Text, (0, 255, 0, 255)),
                (dpg.mvThemeCol_ButtonHovered, (30, 235, 40, 105)),
                (dpg.mvThemeCol_ButtonActive, (0, 200, 25, 155)),
                (dpg.mvThemeCol_CheckMark, (0, 200, 5, 155)),
                (dpg.mvThemeCol_TextSelectedBg, (0, 200, 25, 155)),
                (dpg.mvThemeCol_FrameBgHovered, (30, 235, 40, 105)),
                (dpg.mvThemeCol_FrameBgActive, (0, 200, 25, 155)),
                (dpg.mvThemeCol_HeaderHovered, (30, 235, 40, 105)),
                (dpg.mvThemeCol_HeaderActive, (0, 200, 25, 155)),
                (dpg.mvThemeCol_TitleBgActive, (0, 0, 0)),
                (dpg.mvThemeCol_WindowBg, (0, 0, 0))
            ]
            for target, color in theme_data:
                dpg.add_theme_color(target, color, category=dpg.mvThemeCat_Core)
    dpg.bind_theme(global_theme)
    
    with dpg.font_registry():
        default_font = dpg.add_font(resource.get_resource("res/cour.ttf"), 15)
    dpg.bind_font(default_font)
