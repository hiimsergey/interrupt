# utils.py - helper functions

import math
from os.path import basename
from datetime import datetime

def colorize(string, color):
    color_dict = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "purple": "\033[45m", # TODO bg magenta
        "reset": "\033[0m", # default color
        "bold": "\033[1m",
        "italic": "\033[3m"
    }
    return f"{color_dict.get(color)}{string}{color_dict['reset']}"

def input_as_str(args_input): return ", ".join(map(basename, args_input))

def ms_to_timestamp(ms):
    hours = math.floor(ms / 3_600_000)      # convert ms to h and floor
    minutes = math.floor(ms / 60_000 % 60)  # convert ms to min and take hour rest using modulo
    seconds = math.floor(ms / 1_000 % 60)   # convert ms to s and take minute rest using modulo
    
    return colorize("{}h {:02d}min {:02d}s".format(hours, minutes, seconds), "cyan")

def placeholder_name():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"interrupt_{timestamp}.mp3"
