from logging import getLogger

from openrazer.client import DaemonNotFound, DeviceManager, constants as razer_constants

from hyprrazer import config_contants as conf
from hyprrazer.layout import layouts
import csv

ERR_DAEMON_OFF = -2  # openrazer is not running
ERR_NO_KEYBOARD = -3  # no razer keyboard found
ERR_CONFIG = -4  # Error in config file


class hyprRazer:
    _logger = None

    # Keyboard settings
    _serial = ""
    _keyboard = None
    _key_layout = {}
    _key_layout_name = ""  # Only present if layout is set manually

    # handle modes and keys
    _listen_to_keys = set()  # the keys which could change the displayed color scheme
    _current_pressed_keys = set()
    _current_scheme_name = ""
    _mode = None

    _drawing_scheme = set()  # prevent infinite inherit loop in color schemes

    # Thread handling
    _hook = None
    _running = False

    def __init__(self, layout=None, logger=None):
        """
        layout: keyboard Layout to use for lighting the keys. If none is given it is detected automatically
        logger: Logger to use for logging
        """
        if not logger:
            logger = getLogger(__name__)
        self._logger = logger
        self._key_color_mapping = {}
        self._logger.info("Loading Razer Keyboard")
        self._load_keyboard(layout)
        self._logger.info("Loading done")

    def _draw_static_scheme_from_csv(self):
        """
        Draw static color scheme from the loaded CSV data
        """
        self._keyboard.fx.advanced.matrix.reset()
        for key_code, hex_value in self._key_color_mapping.items():
            # if field == conf.all_keys:
            #     keys = self._key_layout.keys()
            # else:
            #     # field is a key array
            #     self._set_color(color, keys)
            try:
                # Convert the key code to an integer
                # key = self._key_layout.get(key_code)
                # Apply hex_value to the key represented by key_code
                hex_pairs = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]
                color = [int(pair, 16) for pair in hex_pairs]
                print(f"Applying color {hex_value} to key {key_code}")  # Debug print statement
                self._keyboard.fx.advanced.matrix[self._key_layout.get(key_code)] = color
            except ValueError:
                self._logger.warning(f"Invalid key code format: '{key_code}'")
        self._keyboard.fx.advanced.draw()

    def _load_layout_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    key_code = row[0]
                    hex_value = row[1]
                    # Store the key code and hex value mapping
                    self._key_color_mapping[key_code] = hex_value
                else:
                    self._logger.warning("Invalid row in CSV file")

        # Apply the loaded layout
        self._draw_static_scheme_from_csv()


    def _set_color(self, color, keys):
        for key in keys:
            if key in self._key_layout:
                self._keyboard.fx.advanced.matrix[self._key_layout[key]] = color
            else:
                self._logger.warning(f"Key '{key}' not found in Layout")

    def _load_keyboard(self, layout):
        """
        Load Keyboard on startup
        """
        self._key_layout_name = layout
        if not self.reload_keyboard():
            self._logger.critical("No Razer Keyboard found")
            exit(ERR_NO_KEYBOARD)

    ###############################################
    # public methods to change or query the state #
    ###############################################

    def start(self):
        """
        Start the shortcut visualisation. This starts a new Thread.
        Stop this by calling stop() on the object.
        """
        if not self._running:
            self._logger.warning("Starting Hook")
            # self._setup_key_hook()
            # self._hook.start()
            self._running = True
            self._update_color_scheme()

    def stop(self):
        """
        stops the program by stopping the internal thread waiting for keyboard events
        """
        if self._running:
            self._logger.warning(f"Stopping hook")
            self._running = False
            self._hook.cancel()
            self._hook = None

    def reload_keyboard(self, layout=None) -> bool:
        """
        Reloads to the computer connected keyboards, and could set an layout
        return: true if a razer keyboard was loaded
        """
        try:
            device_manager = DeviceManager()
        except DaemonNotFound:
            self._logger.critical("Openrazer daemon not running")
            exit(ERR_DAEMON_OFF)
        for device in device_manager.devices:
            if device.type == "keyboard":
                self._keyboard = device
                break

        if self._keyboard:
            if layout:
                self._key_layout_name = layout
            device_manager.sync_effects = False
            self._serial = str(self._keyboard.serial)
            self.load_layout(self._key_layout_name)
        else:
            self._logger.error("no razer keyboard found")
            return False
        self._logger.info(f"successfully loaded Keyboard {self._keyboard.name}")
        return True

    def load_layout(self, layout_name=None) -> bool:
        """
        Loads the named layout for the current keyboard. If none is named, the layout is detected automatically
        returns False if the layout cannot be found, the layout is not changed
        """
        # Keysyms have a new map if layout changed
        if self._hook:
            self._hook.reset_keysyms()

        no_layout = False  # flow control
        if not layout_name:
            no_layout = True
            if self._keyboard:
                layout_name = self._keyboard.keyboard_layout
                self._logger.info(f"Detected Layout {layout_name}")
        if layout_name not in layouts and no_layout:
            self._logger.error(f"Layout {layout_name} not found, using default 'en_US'")
            layout_name = "en_US"  # en_US is default and in layout.py

        if layout_name in layouts:
            # Load the layout
            self._key_layout = layouts[layout_name]
            self._logger.info(f"Loaded keyboard layout {layout_name}")
            return True

    def get_mode_name(self) -> str:
        """
        returns the name of the current mode
        """
        if self._mode:
            return self._mode[conf.field_name]
        else:
            # if no mode loaded, return default name
            return conf.mode_default

    def get_color_scheme_name(self) -> str:
        """
        returns the current drawn color scheme
        """
        return self._current_scheme_name

    def force_update_color_scheme(self):
        """
        deletes internal variables and detects which color scheme to show
        """
        self._current_scheme_name = ""
        self._update_color_scheme()
