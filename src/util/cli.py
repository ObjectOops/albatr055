"""
Capabilities:
- Launch with specific configuration file.
- Launch and immediately lock input from all keyboards and/or mice.
- Set an unlock passphrase for this specific session.
- Set a unlock duration for this specific session.
- Lock mouse on detection for this specific session.
- Launch in active mode.
- Launch session in background (enables active mode).
- Set all other detection options for this specific session.
- Set log keystrokes for this specific session.
"""

import argparse

from config import constants, config
from control import device_lock
from util import passphrase_utils

args = None
ephemeral_mode = None

def init_cli():
    global args, ephemeral_mode
    
    parser = argparse.ArgumentParser(
        description="Lock device input from all keyboards and/or mice with a GUI. An anti-(BadUSB / Rubber Ducky) tool. Note: All options (except -l, -a, and -b) will disable making changes to the configuration file from the GUI.",
        epilog="MIT License, Copyright (c) 2025 Alex Yao"
    )

    parser.add_argument("config_file", nargs="?", default=constants.INIT_FILE_PATH, type=str, help="Path to configuration file. Default: `./albatr055.ini`")
    parser.add_argument("-l", "--lock", choices=["keyboard", "mouse", "all"], help="Immediately lock input from devices.")
    parser.add_argument("-p", "--passphrase", type=str, help="Unlock passphrase. Use 'none' to disable.")
    parser.add_argument("-u", "--auto-unlock-enabled", action="store_true", default=None, help="Enable auto unlock timer.")
    parser.add_argument("-d", "--auto-unlock-duration", type=int, help="Auto unlock duration in seconds.")
    parser.add_argument("-m", "--lock-mouse-on-detection", action="store_true", default=None, help="Lock mouse on detection.")
    parser.add_argument("-a", "--active", action="store_true", help="Launch with active detection. This state may be saved to the configuration file.")
    parser.add_argument("-b", "--background", action="store_true", help="Launch as background process. Detection will be active regardless of configuration. Conflicts with: `--lock`")
    parser.add_argument("-k", "--kps-threshold", type=float, help="Keys per second threshold for detection.")
    parser.add_argument("-s", "--sample-size", type=int, help="Sample size for detection.")
    parser.add_argument("--listen-hotkeys", action="store_true", default=None, help="Enable listening for suspicious hotkeys.")
    parser.add_argument("--hotkeys", nargs="+", type=str, help="List of suspicious hotkeys to listen for. Appends to default hotkeys if the first argument is \"*\". Example: --hotkeys * '<ctrl>+<shift>+<esc>'")
    parser.add_argument("-i", "--ignore-recurring", action="store_true", default=None, help="Ignore recurring keystrokes in detection.")
    parser.add_argument("-t", "--log-on-detection", action="store_true", default=None, help="Log detection events.")
    parser.add_argument("--log-keystrokes", action="store_true", default=None, help="Immediately begin logging all keystrokes.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {constants.VERSION}", help="Show version information.")
    parser.add_argument("--relaunched", action="store_true", help="Not intended for general CLI use. Indicates that the process has been relaunched in the background. Can be used for debugging purposes.")

    args = parser.parse_args()
    
    ephemeral_mode = any(arg is not None for arg in [
        args.passphrase, 
        args.auto_unlock_enabled, 
        args.auto_unlock_duration, 
        args.lock_mouse_on_detection, 
        args.kps_threshold, 
        args.sample_size, 
        args.listen_hotkeys, 
        args.hotkeys, 
        args.ignore_recurring, 
        args.log_on_detection, 
        args.log_keystrokes
    ])

def set_cli_values():
    set_passphrase()
    set_auto_unlock_enabled()
    set_auto_unlock_duration()
    set_lock_mouse_on_detection()
    set_active()
    test_background_lock_conflict()
    set_kps_threshold()
    set_sample_size()
    set_listen_hotkeys()
    set_hotkeys()
    set_ignore_recurring()
    set_log_on_detection()
    set_log_keystrokes()

def immediate_actions():
    immediate_lock()

def option_override_value(option_value, config_value):
    return option_value if option_value is not None else config_value

def immediate_lock():
    if args.lock == "keyboard":
        device_lock.lock_keyboard()
    elif args.lock == "mouse":
        device_lock.lock_mouse()
    elif args.lock == "all":
        device_lock.lock_keyboard()
        device_lock.lock_mouse()

def set_passphrase():
    if args.passphrase is None:
        return
    if args.passphrase.lower() == "none":
        config.instance.passphrase_enabled = False
        return
    if not passphrase_utils.is_valid_passphrase(args.passphrase):
        print(
f"""-p: Invalid Passphrase
Passphrase characters must be a part of this character set:
\"{constants.VALID_PASSPHRASE_CHARACTERS}\"""")
        exit(1)
    
    passphrase_utils.set_passphrase(args.passphrase)

def set_auto_unlock_enabled():
    config.instance.auto_unlock_enabled = (
        args.auto_unlock_enabled or config.instance.auto_unlock_enabled
    )

def set_auto_unlock_duration():
    config.instance.auto_unlock_duration = option_override_value(
        args.auto_unlock_duration, config.instance.auto_unlock_duration
    )
    if config.instance.auto_unlock_duration < 0:
        print("-d: Invalid Auto Unlock Duration\nAuto unlock duration cannot be negative.")
        exit(1)

def set_lock_mouse_on_detection():
    config.instance.lock_mouse_on_detection = args.lock_mouse_on_detection or config.instance.lock_mouse_on_detection

def set_active():
    config.instance.detection_active = args.active or config.instance.detection_active

def test_background_lock_conflict():
    if args.background and args.lock:
        print("-b: Option Conflict\n`--background` is incompatible with `--lock`.")
        exit(1)

def set_kps_threshold():
    config.instance.kps_threshold = option_override_value(
        args.kps_threshold, config.instance.kps_threshold
    )
    if config.instance.kps_threshold <= 0:
        print("-k: Invalid KPS Threshold\nKPS threshold must be a positive number.")
        exit(1)

def set_sample_size():
    config.instance.sample_size = option_override_value(
        args.sample_size, config.instance.sample_size
    )
    if config.instance.sample_size < 2:
        print("-s: Invalid Sample Size\nSample size must be greater than or equal to 2.")
        exit(1)

def set_listen_hotkeys():
    config.instance.listen_hotkeys = args.listen_hotkeys or config.instance.listen_hotkeys

def set_hotkeys():
    if args.hotkeys is None:
        return
    
    if args.hotkeys[0] == "*":
        config.instance.hotkey_blacklist.extend(args.hotkeys[1:])
    else:
        config.instance.hotkey_blacklist = args.hotkeys

def set_ignore_recurring():
    config.instance.ignore_recurring = args.ignore_recurring or config.instance.ignore_recurring

def set_log_on_detection():
    config.instance.log_on_detection = args.log_on_detection or config.instance.log_on_detection

def set_log_keystrokes():
    config.instance.log_keystrokes = args.log_keystrokes or config.instance.log_keystrokes
