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
    parser.add_argument("-p", "--passphrase", type=str, help="Unlock passphrase.")
    parser.add_argument("-d", "--auto-unlock-duration", type=int, help="Auto unlock duration in seconds.")
    parser.add_argument("-m", "--lock-mouse-on-detection", action="store_true", default=None, help="Lock mouse on detection.")
    parser.add_argument("-a", "--active", action="store_true", help="Launch with active detection. This state may be saved to the configuration file.")
    parser.add_argument("-b", "--background", action="store_true", help="Launch as background process. Detection will be active regardless of configuration. Conflicts with: `--lock`")
    parser.add_argument("-k", "--kps-threshold", type=float, help="Keys per second threshold for detection.")
    parser.add_argument("-s", "--sample-size", type=int, help="Sample size for detection.")
    parser.add_argument("--listen-hotkeys", action="store_true", default=None, help="Enable listening for suspicious hotkeys.")
    parser.add_argument("--hotkeys", nargs="*", type=str, help="List of suspicious hotkeys to listen for. Example: '<ctrl>+<shift>+<esc>'")
    parser.add_argument("-i", "--ignore-recurring", action="store_true", default=None, help="Ignore recurring keystrokes in detection.")
    parser.add_argument("-t", "--log-on-detection", action="store_true", default=None, help="Log detection events.")
    parser.add_argument("--log-keystrokes", action="store_true", default=None, help="Immediately begin logging all keystrokes.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {constants.VERSION}", help="Show version information.")

    args = parser.parse_args()
    
    ephemeral_mode = bool(
        args.passphrase 
        or args.auto_unlock_duration 
        or args.lock_mouse_on_detection 
        or args.kps_threshold 
        or args.sample_size 
        or args.listen_hotkeys 
        or args.hotkeys 
        or args.ignore_recurring 
        or args.log_on_detection 
        or args.log_keystrokes
    )

def set_cli_values():
    set_passphrase()
    set_unlock_duration()
    set_lock_mouse_on_detection()
    set_active()
    test_background_lock_conflict()

def immediate_actions():
    immediate_lock()

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
    if not passphrase_utils.is_valid_passphrase(args.passphrase):
        print(
f"""-p: Invalid Passphrase
Passphrase characters must be a part of this character set:
\"{constants.VALID_PASSPHRASE_CHARACTERS}\"""")
        exit(1)
    
    passphrase_utils.set_passphrase(args.passphrase)

def set_unlock_duration():
    auto_unlock_duration = args.auto_unlock_duration or config.instance.auto_unlock_duration
    if auto_unlock_duration < 0:
        print("-d: Invalid Auto Unlock Duration\nAuto unlock duration must be a positive integer.")
        exit(1)
    
    config.instance.auto_unlock_duration = auto_unlock_duration

def set_lock_mouse_on_detection():
    config.instance.lock_mouse_on_detection = args.lock_mouse_on_detection or config.instance.lock_mouse_on_detection

def set_active():
    config.instance.detection_active = args.active or config.instance.detection_active

def test_background_lock_conflict():
    if args.background and args.lock:
        print("-b: Option Conflict\n`--background` is incompatible with `--lock`.")
        exit(1)
