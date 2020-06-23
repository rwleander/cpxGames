#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#    Copyright (c) 2020 Rick Leander All rights reserved
#
# pong

from adafruit_circuitplayground import cp
import time

# game settings

delay_start = 0.25
delay_end = 0.05
delay_incr = 0.025

# constants

tones = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
lights = [2, 1, 0, 9, 8, 7]
color = 0x000080

winner = 'Fanfare.wav'
loser = 'Boing.wav'

# show spot

def show_spot(spot):
  n = lights[spot]
  cp.pixels.fill(0)
  cp.pixels[n] = color

# play tone if slide switch is set to the right

def play_note (note):
  cp.stop_tone()
  if cp.switch == False:
    cp.start_tone(tones[note])

# game loop

def play_game():
  cp.pixels.brightness = 50
  cp.pixels.fill(0)

  spot = -1 
  direction = 1
  delay = delay_start
  win_lose = 0
  
  while win_lose == 0:
    spot = spot + direction
    show_spot(spot)
    play_note(spot)

    if spot >= 5:
      direction = -1
      if cp.button_b == False:
        win_lose = -1
    elif spot <= 0:
      direction = 1
      delay = delay - delay_incr
      if cp.button_a == False:
        win_lose = -1
    elif spot > 1 and spot < 5: 
      if cp.button_a or cp.button_b:
        win_lose = -1
    
    time.sleep(delay)
    if delay <= delay_end:
      win_lose = 1

  cp.pixels.fill(0)
  cp.stop_tone()
  if win_lose > 0:
    cp.play_file (winner)
  else:
    cp.play_file(loser)

# main loop - start game when button pressed

while True:
  if cp.button_a or cp.button_b:
    play_game() 



        
  