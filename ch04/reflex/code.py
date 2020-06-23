#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#    Copyright (c) 2020 Rick Leander All rights reserved
#
# Reflex game

from adafruit_circuitplayground import cp
import random
import time

#constants

max_moles = 40
moles_to_win = 25
note_time = 0.2

win_sound = 'Fanfare.wav' 
lose_sound = 'Boing.wav'
whack_sound = 'cowbell.wav' 

red = 0x600000
green = 0x006000
blue = 0x000060
yellow = 0x303000

colors = [red, yellow, green, blue]
pixels = [1, 3, 6, 8]
tones = [261.63, 293.66, 329.63, 349.23]

# read the touch pads

def read_touch(wait):
  touch = -1
  delay = wait
  while touch < 0 and delay >= 0:
    if cp.touch_A4:
      touch = 0
    if cp.touch_A6:
      touch = 1
    if cp.touch_A3:
      touch = 2
    if cp.touch_A1:
      touch = 3
    time.sleep(0.2)
    delay = delay - 0.2

  return touch;

# show the mole

def show_mole(mole):  
  cp.pixels.fill(0)
  cp.pixels[pixels[mole]] = colors[mole]
  cp.play_tone(tones[mole], note_time)

# game loop

def play_game():
  win_lose = 0
  wait = 1
  hits = 0
  n = 0
  while n < max_moles and win_lose == 0:
    mole = random.randint (0, 3)
    show_mole(mole)
    touch = read_touch(wait)
    if touch == mole:
      hits = hits + 1
      cp.play_file(whack_sound)
    time.sleep(0.1)
    n = n + 1
    if n % 5 == 0:
      wait = wait - 0.1
    if hits > moles_to_win:
      win_lose = 1

  cp.pixels.fill(0)
  if win_lose == 1:
    cp.play_file(win_sound)
    cp.play_file(win_sound)    
    cp.play_file(win_sound)
  else: 
    cp.play_file (lose_sound)
    cp.play_file (lose_sound)
    cp.play_file (lose_sound)
  time.sleep(2)

# main game loop - wait for button press

while True:
  if read_touch(1) > 0:
    play_game()
