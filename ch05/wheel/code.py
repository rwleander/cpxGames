#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#    Copyright (c) 2020 Rick Leander All rights reserved
#
# spinning wheel

from adafruit_circuitplayground import cp
import random
import time

# constants

alert_sound = 'Fanfare.wav' 

red = 0x600000
green = 0x006000
blue = 0x000060
white = 0x282828

colors = [red, blue, green]

# set next pixel

def set_pixels(n, delay):
  color = int(n % 3)
  pixel = 9 - int(n % 10)

  cp.pixels[pixel] = white
  time.sleep(delay)
  cp.pixels[pixel] = colors[color]


# spin the wheel

def spin_wheel():
  cp.pixels.fill(0)
  delay = 0.1
  n = 0

#  spin faster while button is down
    
  while cp.button_a:
    set_pixels(n, delay)

    n = n + 1
    delay = delay - random.random() * 0.05
    if delay < 0.001:
      delay = 0.001

# slow down when button comes up

  while delay < 0.5 :
    set_pixels(n, delay)
    n = n + 1
    delay = delay + random.random() * 0.05

  cp.play_file(alert_sound)
  return n + 1
          
#main game loop

cp.pixels.brightness = 100
cp.pixels.fill(0)
blink = 0.25
n = 0  

while True:
  if cp.button_a:
    n = spin_wheel()

  if n > 0:
    set_pixels(n, blink)
    time.sleep(blink)

      