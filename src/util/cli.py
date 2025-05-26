"""
Capabilities:
- Launch with specific configuration file.
- Launch and immediately lock input from all keyboards and/or mice.
- Set an unlock passphrase for this specific session.
- Set a unlock duration for this specific session.
- Lock mouse on detection for this specific session.
- Launch session in background.
- Set all other detection options for this specific session.
- Set log keystrokes for this specific session.
"""

import argparse

from config import constants

args = None
ephemeral_mode = None

def init_cli():
    global args, ephemeral_mode
    
    parser = argparse.ArgumentParser(
        description="Lock device input from all keyboards and/or mice with a GUI. An anti-(BadUSB / Rubber Ducky) tool. Note: Setting values via the CLI will disable changes to the configuration file.",
        epilog="MIT License, Copyright (c) 2025 Alex Yao"
    )

    parser.add_argument("config_file", nargs="?", default=constants.INIT_FILE_PATH, type=str, help="Path to configuration file. Default: `./albatr055.ini`")
    parser.add_argument("-l", "--lock", choices=["keyboard", "mouse", "all"], help="Immediately lock input from devices.")
    parser.add_argument("-p", "--passphrase", type=str, help="Unlock passphrase.")
    parser.add_argument("-d", "--unlock-duration", type=int, help="Unlock duration in seconds.")
    parser.add_argument("-m", "--lock-mouse-on-detection", action="store_true", default=None, help="Lock mouse on detection.")
    parser.add_argument("-b", "--background", action="store_true", help="Launch in background. Conflicts with: `--lock`")
    parser.add_argument("-k", "--kps-threshold", type=float, help="Keys per second threshold for detection.")
    parser.add_argument("-s", "--sample-size", type=int, help="Sample size for detection.")
    parser.add_argument("--listen-hotkeys", action="store_true", default=None, help="Enable listening for suspicious hotkeys.")
    parser.add_argument("--hotkeys", nargs="*", type=str, help="List of suspicious hotkeys to listen for. Example: '<ctrl>+<shift>+<esc>'")
    parser.add_argument("-i", "--ignore-recurring", action="store_true", default=None, help="Ignore recurring keystrokes in detection.")
    parser.add_argument("-t", "--log-on-detection", action="store_true", default=None, help="Log detection events.")
    parser.add_argument("--log-keystrokes", action="store_true", default=None, help="Immediately begin logging all keystrokes.")

    args = parser.parse_args()
    
    ephemeral_mode = bool(
        args.passphrase 
        or args.unlock_duration 
        or args.lock_mouse_on_detection 
        or args.kps_threshold 
        or args.sample_size 
        or args.listen_hotkeys 
        or args.hotkeys 
        or args.ignore_recurring 
        or args.log_on_detection 
        or args.log_keystrokes
    )
