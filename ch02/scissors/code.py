#  Python code for Ten Games for the Circuit Playground Express
#    by Rick Leander
#  Copyright (c) 2020 Rick Leander All rights reserved
#  Buy the book at https://www.amazon.com/author/rleander
#
# Scissors, Paper, Rock

from adafruit_circuitplayground import cp
import random
import time

# constants

names = ['', 'scissors', 'paper', 'rock']
results = ['', 'Scissors cut paper', 'Paper covers rock', 'Rock breaks scissors']

prompt_sound = 'Cowbell.wav'
win_sound = 'Fanfare.wav' 
tie_sound = 'blip2.wav'
lose_sound = 'Boing.wav' 

brightness = 100
green = 0x006000
yellow = 0x303000
red = 0x600000

# get players selection
#   first beep three times,
#   then wait for button presses

def read_pick1():
  cp.play_file(prompt_sound)
  time.sleep(0.5)
  cp.play_file(prompt_sound)
  time.sleep(0.5)
  cp.play_file(prompt_sound)
  time.sleep(0.5)

  btn1 = False
  btn2 = False
  n = 0
  while n < 10:
    if cp.button_a:   
      btn1 = True
    if cp.button_b:
      btn2 = True
    time.sleep(0.2)
    n = n + 1

  pick1 = 0
  if btn1:
    pick1 = pick1 + 1
  if btn2:
    pick1 = pick1 + 2
  return pick1  

#  show the results of the match

def show_match(pick1, pick2, msg, win_lose):
  color = yellow
  sound = tie_sound

  print (names[pick1] + ' - ' + names[pick2])
  if win_lose == 1:
    print (msg + ' - You win')
    sound = win_sound    
    color = green
  elif win_lose == -1:
    print (msg + ' - You lose')
    sound = lose_sound
    color = red
  else:
    print (msg)

  cp.pixels.fill(0)
  if pick2 == 1 or pick2 == 3:
    cp.pixels[0] = color
  if pick2 == 2 or pick2 == 3:
    cp.pixels[9] = color
  cp.play_file (sound)
  time.sleep(2)

# show the score then wait for a button click

def show_score(score1, score2):
  cp.pixels.fill(0)
  n = 1
  while n < 6: 
    if n < score1:
      cp.pixels[n - 1] = green
    if n < score2:
      cp.pixels[10 - n] = red
    n = n + 1

  print (str(score1) + ' to ' + str(score2))
  if score1 >= 5:
    print ('You win')
    cp.play_file(win_sound)
    cp.play_file(win_sound)
  if score2 >= 5:
    print ('You lose')
    cp.play_file(lose_sound)
    cp.play_file(lose_sound)

  while cp.button_a == False and cp.button_b == False:
    time.sleep(0.5)


# play a round of the game

def play_round():
  msg = ''
  win_lose = 0

  pick1 = read_pick1()  
  pick2 = random.randint(0, 2) + 1

# determine winner

  if pick1 == pick2:
    msg = 'Tie'

  elif pick1 == 1:
    if pick2 == 2:
      msg = results[1]
      win_lose = 1
    elif pick2 == 3:
      msg = results[3]
      win_lose = -1      
      
  elif pick1 == 2:
    if pick2 == 1:
      msg = results[1]
      win_lose = -1
    elif pick2 == 3:
      msg = results[2]
      win_lose = 1      

  elif pick1 == 3:
    if pick2 == 1:
      msg = results[3]
      win_lose = 1 
    elif pick2 == 2:
      msg = results[2]
      win_lose = -1

  show_match(pick1, pick2, msg, win_lose)
  return win_lose

# game loop

def play_game():
  score1 = 0
  score2 = 0

  while score1 < 5 and score2 < 5:
    win_lose = play_round() 
    if win_lose == 1:
      score1 = score1 + 1
    if win_lose == -1:
      score2 = score2 + 1
    show_score(score1, score2)



# main loop

cp.pixels.brightness = brightness
cp.pixels.fill(0)
while True:
  if cp.button_a or cp.button_b:
    play_game()


