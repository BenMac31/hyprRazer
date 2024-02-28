#!/usr/bin/python3

import logging
import os
import csv
from argparse import ArgumentParser

from i3razer.i3_razer import ConfigParser, I3Razer
from i3razer.map_layout import map_layout

from openrazer.client import __version__ as openrazer_version

__all__ = [
    "I3Razer",
    "ConfigParser",
    "main",
    "__version__",
]

__version__ = "0.2"

def main():
    # Arguments
    parser = ArgumentParser()
    parser.add_argument("--version", help="Display version information and exit", action="store_true")
    parser.add_argument("--map", help="Map keyboard layout of connected Razer keyboards", action="store_true")

    default_config = os.path.join(os.path.dirname(__file__), "example_config.yaml")
    parser.add_argument("-c", "--config", default=default_config, help="Config file")
    parser.add_argument("-l", "--layout", help="Keyboard layout for colored keys. Usually detected automatically")
    parser.add_argument("-v", help="Be more verbose", action="count", default=0)
    parser.add_argument("-s", "--color-scheme", help="Color scheme to set")
    parser.add_argument("-f", "--csv-file", help="CSV file containing key codes and hex values")

    args = parser.parse_args()

    # only output version
    if args.version:
        print(f"i3 razer version: {__version__}")
        print(f"open razer version: {openrazer_version}")
        exit()

    # map a new layout
    if args.map:
        map_layout()
        exit()

    # set verbosity
    if args.v >= 3:
        level = logging.DEBUG
    elif args.v == 2:
        level = logging.INFO
    elif args.v == 1:
        level = logging.WARNING
    else:
        level = logging.ERROR
    logging.basicConfig(format="%(message)s", level=level)

    # start
    i3razer = I3Razer(config_file=args.config, layout=args.layout)
    
    # Set color scheme if provided
    if args.color_scheme:
        success = i3razer.change_color_scheme(args.color_scheme)
        if not success:
            print(f"Color scheme '{args.color_scheme}' not found.")
        else:
            print(f"Color scheme set to '{args.color_scheme}'.")
        exit()

    # Handle CSV file
    if args.csv_file:
        try:
            with open(args.csv_file, "r") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if len(row) >= 2:
                        key_code = row[0].lower()
                        hex_value = row[1].lower()
                        # Apply hex_value to the key represented by key_code
                        if key_code in i3razer._key_layout:
                            i3razer._key_color_mapping[key_code] = hex_value
                        else:
                            print(f"Key code '{key_code}' not found in layout")
                    else:
                        print("Invalid row in CSV file:", row)
            # Apply the loaded layout
            i3razer._draw_static_scheme_from_csv()
        except FileNotFoundError:
            print("CSV file not found:", args.csv_file)
        exit()

    i3razer.start()
if __name__ == "__main__":
    main()

