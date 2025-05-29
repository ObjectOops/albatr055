<!-- View Online (latest version): https://github.com/ObjectOops/albatr055/blob/main/README.md -->

# albatr055

<p align="center">
  <img src="./assets/icon_1080.png" alt="Logo." width="256" height="256" />
  <br>
  Lock device input from all keyboards and/or mice with a GUI. An anti-(BadUSB / Rubber Ducky) tool.
</p>

___

[Prebuilt releases available for Windows (10 or 11), macOS (arm64), and GNU/Linux (glibc 2.39).](https://github.com/ObjectOops/albatr055/releases)

## Features

- Cross-platform
- GUI and CLI
- Launch as background process
- Persistent configuration
- Manually lock keyboard / mouse
- Optional unlock passphrase
- Automatic unlock after specified duration
- Toggleable detection
- Lock keyboard and mouse on detection
- Configurable detection settings
- Hotkey detection
- Logging

> [!Important]
> **Disclaimer**: This software has not *yet* been tested against an actual BadUSB. It listens for all keystrokes sent to the system and responds if the rate of keystrokes received exceeds the configured keys-per-second threshold.

## Usage

### GUI

| Dashboard | Keyboard Locked | Mouse Locked |
| :---: | :---: | :---: |
| <img width="320" alt="image" src="https://github.com/user-attachments/assets/711b1e17-b085-44d2-8f2a-964b5bd6f30e" /> | <img width="320" alt="image" src="https://github.com/user-attachments/assets/09bf7711-3a7a-4f80-acdf-30b704d316d9" /> | <img width="320" alt="image" src="https://github.com/user-attachments/assets/0af17ed4-e106-430b-bab2-94bf3ad8d9e5" /> |

### CLI

```
usage: albatr055[.exe] [-h] [-l {keyboard,mouse,all}] [-p PASSPHRASE] [-u]
                       [-d AUTO_UNLOCK_DURATION] [-m] [-a] [-b]
                       [-k KPS_THRESHOLD] [-s SAMPLE_SIZE] [--listen-hotkeys]
                       [--hotkeys HOTKEYS [HOTKEYS ...]] [-i] [-t]
                       [--log-keystrokes] [-v] [--relaunched]
                       [config_file]

Lock device input from all keyboards and/or mice with a GUI. An anti-(BadUSB /
Rubber Ducky) tool. Note: All options (except -l, -a, and -b) will disable
making changes to the configuration file from the GUI.

positional arguments:
  config_file           Path to configuration file. Default: `./albatr055.ini`

options:
  -h, --help            show this help message and exit
  -l, --lock {keyboard,mouse,all}
                        Immediately lock input from devices.
  -p, --passphrase PASSPHRASE
                        Unlock passphrase. Use 'none' to disable.
  -u, --auto-unlock-enabled
                        Enable auto unlock timer.
  -d, --auto-unlock-duration AUTO_UNLOCK_DURATION
                        Auto unlock duration in seconds.
  -m, --lock-mouse-on-detection
                        Lock mouse on detection.
  -a, --active          Launch with active detection. This state may be saved
                        to the configuration file.
  -b, --background      Launch as background process. Detection will be active
                        regardless of configuration. Conflicts with: `--lock`
  -k, --kps-threshold KPS_THRESHOLD
                        Keys per second threshold for detection.
  -s, --sample-size SAMPLE_SIZE
                        Sample size for detection.
  --listen-hotkeys      Enable listening for suspicious hotkeys.
  --hotkeys HOTKEYS [HOTKEYS ...]
                        List of suspicious hotkeys to listen for. Appends to
                        default hotkeys if the first argument is "*". Example:
                        --hotkeys * '<ctrl>+<shift>+<esc>'
  -i, --ignore-recurring
                        Ignore recurring keystrokes in detection.
  -t, --log-on-detection
                        Log detection events.
  --log-keystrokes      Immediately begin logging all keystrokes.
  -v, --version         Show version information.
  --relaunched          Not intended for general CLI use. Indicates that the
                        process has been relaunched in the background. Can be
                        used for debugging purposes.

MIT License, Copyright (c) 2025 Alex Yao
```

> [!Note]
> To configure the hotkey blacklist, add hotkeys manually to your configuration file (e.g. `albatr055.ini`). You can use the keystroke log to obtain identifiers for each key.

## Contributing

### Requirements

- Python 3.13.1 (might work with earlier versions)
- `requirements.txt`
    - Dear PyGui
    - pynput (> 1.7.7 if using Python 3.13)

### Run

1. `pip install -r requirements.txt`
2. `python src/main.py` or `python src\main.py` (Windows)
