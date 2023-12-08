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
