# skeet shooting

from adafruit_circuitplayground import cp
import random
import time

#constants

pixels = [2, 1, 0, 9, 8, 7]

clay_color = 0x000080
hit_color = 0x303030
difficulty_color = 0x300000

launch_sound = 'cowbell.wav' 
hit_sound = 'hi_snare.wav' 
miss_sound = 'Boing.wav'
win_sound = 'Fanfare.wav'  

# set a pixel

def show_pixel(i, direction, color):
  cp.pixels.fill(0)
  if direction == 0:
    cp.pixels[pixels[i]] = color
  else:
    cp.pixels[pixels[5 - i]] = color    

# play one round

def play_round(direction, delay):
  cp.play_file(launch_sound)
  fire = 0
  i = 0
  while i < 6:
    show_pixel(i, direction, clay_color)

    j = 0
    while j < 5:
      if fire == 0:
        if cp.button_a and direction == 0:
          fire = i
        if cp.button_b and direction == 1:
          fire = i
      time.sleep(delay / 5)
      j = j + 1

    if i == 3:
      if fire  == 3:
        show_pixel(i, direction, hit_color)
        cp.play_file(hit_sound)
        cp.pixels.fill(0)
        return 1

    i = i + 1

  cp.pixels.fill(0)
  cp.play_file(miss_sound)
  return 0


def play_game(difficulty):
  score = 0
  if difficulty == 0:
    delay = 2.0 / 6.0 
    score = play_round(0, delay)
    score = score + play_round(1, delay)
  elif difficulty == 1:
    delay = 2.0 / 6.0
    score = play_round(random.randint(0, 1), delay)
    score = score + play_round(random.randint(0, 1), delay)
  elif difficulty == 2:
    score = play_round(0, random.random() * 0.5)
    score = score + play_round(1, random.random() * 0.5)

  if score == 2:
    cp.play_file(win_sound)

# set difficulty level

def set_difficulty(difficulty):
  difficulty = difficulty + 1
  if difficulty > 2:
    difficulty = 0
  cp.pixels.fill(0)
  cp.pixels[9 - difficulty] = difficulty_color
  return difficulty

# main game loop

cp.pixels.brightness = 100
cp.pixels.fill(0)
difficulty = 0

while True:
  if cp.button_a:
    play_game(difficulty)
  if cp.button_b:
    difficulty = set_difficulty(difficulty)
  time.sleep(0.5)
