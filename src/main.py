import threading, subprocess, sys, os

from util import cli, resource
from config import config
from control import detection
from gui import gui

def main():
    cli.init_cli()
    if cli.args.background and not cli.args.relaunched:
        relaunch_in_background()
        return
    
    config.load()
    cli.set_cli_values()
    
    if config.instance.is_daemon:
        gui_exit_event = threading.Event()
        detection.start_detection(gui_exit_event) # Will spawn GUI in separate thread on detection.
        gui_exit_event.wait() # Wait indefinitely until the GUI exits.
    else:
        detection.start_if_active()
        gui.start()
    
    # Configuration is saved before exiting by `gui.start`.

def relaunch_in_background():
    argv = sys.argv[1:] if resource.is_bundled() else sys.argv
    subprocess.Popen(
        [
            sys.executable, 
            *argv, 
            "--relaunched"
        ],
        # Leave stderr alone for debugging purposes.
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        # Setting this environment variables gives the new background instance 
        # its own temp directory if bundled with onefile.
        env={**os.environ, "PYINSTALLER_RESET_ENVIRONMENT": "1"}
    )

if __name__ == "__main__":
    main()
