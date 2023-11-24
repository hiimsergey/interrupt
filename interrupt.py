#!/usr/bin/env python3
# interrupt - easily create "X hours of silence occasionally broken by Y" audios
# v0.0.1            GPL-3.0 License
# Sergey Lavrent    https://github.com/hiimsergey/interrupt

import argparse
import math
import random
from datetime import datetime
from os.path import basename
from pydub import AudioSegment

# Helper functions
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

def input_as_str(): return ", ".join(map(basename, args.input))

def ms_to_timestamp(ms):
    hours = math.floor(ms / 3_600_000)      # convert ms to h and floor
    minutes = math.floor(ms / 60_000 % 60)  # convert ms to min and take hour rest using modulo
    seconds = math.floor(ms / 1_000 % 60)   # convert ms to s and take minute rest using modulo
    
    return colorize("{}h {:02d}min {:02d}s".format(hours, minutes, seconds), "cyan")

def placeholder_name():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"interrupt_{timestamp}.mp3"

# CLI argument parser
parser = argparse.ArgumentParser(description='Easily create "X hours of silence occasionally broken by Y" audios')
parser.add_argument("input", nargs="+", help="paths of the sounds to include")
parser.add_argument("--base", "-b", help="audio to interrupt instead of silence")
parser.add_argument("--cycle", "-c", action="store_true", help="include audios in order instead of randomly")
parser.add_argument("--length", "-l", default=60, help="length of the generated audio in minutes")
parser.add_argument("--output", "-o", default=placeholder_name(), help="path of the generated audio")
parser.add_argument("--seed", "-s", help="randomization seed of the algorithm")
parser.add_argument("--verbose", "-v", action="store_true", help="print additional info like timestamps")
parser.add_argument("--volume", "-V", help="increase/decrease in volume in dB")
args = parser.parse_args()

# CLI argumenet actions
args.length = float(args.length)

if args.verbose: print("{} {}\n{} {}".format(
    colorize("Output path:", "blue"),
    colorize(colorize(args.output, "yellow"), "bold"),
    colorize("Included sounds:", "blue"),
    colorize(colorize(input_as_str(), "yellow"), "bold")
))

print("{} {}\n".format(
    colorize("Length:", "blue"),
    ms_to_timestamp(args.length * 60_000)
))

if args.seed:
    if args.verbose: print("{} {}\n".format(
        colorize("Seed:", "blue"),
        colorize(colorize(args.seed, "yellow"), "italic")
    ))
    random.seed(args.seed)

if args.base:
    if args.verbose: print("{} {}\n".format(
        colorize("Base audio:", "blue"),
        basename(args.base)
    ))
    result = AudioSegment.from_mp3(args.base)
    if args.length > len(result) / 60_000: # if --length is longer than the base audio
        if args.verbose: print(f"WARNING: provided length is longer than the base audio, using full length\n")
        args.length = len(result)
else:
    result = AudioSegment.silent(duration=random.randint(0, args.length * 6_000)) # --length divided by ten in ms

if args.cycle:
    print("{}".format(colorize("Cycling enabled\n", "magenta")))
    cycle_index = 0

# Construct audio
while len(result) < args.length * 60_000: # convert --length from ms to min
    if args.cycle:
        cycle_index += 1
        chosen_sound = args.input[cycle_index % len(args.input)]
    else: chosen_sound = random.choice(args.input)
    if args.verbose: print(f"{ms_to_timestamp(len(result))}: {chosen_sound}")
    result += AudioSegment.from_mp3(chosen_sound)

    result += AudioSegment.silent(duration=random.randint(0, args.length * 6_000))

# Increase/decrease volume of the result audio
if args.volume:
    if args.verbose: print("\n{}".format(colorize(f"Altering volume by {args.volume}dB", "magenta"))) # TODO \\n only next to {}
    result += args.volume

# Export
if args.verbose: print("{}".format(colorize("\nExporting audio... This takes a moment...", "green")))
result[:args.length * 60_000].export(args.output, format="mp3")
if args.verbose: print("{}".format(colorize("Done :)", "green")))

# TODO make this script format agnostic (currently mp3 only)
# TODO redo the entire algorithm for if args.base
# TODO learn what part of the main logic is so slow
# TODO compress the audios in size
# TODO why does this quit on long videos?
