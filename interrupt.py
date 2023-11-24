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
def input_as_str(): return ", ".join(map(basename, args.input))

def ms_to_timestamp(ms):
    hours = math.floor(ms / 3_600_000)      # convert ms to h and floor
    minutes = math.floor(ms / 60_000 % 60)  # convert ms to min and take hour rest using modulo
    seconds = math.floor(ms / 1_000 % 60)   # convert ms to s and take minute rest using modulo
    
    return "{}h {:02d}min {:02d}s".format(hours, minutes, seconds)

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

if args.verbose: print("Output path: {}\nIncluded sounds: {}".format(args.output, input_as_str()))
if args.cycle:
    print(f"Cycling enabled")
    cycle_index = 0

if args.seed:
    if args.verbose: print(f"Seed: {args.seed}")
    random.seed(args.seed)

if args.base:
    if args.verbose: print(f"Base audio: {basename(args.base)}\n")
    result = AudioSegment.from_mp3(args.base)
    if args.length > len(result) / 60_000: # if --length is longer than the base audio
        if args.verbose: print(f"WARNING: provided length is longer than the base audio, using full length\n")
        args.length = len(result)
else:
    if args.verbose: print(f"Base audio: silence\nLength: {ms_to_timestamp(args.length * 60_000)}\n")
    result = AudioSegment.silent(duration=random.randint(0, args.length * 6_000)) # args.length divided by ten in ms

# Construct audio
while len(result) < args.length * 60_000:
    if args.cycle:
        cycle_index += 1
        chosen_sound = args.input[cycle_index % len(args.input)]
    else: chosen_sound = random.choice(args.input)
    if args.verbose: print(f"{ms_to_timestamp(len(result))}: {chosen_sound}")
    result += AudioSegment.from_mp3(chosen_sound)

    result += AudioSegment.silent(duration=random.randint(0, args.length * 6_000))

# Increase/decrease volume of the result audio
if args.volume:
    if args.verbose: print(f"\nAltering volume by {args.volume}dB\n")
    result += args.volume

# Export
if args.verbose: print("Exporting audio... This takes a moment...")
result[:args.length * 60_000].export(args.output, format="mp3")
if args.verbose: print("\nDone :)")

# TODO make this script format agnostic (currently mp3 only)
# TODO color output
# TODO redo the entire algorithm for if args.base
