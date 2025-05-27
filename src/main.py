import threading

from util import cli
from config import config
from control import detection
from gui import gui

def main():
    cli.init_cli()
    config.load()
    cli.set_cli_values()
    
    if config.instance.is_daemon:
        gui_exit_event = threading.Event()
        detection.start_detection(gui_exit_event) # Will spawn GUI in separate thread on detection.
        gui_exit_event.wait() # Wait indefinitely until the GUI exits.
    else:
        detection.start_if_active()
        gui.start()
    
    config.save()

if __name__ == "__main__":
    main()
