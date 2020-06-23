#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#    Copyright (c) 2020 Rick Leander All rights reserved
#
# space lander game

from adafruit_circuitplayground import cp
import random
import time

# initial values

gravity = -1.62
high_thrust = 10.0
low_thrust = 2.0
altitude = 1000.0
velocity = -10.0
final_velocity = -5.0
delay = 0.5

# other constants

win_sound = 'Fanfare.wav'
lose_sound = 'Boing.wav'

white_tone = 880
blue_tone = 300
red_tone = 440

white = 0x020202
blue = 0x000060
red = 0x0600000

pixels = [4, 3, 2, 1, 0, 9, 8, 7, 6,5]

# global variables

last_pixel = 9

# show location

def show_location(a, v):
  pixel = 9
  if a < 1000:
    pixel = int(a / 100)
    if a < 0:
      pixel = 0

  color = red
  tone = red_tone
  if v > 0:
    color = white
    tone = white_tone
  if v <= final_velocity: 
    color = blue
    tone = blue_tone
  cp.pixels.fill(0)
  cp.pixels[pixels[pixel]] = color

  if pixel != last_pixel:
    cp.play_tone(tone, 0.2)
  last_ppixel = pixel
     

# game loop

def play_game():
  a = altitude
  v = velocity
  n = 0

  cp.pixels.fill(0)  
  show_location(a, v)
  print ('Altitude', 'Velocity')

  while a > 0 and a < 12000:
    t = 0.0
    if cp.button_a:
      t = high_thrust
    if cp.button_b:
      t = low_thrust

    v = gravity + t + v
    a = a + v
    show_location(a, v)
    if n % 10 == 0:
      print (a, v)
    time.sleep(delay)

  if v < final_velocity or a > 12000:
    cp.play_file(lose_sound)
  else:
    cp.play_file (win_sound)
  time.sleep(2)
 
#  main loop

while True:
  if cp.button_a:
    play_game()
  time.sleep(0.5)
  
