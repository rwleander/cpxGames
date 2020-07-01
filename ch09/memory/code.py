#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#  Copyright (c) 2020 Rick Leander All rights reserved
#  Buy the book at https://www.amazon.com/author/rleander
#
# The Memory Game 

from adafruit_circuitplayground import cp
import random
import time

#constants

note_time = 0.5

lose_sound = 'Boing.wav'

brightness = 100
red = 0x600000
green = 0x006000
blue = 0x000060
yellow = 0x303000

colors = [red, yellow, green, blue]
pixels = [1, 3, 6, 8]
tones = [261.63, 293.66, 329.63, 349.23]

# read the touch pads

def read_touch():
  touch = -1
  while touch < 0:
    if cp.touch_A4:
      touch = 0
    if cp.touch_A6:
      touch = 1
    if cp.touch_A3:
      touch = 2
    if cp.touch_A1:
      touch = 3
    time.sleep(0.2)

  return touch;

# play a note

def play_note(note):
  cp.pixels.fill(0)
  cp.pixels[pixels[note]] = colors[note]
  cp.play_tone(tones[note], note_time)

# play the song

def play_song(notes):
  for note in notes:
    play_note(note)
  cp.pixels.fill(0)

# have player play back notes

def read_song(notes):
  win_lose = True
  n = 0
  while n < len(notes) and win_lose:
    new_note = read_touch()
    play_note(new_note)
    if notes[n] != new_note:
      win_lose = False
    n = n + 1

  if win_lose == False:
    cp.play_file(lose_sound)
  return win_lose

# game loop

def play_game():
  notes = [random.randint(0, 3)]
  win_lose = True
  while win_lose == True:
    play_song(notes)
    win_lose = read_song(notes)
    notes.append(random.randint(0, 3))
    time.sleep(1)

# main game loop - wait for button press

cp.pixels.brightness = brightness
cp.pixels.fill(0)
while True:
  if read_touch() >= 0:
    play_game()
