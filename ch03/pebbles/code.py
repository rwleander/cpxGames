# pebbles game

from adafruit_circuitplayground import cp
import random
import time

#constants

win_sound ='Fanfare.wav' 
lose_sound = 'Boing.wav'
beep_sound = 'blip2.wav'

blue = 0x000060

#  set the number of pixels

def set_pixels(i):
  cp.pixels.fill(blue)
  n = 9
  while n > i:
    cp.pixels[n] = 0
    n = n - 1


# read buttons

def read_buttons(i):
  done = 0
  n = 0
  while done == 0:
    if cp.button_a:
      cp.play_file(beep_sound)
      n = n + 1
    if cp.button_b:
      done = 1
    if n > 2:
      n = 1
    if n > i:
      n = i
    set_pixels(i - n)
  return n
   

# get machine's move

def get_move(i):
  j = i % 3
  if j == 0:
    return 1
  else:
    return j

#  play the game

def play_game():
  cp.pixels.fill(blue)
  i = random.randint(8, 9)
  while i > 0:
    set_pixels(i)
    n = read_buttons(i)
    i = i - n
    if i == 0:
      cp.play_file(win_sound)
      return

    n = get_move(i)
    time.sleep(0.25)
    i = i - 1
    set_pixels(i)
    cp.play_file(beep_sound)
    if n == 2:
      time.sleep(0.25)
      i = i - 1
      set_pixels(i)
      cp.play_file(beep_sound)
    if i == 0:
      cp.play_file(lose_sound)

#  main loop - wait for button press

cp.pixels.brightness = 100
cp.pixels.fill(0)
while True:
  if cp.button_a:
    time.sleep(1)
    play_game()
  time.sleep(0.1)

