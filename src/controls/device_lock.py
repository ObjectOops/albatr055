import dearpygui.dearpygui as dpg
from pynput import keyboard, mouse

from config.init_file import Config, save
from util import passphrase_hash
from controls import logging, detection
from util import inputs

def challenge():
    if not Config.instance.passphrase_enabled:
        unlock_keyboard()
        unlock_mouse()
        return
    passphrase = dpg.get_value("passphrase_input")
    hash = passphrase_hash.hash(passphrase)
    if hash != Config.instance.passphrase_hash:
        if not dpg.does_item_exist("challenge_notice"):
            dpg.add_text(
                "Incorrect passphrase.",
                tag="challenge_notice",
                parent="passphrase_prompt"
            )
        return
    unlock_keyboard()
    unlock_mouse()

def passphrase_prompt():
    if dpg.does_item_exist("passphrase_prompt"):
        return
    
    with dpg.window(
        tag="passphrase_prompt",
        no_close=True,
        no_move=True,
        width=400,
        height=150,
        pos=(0, 0)
    ):
        if Config.instance.passphrase_enabled:
            dpg.add_text("« Enter Passphrase »")
            dpg.add_input_text(
                tag="passphrase_input",
                password=True,
                on_enter=True,
                callback=challenge
            )
            dpg.add_button(label="Submit", callback=challenge)
        else:
            dpg.add_button(label="Unlock", callback=challenge)

def lock_keyboard():
    def on_press(key):
        logging.log_key_down(key)
        if not Config.instance.passphrase_enabled:
            return
        if key == keyboard.Key.backspace:
            dpg.set_value("passphrase_input", dpg.get_value("passphrase_input")[:-1])
        elif key == keyboard.Key.enter:
            challenge()
        else:
            try:
                dpg.set_value("passphrase_input", dpg.get_value("passphrase_input") + key.char)
            except AttributeError:
                pass
    
    def on_release(key):
        logging.log_key_up(key)
    
    detection.stop_detection()
    
    inputs.set_keyboard_listener(
        keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=True
        )
    )
    
    passphrase_prompt()
    if Config.instance.passphrase_enabled:
        dpg.configure_item("passphrase_input", readonly=True)

def unlock_keyboard():
    inputs.set_keyboard_listener(None)
    dpg.delete_item("passphrase_prompt")
    
    if Config.instance.detect_active:
        detection.start_detection()

def lock_mouse():
    passphrase_prompt()
    dpg.set_primary_window("passphrase_prompt", value=True)
    dpg.configure_viewport(0, always_on_top=True, decorated=False)
    dpg.configure_item("primary_window", show=False)

def unlock_mouse():
    dpg.set_primary_window("primary_window", value=True)
    dpg.configure_viewport(0, always_on_top=False, decorated=True)
    dpg.configure_item("primary_window", show=True)

def confirm():
    passphrase_1 = dpg.get_value("passphrase_input_1")
    passphrase_2 = dpg.get_value("passphrase_input_2")
    if len(passphrase_1) == 0:
        Config.instance.passphrase_enabled = False
        save()
        dpg.delete_item("set_passphrase_prompt")
        return
    if passphrase_1 != passphrase_2:
        if not dpg.does_item_exist("passphrase_notice"):
            dpg.add_text(
                "Passphrases do not match.",
                tag="passphrase_notice",
                parent="set_passphrase_prompt"
            )
        return
    valid_characters = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    for character in passphrase_1:
        if character not in valid_characters:
            dpg.add_text(
                f"Password characters must be a part of this character set:\n\"{valid_characters}\"",
                tag="passphrase_notice",
                parent="set_passphrase_prompt"
            )
            return
    Config.instance.passphrase_hash = passphrase_hash.hash(passphrase_1)
    Config.instance.passphrase_enabled = True
    save()
    dpg.delete_item("set_passphrase_prompt")

def set_passphrase():
    if dpg.does_item_exist("set_passphrase_prompt"):
        return
        
    with dpg.window(
        label="Set Passphrase",
        tag="set_passphrase_prompt",
        no_collapse=True,
        no_close=True,
        width=400,
        height=150,
        pos=[25, 25]
    ):
        dpg.add_input_text(
            tag="passphrase_input_1",
            hint="Leave empty for no passphrase.",
            password=True,
            on_enter=True,
            callback=confirm
        )
        dpg.add_input_text(
            tag="passphrase_input_2",
            hint="Confirm passphrase.",
            password=True,
            on_enter=True,
            callback=confirm
        )
        with dpg.group(horizontal=True):
            dpg.add_button(label="Confirm", callback=confirm)
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("set_passphrase_prompt"))
