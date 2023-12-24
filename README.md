# interrupt
Easily create "X hours of silence occasionally broken by Y" audios

```
usage: interrupt.py [-h] [--base BASE] [--cycle] [--length LENGTH]
                    [--output OUTPUT] [--seed SEED] [--verbose]
                    [--volume VOLUME]
                    input [input ...]

Easily create "X hours of silence occasionally broken by Y" audios

positional arguments:
  input                 paths of the sounds to include

options:
  -h, --help            show this help message and exit
  --base BASE, -b BASE  audio to interrupt instead of silence
  --cycle, -c           include audios in order instead of randomly
  --length LENGTH, -l LENGTH
                        length of the generated audio in minutes
  --output OUTPUT, -o OUTPUT
                        path of the generated audio
  --seed SEED, -s SEED  randomization seed of the algorithm
  --verbose, -v         print additional info like timestamps
  --volume VOLUME, -V VOLUME
                        increase/decrease in volume in dB
```

## Features

### Length
Through `--length` you can set the length of the desired audio in minutes (default is 60):

```sh
# create an audio for half an hour
$ python interrupt.py sound.mp3 --length 30
```

### Multiple sounds
You are not limited to one single sound. You can add multiple different sounds to one single audio:

```sh
$ python interrupt.py cave_sound1.mp3 cave_sound2.mp3 cave_sound3.mp3
```

#### Random or sequential order
You can also choose whether the sounds should have a random order or a strict order. Use the `--cycle` flag for the latter.

### Base audio
Instead of silence, you can select a custom audio file to be infested with sounds, like a song:

```sh
$ python interrupt.py ad1.mp3 ad2.mp3 ad3.mp3 --base youtube_video.mp3
```

### Volume
You can also increase or decrease the volume of these sounds (relative to how they sound originally) in dB:

```sh
# make the sound 30dB quieter
$ python interrupt.py sound.mp3 --volume -30
# make the sound 100dB louder so you can scare yourself
$ python interrupt.py sound.mp3 --volume 100
```
