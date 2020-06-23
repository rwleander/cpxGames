#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#    Copyright (c) 2020 Rick Leander All rights reserved
#
# space invaders

from adafruit_circuitplayground import cp
import random
import time

# control values

max_kills = 20
max_aliens = 4
delay = 0.5
delay_incr = 0.05

# globals

col1 = []
col2 = []
fire = 0
aliens = 4
kills = 0

# constants

invader_color = 0x00C000
missile_color = 0x600000
explosion_color = 0xF0F0F0

beep_sound = 'blip2.wav' 
fire_sound = 'cymbal.wav' 
hit_sound = 'hi_snare.wav'
win_sound = 'Fanfare.wav' 
lose_sound = 'Boing.wav'


#  show board

def show_pixels(n):
  global col1, col2

  cp.pixels.fill (0)
  i = 0
  while i < 5:
    if col1[i] == 1:
      cp.pixels[i] = invader_color
    if col2[i] == 1:
      cp.pixels[9 - i] = invader_color

    if col1[i] == 2:
      cp.pixels[i] = explosion_color
    if col2[i] == 2:
      cp.pixels[9 - i] = explosion_color

    if col1[i] == 11:
      cp.pixels[i] = missile_color
    if col2[i] == 11:
      cp.pixels[9 - i] = missile_color
    i = i + 1

  if n % 5 == 0:
    cp.play_file(beep_sound)

#  add new aliens

def add_aliens(n):
  global col1, col2, aliens

  if n % 5 == 0:
    if aliens < max_aliens:
      rnd = random.randint(1, 3)
      if rnd == 1 and col1[1] == 0:
        col1[0] = 1
        aliens = aliens + 1
      if rnd == 2 and col2[0] == 0:
        col2[0] = 1
        aliens = aliens + 1

# check for button

def check_buttons():
  global col1, col2, fire

  if fire == 0:
    if cp.button_a:
      col1[4] = 11
      cp.play_file(fire_sound)
      fire = 1
    if cp.button_b:
      col2[4] = 11
      cp.play_file(fire_sound)
      fire = 1

# clear kills

def clear_kills(col):
  i = 0
  while i < 5:
    if col[i] == 2:
      col[i] = 0
    i = i + 1

  return col

# move missile up

def move_missile(col):
  global aliens, kills, fire  

  i = 0
  while i < 5:
    if col[i] == 11:
      if i == 0:
        col[i] = 0
        fire = 0
      elif col[i - 1] == 2:
        col[i] = 0
        fire = 0
      elif col[i-1] == 1: 
        col[i - 1] = 2
        col[i] = 0
        cp.play_file(hit_sound)
        kills = kills + 1
        aliens = aliens - 1
        fire = 0
      elif i > 0:
        col[i - 1] = col[i]
        col[i] = 0
    i = i + 1

  return col

# move aliens down

def move_aliens(col):
  global aliens, kills, fire

  win_lose = 0
  i = 4
  while i >= 0:
    if col[i] == 1:
      if i == 4:
        col[i] = 0
        win_lose = -1
      elif col[i+1] == 11:
        col[i + 1] = 2
        col[i] = 0
        cp.play_file(hit_sound)
        kills = kills + 1
        aliens = aliens - 1
        fire = 0
      elif i < 4:
        col[i + 1] = col[i]
        col[i] = 0
    i = i - 1

  return [col, win_lose]

# move game objects in columns

def move_objects(col, n):
  win_lose = 0

  col = clear_kills(col)
  col = move_missile(col)

  if n % 5 == 0:
    [col, win_lose] = move_aliens(col)
    if win_lose == -1:
      return [col, -1]

  if kills >= max_kills:
    return [col,1]
  else:
    return [col, 0]


# game loop

def play_game():
  global col1, col2, fire, aliens, kills

  col1 = [1, 1, 0, 0, 0]
  col2 = [1, 1, 0, 0, 0]
  fire = 0
  aliens = 4
  kills = 0
  win_lose = 0
  d = delay
  n = 1

  while win_lose == 0:
    show_pixels(n)
    [col1, win_lose] = move_objects(col1, n)
    [col2, win_lose] = move_objects(col2, n)
    check_buttons()
    add_aliens(n)
    time.sleep(d)

    n = n + 1
    if n % 50 == 0:
      d = d - delay_incr

#    print ([col1, col2, aliens, fire, kills])

  if win_lose == 1:
    cp.play_file(win_sound)
  else:
    cp.play_file(lose_sound)
  

# main loop


cp.pixels.brightness = 100
while True:
  if cp.button_a:
    time.sleep(1)
    play_game()
