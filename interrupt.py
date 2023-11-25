#!/usr/bin/env python3
# interrupt - easily create "X hours of silence occasionally broken by Y" audios
# v0.0.1            GPL-3.0 License
# Sergey Lavrent    https://github.com/hiimsergey/interrupt

import argparse
import math
import random
from os.path import basename
from pydub import AudioSegment

import utils

# CLI argument parser
parser = argparse.ArgumentParser(description='Easily create "X hours of silence occasionally broken by Y" audios')
parser.add_argument("input", nargs="+", help="paths of the sounds to include")
parser.add_argument("--base", "-b", help="audio to interrupt instead of silence")
parser.add_argument("--cycle", "-c", action="store_true", help="include audios in order instead of randomly")
parser.add_argument("--length", "-l", default=60, help="length of the generated audio in minutes")
parser.add_argument("--output", "-o", default=utils.placeholder_name(), help="path of the generated audio")
parser.add_argument("--seed", "-s", help="randomization seed of the algorithm")
parser.add_argument("--verbose", "-v", action="store_true", help="print additional info like timestamps")
parser.add_argument("--volume", "-V", help="increase/decrease in volume in dB")
args = parser.parse_args()

# CLI argumenet actions
args.length = float(args.length)

if args.verbose:
    print("{} {}\n{} {}\n{} {}\n".format(
        utils.colorize("Output path:", "blue"),
        utils.colorize(utils.colorize(args.output, "yellow"), "bold"),
        utils.colorize("Included sounds:", "blue"),
        # TODO NOW
        utils.colorize(utils.colorize(utils.input_as_str(args.input), "yellow"), "bold"),
        utils.colorize("Length:", "blue"),
        utils.ms_to_timestamp(args.length * 60_000)
    ))

if args.seed:
    if args.verbose: print("{} {}\n".format(
        utils.colorize("Seed:", "blue"),
        utils.colorize(utils.colorize(args.seed, "yellow"), "italic")
    ))
    random.seed(args.seed)

if args.base:
    if args.verbose: print("{} {}\n".format(
        utils.colorize("Base audio:", "blue"),
        basename(args.base)
    ))
    result = AudioSegment.from_mp3(args.base)
    if args.length > len(result) / 60_000: # if --length is longer than the base audio
        if args.verbose: print(f"WARNING: provided length is longer than the base audio, using full length\n")
        args.length = len(result)
else:
    result = AudioSegment.silent(duration=args.length * 60_000) # --length in ms

if args.cycle:
    if args.verbose: print("{}".format(utils.colorize("Cycling enabled\n", "magenta")))
    cycle_index = 0

# Construct audio
i = random.randint(0, args.length * 6_000) # tenth of --length in ms
while i < args.length * 60_000:
    if args.cycle:
        chosen_sound = args.input[cycle_index % len(args.input)]
        cycle_index += 1
    else: chosen_sound = random.choice(args.input)
    if args.verbose: print(f"{utils.ms_to_timestamp(i)}: {chosen_sound}")
    result = result[:i] + AudioSegment.from_mp3(chosen_sound) + result[i + len(chosen_sound):]
    i += random.randint(0, args.length * 6_000)

# Increase/decrease volume of the result audio
if args.volume:
    if args.verbose: print("\n{}".format(utils.colorize(f"Altering volume by {args.volume}dB", "magenta"))) # TODO \\n only next to {}
    result += args.volume

# Export
if args.verbose: print("{}".format(utils.colorize("\nExporting audio... This takes a moment...", "green")))
result[:args.length * 60_000].export(args.output, format="mp3")
if args.verbose: print("{}".format(utils.colorize("Done :)", "green")))

# TODO make this script format agnostic (currently mp3 only)
# TODO redo the entire algorithm for if args.base
# TODO learn what part of the main logic is so slow
# TODO compress the audios in size
# TODO why does this quit on long videos?
